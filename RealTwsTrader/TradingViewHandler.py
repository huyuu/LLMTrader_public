from ConfigLoader import ConfigLoader
import requests
import pandas as pd
import numpy as np
import yfinance as yf
import urllib3
from datetime import datetime
from fake_useragent import UserAgent
import asyncio
from playwright.async_api import async_playwright
import json

class TradingViewHandler(ConfigLoader):
    def __init__(self):
        super().__init__()
        # Modify the session to not verify SSL
        self.session = requests.Session()
        self.session.verify = False
        yf.shared._session = self.session

        self.ssl_session = requests.Session()
        self.ssl_session.verify = True

        # Disable InsecureRequestWarning
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    def home_made_fetch(self, symbol: str, period: str="max", should_use_proxy: bool=False) -> pd.DataFrame:
        url = f"https://yfapi.net/v6/finance/quote?symbols={symbol}"

        response = requests.get(url)
        return response.json()
    

    async def _fetch_with_playwright(self, url, headers=None):
        """Fetch URL using Playwright browser automation."""
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context(
                user_agent=headers.get("User-Agent") if headers and "User-Agent" in headers else UserAgent().random,
                viewport={"width": 1920, "height": 1080}
            )
            
            page = await context.new_page()
            
            try:
                await page.goto(url, wait_until="networkidle", timeout=30000)
                await page.wait_for_timeout(1000)
                
                # Extract the JSON data from the pre-rendered HTML
                content = await page.content()
                
                json_text = self.extract_chart_json(content)
                
                await browser.close()
                return json_text
            except Exception as e:
                print(f"Playwright error: {e}")
                await browser.close()
                return None

    def _fetch_html(self, url, headers=None):
        """Retrieve HTML content using Playwright."""
        try:
            return asyncio.run(self._fetch_with_playwright(url, headers))
        except Exception as e:
            print(f"Error fetching the page: {e}")
            return None

    def fetch_history_data_of(self, symbol: str, period: str="max", from_date: datetime=None, to_date: datetime=None) -> pd.DataFrame:
        # special case symbols
        if symbol == "BRK.B":
            symbol = "BRK-B"
        if symbol == "BF.B":
            symbol = "BF-B"
        # Use the session without the proxy
        # data = yf.download(symbol, interval='1d', progress=False, period=period, session=self.session, auto_adjust=True)
        headers = {"User-Agent": UserAgent().random}
        # symbol_ticker = yf.Ticker(symbol, session=self.session, headers=headers)
        # data = symbol_ticker.history(period=period, interval='1d')

        # yfinance_url = "https://query2.finance.yahoo.com/v8/finance/chart/SPY?period1=946702800&period2=1606798800&interval=1d&events=history"
        # response = requests.get(yfinance_url, headers=headers)
        # data = response.json()
        # if data is None or data.empty:
        #     print(f"Error fetching {symbol} data: {data}")
        
        # Construct the Yahoo Finance URL with the appropriate parameters
        # We'll use from_date and to_date if provided
        if from_date is None:
            from_date = datetime(2020, 1, 1)  # Default to year 2000
        if to_date is None:
            to_date = datetime.now()
            
        period1 = int(from_date.timestamp())
        period2 = int(to_date.timestamp())
        
        yfinance_url = f"https://query2.finance.yahoo.com/v8/finance/chart/{symbol}?period1={period1}&period2={period2}&interval=1d&events=history"
        
        # Use Playwright to get the data
        response_data = self._fetch_html(yfinance_url, headers)
        
        if not response_data or 'chart' not in response_data or response_data['chart']['result'] is None:
            print(f"Error fetching {symbol} data: No valid data returned")
            return None
            
        # Extract the chart data
        chart_data = response_data['chart']['result'][0]
        
        # Create a dataframe
        timestamps = chart_data['timestamp']
        quote = chart_data['indicators']['quote'][0]
        
        data = pd.DataFrame({
            'Date': pd.to_datetime(timestamps, unit='s'),
            'Open': quote['open'],
            'Low': quote['low'],
            'High': quote['high'],
            'Close': quote['close'],
            'Volume': quote['volume']
        })
        
        # Reset index to include the date
        data.reset_index(inplace=True)
        
        # convert datetime to naive datetime
        data.loc[:, 'date'] = data['Date'].dt.tz_localize(None)

        # Extract necessary columns
        df = data[['date', 'Open', 'Low', 'High', 'Close', 'Volume']]
        df.columns = ['date', 'open', 'low', 'high', 'close', 'volume']
        df.loc[:, 'date'] = pd.to_datetime(df['date']).dt.floor('D')
        df = df.sort_values('date').reset_index(drop=True)
        # add daily_volatility
        df.loc[:, 'daily_volatility_percentage'] = df.apply(lambda row: (row['high'] - row['low']) / row['close'] * 100 if row['close'] is not None and row['close'] != 0 else pd.NA, axis=1)
        # add 20 day moving average of close price
        df.loc[:, '20_days_moving_average_of_close_price'] = df['close'].rolling(window=20).mean()
        # add 60 day moving average of close price
        df.loc[:, '60_days_moving_average_of_close_price'] = df['close'].rolling(window=60).mean()
        # add 20 day moving average of volume
        df.loc[:, '20_days_moving_average_of_volume'] = df['volume'].rolling(window=20).mean()
        # add 60 day moving average of volume
        df.loc[:, '60_days_moving_average_of_volume'] = df['volume'].rolling(window=60).mean()

        if from_date is not None:
            df = df.loc[df['date'] >= from_date, :]
        if to_date is not None:
            df = df.loc[df['date'] <= to_date, :]
        return df

    @classmethod
    def calculate_volume_profile_of(cls, symbol: str, data_original: pd.DataFrame=None) -> pd.DataFrame:
        # if data is None:
        #     data = self.fetch_history_data_of(symbol)
        data = data_original.copy()

        # Define price bin width (e.g., $0.50)
        bin_width = 0.5

        # Calculate the range of bins
        min_price = data['low'].min()
        max_price = data['high'].max()
        bins = np.arange(min_price, max_price + bin_width, bin_width)

        # Assign each 'close' price to a bin
        data.loc[:, 'price_bin'] = pd.cut(data['close'], bins)

        # Sum the volume for each price bin; need to set observed=False to retain the bins even if they are of zero volume
        volume_profile = data.groupby('price_bin', observed=False)['volume'].sum()

        # Clean up the index for better visualization
        volume_profile.index = volume_profile.index.astype(str)

        # add volume profile standard deviation
        volume_profile_std = volume_profile.std()

        return volume_profile, volume_profile_std


    @classmethod
    def calculate_volume_profile_transition_of(cls, symbol: str, data: pd.DataFrame) -> pd.DataFrame:
        if len(data) == 0:
            return None
        
        volume_profile_transition: dict[datetime, pd.DataFrame] = {}
        volume_profile_deviation_transition: dict[datetime, pd.DataFrame] = {}
        for index in data.index:
            date = data.loc[index, 'date']
            filtered_data = data.loc[data['date'] <= date, :]
            if len(filtered_data) == 0:
                continue

            volume_profile, volume_profile_deviation = cls.calculate_volume_profile_of(symbol, filtered_data)
            volume_profile_transition[date] = volume_profile
            volume_profile_deviation_transition[date] = volume_profile_deviation

        return volume_profile_transition, volume_profile_deviation_transition
    
    @classmethod
    def calculate_volume_profile_avg_and_std_transition_of(cls, symbol: str, data: pd.DataFrame) -> pd.DataFrame:
        if len(data) == 0:
            return None
        
        return_data: pd.DataFrame = pd.DataFrame()
        for index in data.index[-cls.config_cls["n_days_data_fed_to_volume_profile_handler"]:]:
            date = data.loc[index, 'date']
            filtered_data = data.loc[data['date'] <= date, :]
            if len(filtered_data) == 0:
                continue

            volume_profile, volume_profile_deviation = cls.calculate_volume_profile_of(symbol, filtered_data)
            if len(return_data) == 0:
                return_data = pd.DataFrame({"date": [date], "volume_profile_average_value": [volume_profile.mean()], "volume_profile_standard_deviation": [volume_profile.std()]})
            else:
                return_data = pd.concat([return_data, pd.DataFrame({"date": [date], "volume_profile_average_value": [volume_profile.mean()], "volume_profile_standard_deviation": [volume_profile.std()]})], ignore_index=True)
        return_data.sort_values(by='date', inplace=True)
        return_data.set_index('date', inplace=True, drop=True)
        return return_data
    
    @classmethod
    def calculate_volume_profile_transition_of(cls, symbol: str, data: pd.DataFrame) -> pd.DataFrame:
        if len(data) == 0:
            return None
        
        filtered_data = data.iloc[-cls.config_cls["n_days_data_fed_to_volume_profile_handler"]:, :]
        if len(filtered_data) == 0:
            return None
        
        volume_profile, volume_profile_deviation = cls.calculate_volume_profile_of(symbol, filtered_data)
        return volume_profile
            
            
    @staticmethod
    def extract_chart_json(html: str) -> dict:
        """
        Return the first valid JSON object that starts with {"chart": ... }.

        Parameters
        ----------
        html : str
            Raw HTML (or any text) containing the JSON block.

        Returns
        -------
        dict
            Parsed JSON as a Python dict.

        Raises
        ------
        ValueError
            If no valid JSON block is found.
        """
        # 1. Find the substring that looks like {"chart": ... }.
        #    We assume there are no unmatched braces *inside* strings.
        open_brace = html.find('{"chart":')
        if open_brace == -1:
            raise ValueError("No “{\"chart\":” prefix found.")

        depth = 0
        for idx in range(open_brace, len(html)):
            char = html[idx]
            if char == '{':
                depth += 1
            elif char == '}':
                depth -= 1
                if depth == 0:
                    json_blob = html[open_brace:idx + 1]
                    break
        else:  # for-loop finished without finding a closing brace
            raise ValueError("Unbalanced braces – JSON block is incomplete.")

        # 2. Parse the blob into a dict.
        return json.loads(json_blob)