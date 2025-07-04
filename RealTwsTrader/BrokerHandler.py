import numpy as np
from CustomOrder import CustomOrder
from ConfigLoader import ConfigLoader

class BrokerHandler(ConfigLoader):
    def __init__(self):
        super().__init__()

# MARK: - Basic Functions

    def get_balance(self):
        raise NotImplementedError("get_balance is not implemented")

    def get_open_orders(self):
        raise NotImplementedError("get_open_orders is not implemented")

    def post_new_order(self, order: CustomOrder):
        raise NotImplementedError("post_new_order is not implemented")
    
    def get_order_status(self, order: CustomOrder):
        raise NotImplementedError("get_order_status is not implemented")
    
    def update_order(self, order: CustomOrder):
        raise NotImplementedError("update_order is not implemented")

    def cancel_order(self, order: CustomOrder):
        raise NotImplementedError("cancel_order is not implemented")
    
# MARK: - Advanced Functions

    def calculate_kelly_distributed_symbol(self, symbols_info_list: list) -> np.ndarray:
        winning_probability_list = []
        odds_list = []
        symbol_list = []
        for info in symbols_info_list:
            winning_probability_list.append(info["winning_probability"])
            odds_list.append(info["odds"])
            symbol_list.append(info["symbol"])
        winning_probability_list = np.array(winning_probability_list)
        odds_list = np.array(odds_list)

        # placeholder for kelly
        kelly_fraction_list = (winning_probability_list * odds_list - 1) / odds_list
        kelly_fraction_list_sum = np.sum(kelly_fraction_list)
        if kelly_fraction_list_sum < 1.0:
            kelly_fraction_list = kelly_fraction_list / kelly_fraction_list_sum
        else:
            raise Exception("The sum of kelly fraction is greater than 1.0. Please check the data.")
        return kelly_fraction_list