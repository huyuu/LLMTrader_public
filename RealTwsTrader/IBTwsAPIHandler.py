from BrokerHandler import BrokerHandler
from CustomOrder import *
from CustomPosition import *
import json
from time import sleep
import threading
from multiprocessing import Event, Lock
from datetime import datetime, timedelta
import time
import os
import pandas as pd

from ibapi import wrapper
from ibapi.wrapper import EWrapper
from ibapi.client import EClient
from ibapi.utils import getTimeStrFromMillis, longMaxString
from ibapi.utils import iswrapper

# types
from ibapi.common import * # @UnusedWildImport
from ibapi.order_condition import * # @UnusedWildImport
from ibapi.contract import * # @UnusedWildImport
from ibapi.order import * # @UnusedWildImport
from ibapi.order_cancel import * # @UnusedWildImport
from ibapi.order_state import * # @UnusedWildImport
from ibapi.execution import Execution
from ibapi.execution import ExecutionFilter
from ibapi.commission_and_fees_report import CommissionAndFeesReport
from ibapi.ticktype import * # @UnusedWildImport
from ibapi.tag_value import TagValue

from ibapi.account_summary_tags import *

import xmltodict
import yaml



class IBTwsAPIHandler(EWrapper, EClient, BrokerHandler):
    def __init__(self):
        EClient.__init__(self, self)
        BrokerHandler.__init__(self)
        self.nextId = 0
        self.async_flags = {}
        self.async_results = {}
        self.lock = Lock()

# MARK: - Public

    def async_run(self) -> bool:
        didSucceed = self._connect_to_server()
        if not didSucceed:
            return False
        tws_thread = threading.Thread(target=self.run, daemon=True)
        tws_thread.start()
        sleep(3)
        return True

    def run(self):
        while True:
            super().run()

    def get_balance(self):
        pass

    def post_new_order(self, order: CustomOrder) -> CustomOrder:
        contract = Contract()
        contract.symbol = order.symbol
        contract.secType = "STK"
        contract.exchange = "SMART"
        contract.currency = "USD"
        contract.primaryExchange = "NASDAQ"

        ib_order = Order()
        if order.orderId is None: # creating a brand new order
            ib_order.orderId = self.getNextValidId()
            order.orderId = ib_order.orderId
        else: # updating an existing order
            ib_order.orderId = order.orderId
        ib_order.action = order.action
        ib_order.tif = order.expiration
        ib_order.orderType = order.type
        if order.type == "LMT":
            ib_order.lmtPrice = order.price
        ib_order.totalQuantity = order.amount

        self.placeOrder(ib_order.orderId, contract, ib_order)
        return order

    def update_order(self, order: CustomOrder):
        self.post_new_order(order)

    def cancel_order(self, order: CustomOrder):
        self.cancelOrder(orderId=order.orderId, orderCancel=OrderCancel())

    def cancel_all_open_orders(self):
        self.reqGlobalCancel(orderCancel=OrderCancel())
        sleep(3)

    # def fetch_all_open_orders(self):
    #     self._init_async_flags_and_results(func_name="OpenOrder")
    #     self.reqOpenOrders()
    #     open_order = self._await_get_future_return(func_name="OpenOrder")
    #     return open_order

    def fetch_positions(self) -> list[CustomPosition]:
        self._init_async_flags_and_results(func_name="Position")
        self.reqPositions()
        print("Fetching positions...")
        sleep(60)
        positions: dict[str, CustomPosition] = self._await_get_future_return(func_name="Position")
        print(f"{len(positions)} positions fetched")
        if positions is None or len(positions) == 0:
            return []
        return list(positions.values())
    
    def post_exit_positions(self, positions: list[CustomPosition]):
        for position in positions:
            if position.symbol in self.config["symbols_to_avoid"]:
                continue
            if position.amount == 0:
                continue
            if position.is_long:
                if self.config["howToExitPreviousPositions"] == "MKT":
                    self.post_new_order(CustomOrder_Market_Sell(position.symbol, position.amount))
                elif self.config["howToExitPreviousPositions"] == "MOO":
                    if self.hasMarketOpened():
                        self.post_new_order(CustomOrder_Market_Sell(position.symbol, position.amount))
                    else:
                        self.post_new_order(CustomOrder_Market_Sell_On_Open(position.symbol, position.amount))
                elif self.config["howToExitPreviousPositions"] == "MOC":
                    self.post_new_order(CustomOrder_Market_On_Close_Sell(position.symbol, position.amount))
                else:
                    raise ValueError(f"Invalid howToExitPreviousPositions: {self.config['howToExitPreviousPositions']}")
            else: # short position
                if self.config["howToExitPreviousPositions"] == "MKT":
                    self.post_new_order(CustomOrder_Market_Buy(position.symbol, position.amount))
                elif self.config["howToExitPreviousPositions"] == "MOO":
                    if self.hasMarketOpened():
                        self.post_new_order(CustomOrder_Market_Buy(position.symbol, position.amount))
                    else:
                        self.post_new_order(CustomOrder_Market_Buy_On_Open(position.symbol, position.amount))
                elif self.config["howToExitPreviousPositions"] == "MOC":
                    self.post_new_order(CustomOrder_Market_On_Close_Buy(position.symbol, position.amount))
                else:
                    raise ValueError(f"Invalid howToExitPreviousPositions: {self.config['howToExitPreviousPositions']}")

    def post_exit_all_positions(self):
        positions = self.fetch_positions()
        sleep(10)
        self.post_exit_positions(positions)
        sleep(10)
    
    def fetch_earnings_dates_for_symbol(self, symbol: str, start_date: datetime, end_date: datetime, conid: int = None) -> list:
        if conid is None:
            conid = self.fetch_contractIds_of_symbols([symbol])[0]

        self._init_async_flags_and_results(func_name="WshMetaData")
        self.reqWshMetaData(self.getNextValidId())  # Request WSH metadata
        wsh_meta_data = self._await_get_future_return(func_name="WshMetaData")

        wsh_event_data = WshEventData()
        wsh_event_data.conId = f"{conid}"
        if isinstance(start_date, datetime):
            wsh_event_data.startDate = start_date.strftime("%Y%m%d")
        elif isinstance(start_date, str):   
            wsh_event_data.startDate = start_date
        else:
            raise ValueError(f"Invalid start_date: {start_date}")
        if isinstance(end_date, datetime):
            wsh_event_data.endDate = end_date.strftime("%Y%m%d")
        elif isinstance(end_date, str):
            wsh_event_data.endDate = end_date
        else:
            raise ValueError(f"Invalid end_date: {end_date}")

        reqIdForWshEventData = self.getNextValidId()
        self._init_async_flags_and_results(func_name="WshEventData")
        self.reqWshEventData(reqIdForWshEventData, wsh_event_data, 0)  # Request earnings events
        sleep(0.5)
        self.cancelWshEventData(reqIdForWshEventData)
        wsh_event_data = self._await_get_future_return(func_name="WshEventData")
        earnings_dates = []
        if wsh_event_data is None:
            return []
        for event in wsh_event_data:
            if event["event_type"] == "wshe_ed":
                event_data = event["data"]
                url = event_data["announcement_url"] if "announcement_url" in event_data else None
                earnings_dates.append((event_data["earnings_date"], event_data["time_of_day"], url))
                print(f"Symbol: {symbol} - Earnings date: {event_data['earnings_date']} - Time of day: {event_data['time_of_day']}")
            # elif event["event_type"] == "wshe_eps":
            #     actual_eps = event["data"]["amount_oc"]
            #     estimated_eps = event["data"]["estimated_eps"]
            #     surprise_percent = event["data"]["change_percent"]
            #     surprise_amount = event["data"]["change_amount"]
                # print(f"Symbol: {symbol} - Actual EPS: {actual_eps} - Estimated EPS: {estimated_eps} - Surprise Percent: {surprise_percent} - Surprise Amount: {surprise_amount}")
        return earnings_dates
    
    def load_or_fetch_conids_for_symbols(self, symbols: list[str]) -> list[int]:
        conids_file_path = self.config["conids_file_path"]
        if not os.path.exists(conids_file_path):
            return self.fetch_contractIds_of_symbols(symbols)
        data_cache = pd.read_csv(conids_file_path)
        conids = []
        for symbol in symbols:
            conid = data_cache[data_cache["symbol"] == symbol]["conid"].values[0]
            conids.append(conid)
        return conids

    def fetch_contractIds_of_symbols(self, symbols: list[str]) -> list[int]:
        conids = []
        for symbol in symbols:
            self._init_async_flags_and_results(func_name="ContractDetails")
            contract = Contract()
            contract.symbol = symbol
            contract.secType = "STK"
            contract.exchange = "SMART"
            contract.currency = "USD"
            contract.primaryExchange = "NASDAQ"
            try:
                self.reqContractDetails(self.getNextValidId(), contract)
                contract_details: ContractDetails = self._await_get_future_return(func_name="ContractDetails")
                conid = int(contract_details.contract.conId)
                print(f"Symbol: {symbol} - Conid: {conid}")
            except Exception as e:
                print(f"Error fetching contract details for symbol: {symbol} - Error: {e}")
                conid = None
            conids.append(conid)
        return conids
    
    def fetch_contractId_of_Any(self, key: str) -> int:
        self._init_async_flags_and_results(func_name="ContractDetails")
        contract = Contract()
        contract.symbol = key
        # contract.secType = "STK"
        # contract.exchange = "SMART"
        # contract.currency = "USD"
        # contract.primaryExchange = "NASDAQ"
        try:
            self.reqContractDetails(self.getNextValidId(), contract)
            contract_details: ContractDetails = self._await_get_future_return(func_name="ContractDetails")
            if isinstance(contract_details, list):
                conids = [int(contract_details[i].contract.conId) for i in range(len(contract_details))]
            else:
                conids = int(contract_details.contract.conId)
            print(f"Key: {key} - Conid: {conids}")
        except Exception as e:
            print(f"Error fetching contract details for key: {key} - Error: {e}")
            conids = None
        return conids
    
    def fetch_last_closing_price_of(self, symbol: str) -> float:
        contract = Contract()
        contract.symbol = symbol
        contract.secType = "STK"
        contract.exchange = "SMART"
        contract.currency = "USD"
        contract.primaryExchange = "NASDAQ"

        self._init_async_flags_and_results(func_name="CurrentPrice")
        self.reqMarketDataType(3)  # Request delayed data
        # https://ibkrcampus.com/campus/ibkr-api-page/twsapi-doc/#available-tick-types
        self.reqMktData(self.getNextValidId(), contract, "", False, False, [])
        current_price = self._await_get_future_return(func_name="CurrentPrice")
        return current_price
    
    def fetch_segment_performance(self):
        self._init_async_flags_and_results(func_name="ScannerParameters")
        self.reqScannerParameters()
        market_situation = self._await_get_future_return(func_name="ScannerParameters")
        return market_situation

# MARK: - Private
    
    def _connect_to_server(self):
        host = "127.0.0.1"
        port = 7496 if self.config["is_using_real_account"] else 7497
        clientId = 0
        try:
            self.connect(host, port, clientId)
            return True
        except Exception as e:
            print(f"Error connecting to server: {e}. Running without TWS.")
            return False

    def _await_get_future_return(self, func_name: str):
        assert func_name in self.async_flags
        flag= self.async_flags[func_name]
        start_time = time.time()
        timeout = 10
        while not flag.is_set() and time.time() - start_time < timeout:
            sleep(0.1)
        # if time out, return None
        if not flag.is_set():
            return None
        assert func_name in self.async_results
        return self.async_results[func_name]

    def _init_async_flags_and_results(self, func_name: str):
        with self.lock:
            self.async_flags[func_name] = Event()
            self.async_results[func_name] = None

    def _get_wall_street_horizon_meta_data(self):
        reqId = self.nextId()
        self.reqWshMetaData(reqId)
        # future = self.wrapper.startReq(reqId, container='')
        # await future
        # return future.result()

    def _get_wall_street_horizon(self):
        eventDataObject = WshEventData(
            eventType = "WALL_STREET_HORIZON",
            conid = 123456,
            period = "10 S",
            barSize = "TRADES",
            startDateTime = "20250101",
            endDateTime = "20250201"
        )
        # self.reqWshEventData(1101, eventDataO)

    def _scan_market(self):
        sub = ScannerSubscription()
        sub.instrument = "STK"
        sub.locationCode = "STK.US.MAJOR"
        subscanCode = "TOP_OPEN_PERC_GAIN"

        scan_options = []
        filter_options = [
            TagValue("volumeAbove", "10000"),
            TagValue("marketCapBelow1e6", "1000"),
            TagValue("priceAbove", '1')
        ]

        self.reqScannerSubscription(self.getNextValidId(), sub, scan_options, filter_options)

# MARK: - Officially Required Methods

    # def start(self):
    #     self.reqAccountUpdates(True, "")

    # def stop(self):
    #     self.reqAccountUpdates(False, "")
    #     self.done = True
    #     self.disconnect()

    def nextValidId(self, first_available_id_for_this_session: int):
        self.nextId = first_available_id_for_this_session

    def getNextValidId(self):
        self.nextId += 1
        return self.nextId
    
    def currentTime(self, time):
        print(f"Current time: {time}")
    
    def error(self, reqId, errorCode, errorString, advancedOrderReject, not_important):
        print(f"Error: errorCode: {errorCode} - errorString: {errorString}, advancedOrderReject: {advancedOrderReject}")
        if f"{errorCode}" == "1744871908388":
            raise ValueError("Connection to TWS is lost. Please check your TWS connection.")
    # call back functions for orders

    def openOrder(self, orderId: OrderId, contract: Contract, ib_order: Order, ib_orderState: OrderState):
        print(f"Open order: {orderId} - {contract} - {ib_order} - {ib_orderState}")
        # custom_order = CustomOrder.from_ib(contract, ib_order)
        # with self.lock:
        #     self.async_results["OpenOrder"] = custom_order
        #     assert "OpenOrder" in self.async_flags, f"OpenOrder not in async_flags: {self.async_flags}. Forgot to call _init_async_flags_and_results?"
        #     self.async_flags["OpenOrder"].set()

    def orderStatus(self, orderId: OrderId, status: str, filled: float, remaining: float, avgFillPrice: float, permId: int, parentId: int, lastFillPrice: float, clientId: int, whyHeld: str, mktCapPrice: float):
        # print(f"Order status: {orderId} - {status} - {filled} - {remaining} - {avgFillPrice} - {permId} - {parentId} - {lastFillPrice} - {clientId} - {whyHeld} - {mktCapPrice}")
        pass

    def execDetails(self, reqId: int, contract: Contract, execution: Execution):
        # print(f"Exec details: {reqId} - {contract} - {execution}")
        pass

    # call back functions for positions

    def position(self, account: str, contract: Contract, position: float, avgCost: float):
        print(f"Position: {account} - {contract} - {position} - {avgCost}")
        with self.lock:
            symbol: str = contract.localSymbol
            position_dict = {
                symbol: CustomPosition(symbol, position, avgCost)
            }
            if "Position" not in self.async_results or self.async_results["Position"] is None:
                self.async_results["Position"] = position_dict
            else:
                self.async_results["Position"].update(position_dict)
            assert "Position" in self.async_flags, f"Position not in async_flags: {self.async_flags}. Forgot to call _init_async_flags_and_results?"
            self.async_flags["Position"].set()

    # call back functions for portforlio
    # refer to https://www.youtube.com/watch?v=TWzITCzRN7k&list=PL71vNXrERKUpPreMb3z1WGx6fOTCzMaH1&index=9

    def updatePortfolio(self, contract: Contract, position: float, marketPrice: float, marketValue: float, averageCost: float, unrealizedONL: float, realizedPNL: float, accountName: str):
        print(f"Update portfolio: {contract} - {position} - {marketPrice} - {marketValue} - {averageCost} - {unrealizedONL} - {realizedPNL} - {accountName}")

    def updateAccountValue(self, key: str, value: str, currecny: str, accountName: str):
        print(f"Update account value: {key} - {value} - {currecny} - {accountName}")

    def updateAccountTime(self, timeStamp: str):
        print(f"Update account time: {timeStamp}")

    def accountDownloadEnd(self, accountName: str):
        print(f"Account download end: {accountName}")

    # call back functions for scanner parameters

    def scannerParameters(self, xml):
        print(f"Scanner parameters: {xml}")
        # Convert XML to a dictionary
        xml_dict = xmltodict.parse(xml)
        # Convert the dictionary to YAML
        yaml_data = yaml.dump(xml_dict, default_flow_style=False)
        # Save the YAML data to a file
        with open(os.path.join(self.config["temp_data_folder_path"], "scanner_parameters.yaml"), "w", encoding="utf-8") as yaml_file:
            yaml_file.write(yaml_data)

        # extract the "scanCode:" field from the it and collect them, and save them to a file
        scan_codes = []
        with open(os.path.join(self.config["temp_data_folder_path"], "scanner_parameters.yaml"), "r", encoding="utf-8") as file:
            txt = file.read()
        for item in txt.split("\n"):
            if "scanCode:" in item.replace(" ", ""):
                scan_codes.append(item.split("scanCode:")[1].strip())

        with open(os.path.join(self.config["temp_data_folder_path"], "scanner_codes.yaml"), "w", encoding="utf-8") as yaml_file:
            yaml_file.write(yaml.dump(scan_codes))

    def scannerData(self, reqId, rank, contractDetails, distance, benchmark, projection, legsStr):
        print(f"Scanner data: {reqId} - {rank} - {contractDetails} - {distance} - {benchmark} - {projection} - {legsStr}")

    def scannerDataEnd(self, reqId):
        print(f"ScannerDataEnd reqId: {reqId}")
        self.cancelScannerSubscription(reqId)

    # call back functions for wsh event data

    def wshMetaData(self, reqId, data):
        data = json.loads(data)
        with self.lock:
            self.async_results["WshMetaData"] = data
            assert "WshMetaData" in self.async_flags, f"WshMetaData not in async_flags: {self.async_flags}. Forgot to call _init_async_flags_and_results?"
            self.async_flags["WshMetaData"].set()
        # event_types = data['meta_data']["event_types"]
        # filters = data['meta_data']["filters"]
        # print(f"Wall Street Horizon Meta Data: {data}")

    def wshEventData(self, reqId, data):
        data = json.loads(data)
        with self.lock:
            self.async_results["WshEventData"] = data
            assert "WshEventData" in self.async_flags, f"WshEventData not in async_flags: {self.async_flags}. Forgot to call _init_async_flags_and_results?"
            self.async_flags["WshEventData"].set()
        # print(f"WSH Event Data: {data}")

    # call back functions for contract details

    def contractDetails(self, reqId, contractDetails: ContractDetails):
        with self.lock:
            self.async_results["ContractDetails"] = contractDetails
            assert "ContractDetails" in self.async_flags, f"ContractDetails not in async_flags: {self.async_flags}. Forgot to call _init_async_flags_and_results?"
            self.async_flags["ContractDetails"].set()
        # print(f"Contract Details: {contractDetails}")

    # call back functions for market data

    def tickPrice(self, reqId: int, tickType: int, price: float, attrib: TickAttrib):
        if int(tickType) != 75: # skip other than last close price tick types
            return
        # print(f"Tick price: {reqId} - {tickType} - {price} - {attrib}")
        # Handle the tick price update here
        with self.lock:
            self.async_results["CurrentPrice"] = float(price)
            assert "CurrentPrice" in self.async_flags, f"CurrentPrice not in async_flags: {self.async_flags}. Forgot to call _init_async_flags_and_results?"
            self.async_flags["CurrentPrice"].set()

    # call back functions for market scanner

if __name__ == "__main__":
    tws = IBTwsAPIHandler()
    tws.async_run()

    tws._get_wall_street_horizon_meta_data()

