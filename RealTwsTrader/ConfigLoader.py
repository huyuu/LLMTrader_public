import yaml
import platform
import os
from datetime import datetime, timedelta
import subprocess
import pytz
import warnings
import pandas as pd
from multiprocessing import Event

class ConfigLoader:
    config_cls = None
    project_root_path = os.path.dirname(os.path.abspath(__file__))
    config_general_file_path = f"{project_root_path}/config_general.yaml"
    # set absolute current time and date in eastern timezone
    eastern = pytz.timezone('America/New_York')  # GMT-5 timezone
    absolute_current_time_in_eastern_cls = datetime.now(eastern).replace(tzinfo=None)
    absolute_current_date_in_eastern_cls = datetime(
        year=absolute_current_time_in_eastern_cls.year, 
        month=absolute_current_time_in_eastern_cls.month, 
        day=absolute_current_time_in_eastern_cls.day
    )
    # set absolute current time and date in UTC timezone
    absolute_current_time_in_utc_cls = datetime.now(pytz.utc).replace(tzinfo=None)
    absolute_current_date_in_utc_cls = datetime(
        year=absolute_current_time_in_utc_cls.year, 
        month=absolute_current_time_in_utc_cls.month, 
        day=absolute_current_time_in_utc_cls.day
    )
    # set absolute current time and date in JPT timezone
    absolute_current_time_in_jpt_cls = datetime.now(pytz.timezone('Asia/Tokyo')).replace(tzinfo=None)
    absolute_current_date_in_jpt_cls = datetime(
        year=absolute_current_time_in_jpt_cls.year, 
        month=absolute_current_time_in_jpt_cls.month, 
        day=absolute_current_time_in_jpt_cls.day
    )
    # set common properties
    green_color_code = "\033[92m"
    red_color_code = "\033[91m"
    yellow_color_code = "\033[93m"
    reset_color_code = "\033[0m"

    def __init__(self):
        if ConfigLoader.config_cls is None:
            ConfigLoader.load_config()
    
    @property
    def absolute_current_time_in_eastern(self):
        return ConfigLoader.absolute_current_time_in_eastern_cls

    @property
    def absolute_current_date_in_eastern(self):
        return ConfigLoader.absolute_current_date_in_eastern_cls

    @property
    def absolute_current_time_in_utc(self):
        return ConfigLoader.absolute_current_time_in_utc_cls

    @property
    def absolute_current_date_in_utc(self):
        return ConfigLoader.absolute_current_date_in_utc_cls
    
    @property
    def absolute_current_date_in_jpt(self):
        return ConfigLoader.absolute_current_date_in_jpt_cls

    # this @property is needed to dynamically access the config_cls
    @property
    def config(self):
        return ConfigLoader.config_cls

    @classmethod
    def load_config(cls):
        with open(cls.config_general_file_path, "r") as file:
            cls.config_cls = yaml.safe_load(file)
            cls.config_cls["active_data_folder_path"] = f"{os.path.join(cls.project_root_path, 'activeData')}"
            if not os.path.exists(cls.config_cls["active_data_folder_path"]):
                os.makedirs(cls.config_cls["active_data_folder_path"])
            cls.config_cls["archieve_data_folder_path"] = f"{os.path.join(cls.project_root_path, 'archieveData')}"
            if not os.path.exists(cls.config_cls["archieve_data_folder_path"]):
                os.makedirs(cls.config_cls["archieve_data_folder_path"])
            cls.config_cls["nasdaq_tickers_file_path"] = f"{os.path.join(cls.config_cls['active_data_folder_path'], cls.config_cls['nasdaq_tickers_file_name'])}"
            cls.config_cls["nasdaq_financial_report_release_dates_file_path"] = f"{os.path.join(cls.config_cls['active_data_folder_path'], cls.config_cls['nasdaq_financial_report_release_dates_file_name'])}"
            cls.config_cls["market_open_dates_file_path"] = f"{os.path.join(cls.config_cls['active_data_folder_path'], cls.config_cls['market_open_dates_file_name'])}"
            cls.config_cls["temp_data_folder_path"] = f"{os.path.join(cls.project_root_path, 'tempData')}"
            if not os.path.exists(cls.config_cls["temp_data_folder_path"]):
                os.makedirs(cls.config_cls["temp_data_folder_path"])
            cls.config_cls["financial_report_download_folder_path"] = f"{os.path.join(cls.config_cls['active_data_folder_path'], 'financial_reports_original_download')}"
            if not os.path.exists(cls.config_cls["financial_report_download_folder_path"]):
                os.makedirs(cls.config_cls["financial_report_download_folder_path"])
            cls.config_cls["financial_report_extracted_text_cache_folder_path"] = f"{os.path.join(cls.config_cls['active_data_folder_path'], 'financial_reports_extracted_text_cache')}"
            if not os.path.exists(cls.config_cls["financial_report_extracted_text_cache_folder_path"]):
                os.makedirs(cls.config_cls["financial_report_extracted_text_cache_folder_path"])

            cls.config_cls["should_continue_from_last_result"] = not cls.config_cls["should_clear_temp_data_before_trade"]

            cls.config_cls["large_scale_close_loop_sim_symbols_file_path"] = os.path.join(cls.config_cls["active_data_folder_path"], cls.config_cls["close_loop_sim_symbols_file_name"])

            cls.config_cls["ib_tws_api_handler_class_name"] = "IBTwsAPIHandler"

            cls.config_cls["conids_file_path"] = os.path.join(cls.config_cls["active_data_folder_path"], "conids_for_symbols.csv")

            # update real_trader_using_prediction_folder_name:
            if cls.config_cls["real_trader_using_prediction_folder_name"] == 'tempData':
                cls.config_cls["real_trader_using_prediction_folder_path"] = cls.config_cls["temp_data_folder_path"]
            else:
                cls.config_cls["real_trader_using_prediction_folder_path"] = os.path.join(cls.config_cls["archieve_data_folder_path"], cls.config_cls["real_trader_using_prediction_folder_name"])

            cls.config_cls["large_scale_close_loop_sim_history_data_folder_path"] = os.path.join(cls.config_cls["archieve_data_folder_path"], cls.config_cls["large_scale_close_loop_sim_history_data_folder_name"])

            cls.config_cls["history_earnings_calendar_file_path"] = os.path.join(cls.config_cls["active_data_folder_path"], "history_earnings_calendar_from_ib_cache.csv")

            cls.config_cls["proxy_list_path"] = os.path.join(cls.config_cls["active_data_folder_path"], "proxy_list.yaml")

            cls.config_cls["agents_cache_folder"] = os.path.join(cls.config_cls["active_data_folder_path"], "agents_cache")
            if not os.path.exists(cls.config_cls["agents_cache_folder"]):
                os.makedirs(cls.config_cls["agents_cache_folder"])
        
            cls.config_cls["absolute_earliest_referred_date"] = datetime.strptime(cls.config_cls["trade_start_date"], "%Y-%m-%d") - timedelta(days=365)

            cls.config_cls["sp500_cache_folder"] = os.path.join(cls.config_cls["active_data_folder_path"], "sp500_cache")
            if not os.path.exists(cls.config_cls["sp500_cache_folder"]):
                os.makedirs(cls.config_cls["sp500_cache_folder"])


    def update_submodule(self, submodule: str):
        """
        Updates the submodule at the given path by pulling the latest changes from the tracked branch.

        :param submodule_path: The relative path to the submodule directory.
        """
        try:
            folder_path = os.path.join("submodules", submodule)
            if not os.path.exists(folder_path):
                os.mkdir(folder_path)

            # Ensure the submodule is updated to track the specified branch
            subprocess.run(["git", "submodule", "update", "--init", "--recursive", "--remote", f"submodules/{submodule}"], check=True)

            print(f"Successfully updated submodule at '{folder_path}'.")
        except subprocess.CalledProcessError as e:
            print(f"Error occurred while updating submodule '{folder_path}': {e}")
            print("Using cache data instead.")

    @classmethod
    def set_terminate_signal(cls):
        cls.config_cls["should_terminate"].set()

    def save_to_yaml(self, data, file_path, append=False):
        # Save data to a YAML file
        mode = 'a' if append else 'w'
        with open(file_path, mode) as file:
            yaml.dump(data, file)

    @classmethod
    def convert_to_datetime(cls, pdSeries: pd.Series, unit: str=None):
        with warnings.catch_warnings():
            warnings.simplefilter(action='ignore', category=FutureWarning)
            if unit is None:
                return pd.to_datetime(pdSeries, format='mixed').dt.to_pydatetime()
            else:
                return pd.to_datetime(pdSeries, unit=unit).dt.to_pydatetime()

    def get_file_last_update_date(self, file_path: str) -> datetime:
        """
        Returns the last modification date of the earnings calendar CSV file.
        
        Returns:
            datetime: The last modification date of the file, or None if the file doesn't exist.
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        # Get the last modification time as a timestamp
        mod_time = os.path.getmtime(file_path)
        # Convert timestamp to datetime object
        last_update = datetime.fromtimestamp(mod_time)
        return last_update


    def distribute_ids_to_threads(self, ids, num_threads: int) -> list[list[str]]:
        if num_threads == 1:
            return [ids]
        # Distribute symbols into groups
        num_threads = min(num_threads, len(ids))
        groups = []
        amount_of_symbols_per_group = len(ids) // num_threads
        # adjustment
        if (num_threads-1) * (amount_of_symbols_per_group + 1) < len(ids):
            amount_of_symbols_per_group += 1
        for i in range(num_threads):
            if i == num_threads - 1: # for the last group, add the remaining symbols
                group = ids[i * amount_of_symbols_per_group:]
            else:
                group = ids[i * amount_of_symbols_per_group:(i + 1) * amount_of_symbols_per_group]
            groups.append(group)
        return groups