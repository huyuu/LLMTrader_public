#!/usr/bin/env python3

import sys
import os

# Add the src directory to the path to import our module
sys.path.append('src')

from calculateCostForEachMonth import CostCalculator

def test_cost_calculator():
    """Test the OpenAI cost calculation function"""
    
    calculator = CostCalculator()
    
    print("Testing OpenAI cost calculation...")
    
    try:
        result_df = calculator._calculate_openai_cost_for_each_month()
        
        print(f"\nFound data for {len(result_df)} months:")
        print(result_df)
        
        if not result_df.empty:
            print(f"\nTotal OpenAI cost across all months: ${result_df['openai'].sum():.2f}")
            print(f"Average monthly cost: ${result_df['openai'].mean():.2f}")
            print(f"Highest monthly cost: ${result_df['openai'].max():.2f}")
            print(f"Lowest monthly cost: ${result_df['openai'].min():.2f}")
        else:
            print("No cost data found.")
            
    except Exception as e:
        print(f"Error during testing: {e}")

if __name__ == "__main__":
    test_cost_calculator() 