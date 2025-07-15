from ConfigLoader import ConfigLoader
from IBTwsAPIHandler import IBTwsAPIHandler
import pandas as pd
import os
from time import sleep
import numpy as np
from CustomOrder import CustomOrder, CustomOrder_Market_Buy, CustomOrder_Market_Sell, CustomOrder_Market_On_Close_Buy, CustomOrder_Market_On_Close_Sell


class RealTrader(ConfigLoader):
    def __init__(self):
        super().__init__()
        self.ib_tws_api_handler = IBTwsAPIHandler()
        self.ib_tws_api_handler.async_run()

    def run(self):
        file_name = self.config["real_trader_using_prediction_file_name"]
        project_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        file_path = os.path.join(project_path, "activeData", "predictions", file_name)
        if os.path.exists(file_path):
            data = pd.read_csv(file_path)
        else:
            print(f"file {file_path} does not exist, are you sure you just want to file cancel all orders request?")
            data = pd.DataFrame()

        self._conduct_simple_strategy(data)
        

# MARK: - Private

    def _conduct_simple_strategy(self, entry_data: pd.DataFrame):
        # step4: close all the previsouly opened orders
        # symbols_to_exit = exit_data.loc[(exit_data["prediction [%]"] >= 4.0) | (exit_data["prediction [%]"] < 0.0), :]["symbol"].unique().tolist()
        self.ib_tws_api_handler.cancel_all_open_orders()
        # self.ib_tws_api_handler.post_exit_positions(symbols_to_exit)
        self.ib_tws_api_handler.post_exit_all_positions()

        if entry_data is None or len(entry_data) == 0:
            print("no data to enter, just close all positions and exit")
            self.ib_tws_api_handler.cancel_all_open_orders()
            self.ib_tws_api_handler.post_exit_all_positions()
            return

        # step1: get the symbols to enter today
        entry_data = entry_data.loc[(entry_data["prediction [%]"] >= self.config["long_odds_threshold"]) | (entry_data["prediction [%]"] < self.config["short_odds_threshold"]), :]
        symbols_to_enter = entry_data["symbol"].unique().tolist()
        amount_of_symbols = len(symbols_to_enter)

        # step2: fetch balance
        total_asset = self.config["real_trader_asset_USD"] # USD

        # step4: tyr fetch the current price of the symbols
        symbols_last_closing_price = {}
        for index, row in entry_data.iterrows():
            symbol = row["symbol"]
            if symbol in self.config["symbols_to_avoid"]:
                continue
            # get the current price of the symbol
            current_price = self.ib_tws_api_handler.fetch_last_traded_price_of(symbol)
            if current_price is None:
                continue
            symbols_last_closing_price[symbol] = current_price
        # update symbols_to_enter to only include symbols that have current price
        symbols_to_enter = list(filter(lambda symbol: symbol in symbols_last_closing_price, symbols_to_enter))
        amount_of_symbols = len(symbols_to_enter)

        actual_investment_sum = 0

        # step5: open new orders for the symbols set to entry at close today
        for index, row in entry_data.iterrows():
            symbol = row["symbol"]
            if symbol not in symbols_last_closing_price:
                continue
            # get the current price of the symbol
            current_price = symbols_last_closing_price[symbol]
            # calculate the amount of asset to buy
            investment_for_this_symbol = total_asset * row["kelly_fraction [%]"] / 100
            amount_of_asset = np.floor(investment_for_this_symbol / current_price)
            if amount_of_asset == 0:
                continue
            actual_investment_sum += amount_of_asset * current_price
            prediction = row["prediction [%]"]
            if prediction > 0:
                self.ib_tws_api_handler.post_new_order(CustomOrder_Market_On_Close_Buy(
                    symbol=symbol,
                    amount=amount_of_asset
                ))
            else:
                self.ib_tws_api_handler.post_new_order(CustomOrder_Market_On_Close_Sell(
                    symbol=symbol,
                    amount=amount_of_asset
                ))

        print(f"actual investment : {actual_investment_sum / total_asset * 100} %")
        sleep(5)
        exit(0)
            
    
if __name__ == "__main__":
    trader = RealTrader()
    trader.run()
    