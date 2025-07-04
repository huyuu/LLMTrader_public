from ConfigLoader import ConfigLoader
import numpy as np
class CustomPosition(ConfigLoader):
    def __init__(self, symbol: str, amount: float, avgCost: float):
        self.symbol = symbol
        self.amount = np.abs(amount)
        self.avgCost = avgCost
        self.is_long = amount >= 0

    def __str__(self):
        return f"CustomPosition: {self.symbol} - {self.position} - {self.avgCost}, is_long: {self.is_long}"

