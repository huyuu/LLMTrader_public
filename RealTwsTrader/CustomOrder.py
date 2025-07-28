from ConfigLoader import ConfigLoader

class CustomOrder(ConfigLoader):
    def __init__(self, symbol: str, price: float, amount: float, type: str, action: str, expiration: str, orderId: int=None):
        super().__init__()
        self.symbol: str = symbol
        self.price: float = price
        self.amount: float = amount
        self.action: str = action
        self.type: str = type
        self.expiration: str = expiration
        self.orderId: int = orderId

    @classmethod
    def from_ib(cls, contract, ib_order):
        symbol = contract.localSymbol
        type = ib_order.orderType
        action = ib_order.action
        expiration = ib_order.tif
        amount = ib_order.totalQuantity.real
        if type == "LMT":
            price = ib_order.lmtPrice
        else:
            price = None
        orderId = ib_order.orderId
        return cls(symbol, price, amount, type, action, expiration, orderId)
    
    
class CustomOrder_Limit_Buy(CustomOrder):
    def __init__(self, symbol: str, price: float, amount: float):
        super().__init__(symbol, price, amount, "LMT", "BUY", "GTC")

class CustomOrder_Limit_Sell(CustomOrder):
    def __init__(self, symbol: str, price: float, amount: float):
        super().__init__(symbol, price, amount, "LMT", "SELL", "GTC")


class CustomOrder_Market_Buy(CustomOrder):
    def __init__(self, symbol: str, amount: float):
        super().__init__(symbol, None, amount, "MKT", "BUY", "DAY")

class CustomOrder_Market_Sell(CustomOrder):
    def __init__(self, symbol: str, amount: float):
        super().__init__(symbol, None, amount, "MKT", "SELL", "DAY")

class CustomOrder_Market_Buy_On_Open(CustomOrder):
    def __init__(self, symbol: str, amount: float):
        super().__init__(symbol, None, amount, "MKT", "BUY", "OPG")

class CustomOrder_Market_Sell_On_Open(CustomOrder):
    def __init__(self, symbol: str, amount: float):
        super().__init__(symbol, None, amount, "MKT", "SELL", "OPG")

class CustomOrder_Market_On_Close_Buy(CustomOrder):
    def __init__(self, symbol: str, amount: float):
        super().__init__(symbol, None, amount, "MOC", "BUY", "DAY")

class CustomOrder_Market_On_Close_Sell(CustomOrder):
    def __init__(self, symbol: str, amount: float):
        super().__init__(symbol, None, amount, "MOC", "SELL", "DAY")










