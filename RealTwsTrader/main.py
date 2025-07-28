# This class is designed to automate the prediction process, which follows these steps:
# 1. Change the trade_start_date and trade_end_date in the config_general.yaml file, to yesterday and today respectively in EST timezone
# 2. Open the TWS app
# 3. Execute VirtualTrader.py
# 4. Execute scripts/data_analyze_for_prediction.py
# 5. Execute scripts/RealTrader.py
# 6. Move the tempData folder to the archieveData folder

from ConfigLoader import ConfigLoader
import os
import subprocess
import shutil
from datetime import datetime, timedelta
import platform
from time import sleep
import yaml
import pywinauto
from pywinauto.keyboard import send_keys


class AutomatedPredictor(ConfigLoader):
    def __init__(self):
        super().__init__()
        self._load_tws_credentials()
        
    def _load_tws_credentials(self):
        """Load TWS credentials from config (already loaded from config_confidential.yaml)"""
        try:
            self.tws_username = self.config["ib_id"]
            self.tws_password = self.config["ib_password"]
            
            if not self.tws_username or not self.tws_password:
                print(f"{self.yellow_color_code}Warning: TWS credentials not found in config{self.reset_color_code}")
                self.tws_username = None
                self.tws_password = None
                
        except Exception as e:
            print(f"{self.yellow_color_code}Warning: Could not load TWS credentials: {e}{self.reset_color_code}")
            self.tws_username = None
            self.tws_password = None
        
    def run_automated_prediction(self):
        """
        Execute the automated prediction process following the defined steps.
        """
        try:
            print(f"{self.green_color_code}Starting automated prediction process...{self.reset_color_code}")
            
            # Step 2: Open the TWS application
            print(f"{self.yellow_color_code}Step 2: Opening TWS application...{self.reset_color_code}")
            self._open_tws_app()
            
            # Step 5: Execute scripts/RealTrader.py
            print(f"{self.yellow_color_code}Step 5: Executing RealTrader...{self.reset_color_code}")
            self._execute_real_trader()
            
            print(f"{self.green_color_code}Automated prediction process completed successfully!{self.reset_color_code}")
            
        except Exception as e:
            print(f"{self.red_color_code}Error during automated process: {e}{self.reset_color_code}")
    
    def _open_tws_app(self):
        """
        Opens the TWS (Trader Workstation) application.
        Note: This method depends on the installation and path of TWS on the system.
        """
        try:
            # Typical paths for TWS according to OS
            if platform.system() == "Windows":
                # Typical path on Windows
                tws_paths = [
                    r"C:\\tws\\tws.exe"
                ]
            elif platform.system() == "Darwin":  # macOS
                tws_paths = [
                    "/Applications/Trader Workstation/Trader Workstation.app/Contents/MacOS/Trader Workstation"
                ]
            else:  # Linux
                tws_paths = [
                    os.path.expanduser("~/Jts/tws/tws"),
                    "/opt/tws/tws"
                ]
            
            # Try to find and launch TWS
            tws_launched = False
            for path in tws_paths:
                if os.path.exists(path):
                    print(f"Launching TWS from: {path}")
                    subprocess.Popen([path], shell=True)
                    tws_launched = True
                    break
            
            if not tws_launched:
                print(f"{self.yellow_color_code}Warning: TWS not found at standard locations. Please launch it manually.{self.reset_color_code}")
                print("Checked paths:", tws_paths)
                # Wait for user to launch TWS
                input("Press Enter once TWS is launched and connected...")
            else:
                              
                # Auto-login if credentials are available
                if self.tws_username and self.tws_password:
                    print("Attempting auto-login...")
                    self._auto_login_tws()
                else:
                    input("Please login manually and press Enter once connected...")
                
                # Wait a bit for TWS to launch
                print("Waiting for TWS to launch (120 seconds)...")
                sleep(120)
                
        except Exception as e:
            print(f"{self.yellow_color_code}Warning: Unable to launch TWS automatically: {e}{self.reset_color_code}")
            input("Please launch TWS manually and press Enter once connected...")
    
    def _auto_login_tws(self):
        """Auto-login to TWS using keyboard input"""
        try:
            # Wait a bit more for login dialog to appear
            sleep(30)
            
            # Enter username
            send_keys(self.tws_username)
            sleep(1)
            
            # Tab to password field
            send_keys("{TAB}")
            sleep(1)
            
            # Enter password
            send_keys(self.tws_password)
            sleep(1)
            
            # Press Enter to login
            send_keys("{ENTER}")
            sleep(5)
            
            print(f"{self.green_color_code}Auto-login attempt completed{self.reset_color_code}")
            
        except Exception as e:
            print(f"{self.yellow_color_code}Auto-login failed: {e}{self.reset_color_code}")
            print("Please login manually.")
    
    def _execute_real_trader(self):
        """
        Executes the RealTrader.py script.
        """
        try:
            script_path = os.path.join(self.project_root_path, "RealTrader.py")
            if not os.path.exists(script_path):
                raise FileNotFoundError(f"RealTrader.py not found: {script_path}")
            
            print("Executing RealTrader.py...")
            result = subprocess.run(["python", script_path], cwd=self.project_root_path, timeout=60*5)
            
            if result.returncode != 0:
                raise subprocess.CalledProcessError(result.returncode, "RealTrader.py")
            
            print("RealTrader.py executed successfully")
            
        except subprocess.TimeoutExpired:
            print(f"{self.red_color_code}Timeout: RealTrader.py took more than 10 minutes to execute{self.reset_color_code}")
        except Exception as e:
            print(f"{self.red_color_code}Error executing RealTrader.py: {e}{self.reset_color_code}")
    
def main():
    """
    Main entry point for automated execution.
    """
    predictor = AutomatedPredictor()
    predictor.run_automated_prediction()


if __name__ == "__main__":
    main()
