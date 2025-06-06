import pandas as pd
import os
import glob
from datetime import datetime


class CostCalculator:

    def calculate_costs_for_each_month(self) -> pd.DataFrame:
        """
        Calculate costs for each month from CSV files.
        
        Returns:
            pd.DataFrame: DataFrame with monthly costs, indexed by month, with 'openai' column
        """
        openai_df = self._calculate_openai_cost_for_each_month()
        ib_df = self._calculate_ib_wall_street_horizon_cost_for_each_month()
        misc_df = self._calculate_miscellaneous_expenses_for_each_month()

        # Combine the datasets
        combined_df = pd.merge(openai_df.reset_index(), ib_df, on='month', how='outer')
        combined_df = pd.merge(combined_df, misc_df, on='month', how='outer')
        combined_df = combined_df.set_index('month')
        
        return combined_df


# MARK: - Protected Methods


    def _calculate_openai_cost_for_each_month(self) -> pd.DataFrame:
        """
        Calculate OpenAI costs for each month from CSV files.
        
        Returns:
            pd.DataFrame: DataFrame with monthly costs, indexed by month, with 'openai' column
        """
        # Get all OpenAI cost CSV files
        csv_files = glob.glob("activeData/costs/openai/cost_*.csv")
        
        monthly_costs = {}
        
        for csv_file in csv_files:
            # Extract month from filename (e.g., cost_2025-05-05_2025-05-31.csv)
            filename = os.path.basename(csv_file)
            # Get the start date from filename to determine the month
            start_date_str = filename.split('_')[1]  # e.g., "2025-05-05"
            month_key = start_date_str[:7]  # e.g., "2025-05" (YYYY-MM format)
            
            # Read the CSV file
            try:
                df = pd.read_csv(csv_file)
                
                # Filter out rows with empty amount_value
                df = df.dropna(subset=['amount_value'])
                
                # Sum all costs for this file (which represents one month)
                if not df.empty:
                    total_cost = df['amount_value'].sum()
                    
                    # Add to monthly costs
                    if month_key in monthly_costs:
                        monthly_costs[month_key] += total_cost
                    else:
                        monthly_costs[month_key] = total_cost
                        
            except Exception as e:
                print(f"Error reading {csv_file}: {e}")
                continue
        
        # Convert to DataFrame
        if monthly_costs:
            # Sort by month
            sorted_months = sorted(monthly_costs.keys())
            result_df = pd.DataFrame({
                'openai': [monthly_costs[month] for month in sorted_months]
            }, index=sorted_months)
            result_df.index.name = 'month'
            return result_df
        else:
            # Return empty DataFrame if no data found
            return pd.DataFrame(columns=['openai'])
        

    def _calculate_ib_wall_street_horizon_cost_for_each_month(self) -> pd.DataFrame:
        data = pd.DataFrame(
            [
                {
                    'month': '2025-02',
                    'ib_wall_street_horizon': 50.0
                },
                {
                    'month': '2025-03',
                    'ib_wall_street_horizon': 50.0
                },
                {
                    'month': '2025-04',
                    'ib_wall_street_horizon': 50.0
                },
                {
                    'month': '2025-05',
                    'ib_wall_street_horizon': 50.0
                }
            ]
        )
        return data

    def _calculate_miscellaneous_expenses_for_each_month(self) -> pd.DataFrame:
        """
        Calculate miscellaneous expenses for each month.
        
        Returns:
            pd.DataFrame: DataFrame with monthly miscellaneous expenses, with 'month' and 'miscellaneous_expenses' columns
        """
        data = pd.DataFrame(
            [
                {
                    'month': '2025-02',
                    'miscellaneous_expenses': 30.0
                },
                {
                    'month': '2025-03',
                    'miscellaneous_expenses': 50.0
                },
                {
                    'month': '2025-06',
                    'miscellaneous_expenses':  3.3
                }
            ]
        )
        return data
