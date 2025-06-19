# app.py
import os
import re
import pandas as pd
import streamlit as st
import sys
import glob
from datetime import datetime

# Add the src directory to the path to import our cost calculator
sys.path.append('src')
from calculateCostForEachMonth import CostCalculator

###############################################################################
# 1. CONFIG
###############################################################################
IMAGE_DIR  = "activeData/images"             # updated path to match new hierarchy
PREDICTIONS_DIR = "activeData/predictions"   # directory containing prediction CSV files


###############################################################################
# 2. DATA HARDCODED IN APPLICATION
###############################################################################
@st.cache_data
def get_hardcoded_data() -> pd.DataFrame:
    """
    Returns the factor insights data as a pandas DataFrame,
    with data hardcoded directly in the application.
    """
    folders_name = ["prompt_1.0.0_4o-mini",
                    "prompt_1.0.6_4o-mini_attempt1",
                    "prompt_1.0.6_4o-mini_attempt2",
                    "prompt_1.0.6_4.1-mini_attempt1",
                    "prompt_1.2.16_4o-mini_attempt1",
                    "prompt_2.2.1_4o-mini_attempt2",
                    "prompt_1.0.6_4o-mini_attempt1_useOldDistToPredict",
                    ]
    data = {
        "Metric": [
            "Result Folder Name",
            "Factor 1 Name",
            "Factor 1 Prediction Regression Coeff",
            "Factor 1 Performance",
            "Factor 1 Scatter",
            "Factor 1 Critical Distribution",
            "Factor 1 Only Portfolio Value Over Time",
            "Factor 1 Only Portfolio Performance",
            "Factor 2 Name",
            "Factor 2 Prediction Regression Coeff",
            "Factor 2 Performance",
            "Factor 2 Scatter",
            "Factor 2 Critical Distribution",
            "Factor 2 Only Portfolio Value Over Time",
            "Factor 2 Only Portfolio Performance",
            "Factor 3 Name",
            "Factor 3 Prediction Regression Coeff",
            "Factor 3 Performance",
            "Factor 3 Scatter",
            "Factor 3 Critical Distribution",
            "Factor 3 Only Portfolio Value Over Time",
            "Factor 3 Only Portfolio Performance",
            "Factor 4 Name",
            "Factor 4 Prediction Regression Coeff",
            "Factor 4 Performance",
            "Factor 4 Scatter",
            "Factor 4 Critical Distribution",
            "Factor 4 Only Portfolio Value Over Time",
            "Factor 4 Only Portfolio Performance",
            "Factor 5 Name",
            "Factor 5 Prediction Regression Coeff",
            "Factor 5 Performance",
            "Factor 5 Scatter",
            "Factor 5 Critical Distribution",
            "Factor 5 Only Portfolio Value Over Time",
            "Factor 5 Only Portfolio Performance",
            "Overall Scatter",
            "Overall Critical Distribution",
            "Overall Performance",
            "Overall Performance Value",
            "Overall Performance Using the Equally-Destributed-Always-Buy Strategy",
            "Overall Performance Using the Equally-Destributed-Always-Buy Strategy Value",
            "Conclusion",
        ],
        folders_name[0]: [
            "largeScaleCloseLoopSim_gpt-4o-mini_attempt2",
            "Historical Performance",
            0.12,
            "🟢 Good in [-15, +15]",
            f"{folders_name[0]}/factor_1_predicted_vs_actual_scatter_clipped.png",
            f"{folders_name[0]}/odds_by_prediction_win_rates_and_counts_by_group_for_factor_1_largeScaleCloseLoopSim.png",
            f"{folders_name[0]}/portfolio_value_over_time_using_kelly_fraction_using_prediction_by_factor_1.png",
            2.14,
            "Candle",
            0.08,
            "X Double Pick",
            f"{folders_name[0]}/factor_2_predicted_vs_actual_scatter_clipped.png",
            f"{folders_name[0]}/odds_by_prediction_win_rates_and_counts_by_group_for_factor_2_largeScaleCloseLoopSim.png",
            f"{folders_name[0]}/portfolio_value_over_time_using_kelly_fraction_using_prediction_by_factor_2.png",
            1.82,
            "Volume Profile",
            -0.02,
            "X Complete Flat",
            f"{folders_name[0]}/factor_3_predicted_vs_actual_scatter_clipped.png",
            f"{folders_name[0]}/odds_by_prediction_win_rates_and_counts_by_group_for_factor_3_largeScaleCloseLoopSim.png",
            f"{folders_name[0]}/portfolio_value_over_time_using_kelly_fraction_using_prediction_by_factor_3.png",
            2.05,
            "Market Trend",
            0.03,
            "🟢 Available in [-20, 20]",
            f"{folders_name[0]}/factor_4_predicted_vs_actual_scatter_clipped.png",
            f"{folders_name[0]}/odds_by_prediction_win_rates_and_counts_by_group_for_factor_4_largeScaleCloseLoopSim.png",
            f"{folders_name[0]}/portfolio_value_over_time_using_kelly_fraction_using_prediction_by_factor_4.png",
            2.20,
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            f"{folders_name[0]}/win_rates_and_counts_by_group_for_all_rows_largeScaleCloseLoopSim_average_actual_price_change_scatter.png",
            f"{folders_name[0]}/odds_by_prediction_win_rates_and_counts_by_group_for_all_rows_largeScaleCloseLoopSim.png",
            f"{folders_name[0]}/portfolio_value_over_time_using_kelly_fraction_all_period.png",
            2.18,
            f"{folders_name[0]}/portfolio_value_over_time_using_kelly_fraction_equal_distributed_all_period.png",
            1.38,
            "Usable in [-15, +20]"
        ],
        "prompt_1.0.6_4o-mini_attempt1": [
            "prompt1.0.6_gpt-4omini_attempt1",
            "Historical Performance",
            0.08,
            "X Double Pick",
            f"{folders_name[1]}/factor_1_predicted_vs_actual_scatter_clipped.png",
            f"{folders_name[1]}/odds_by_prediction_win_rates_and_counts_by_group_for_factor_1_largeScaleCloseLoopSim.png",
            f"{folders_name[1]}/portfolio_value_over_time_using_kelly_fraction_using_prediction_by_factor_1.png",
            1.28,
            "Candle",
            0.05,
            "🟢 Usable in [-10, +15]",
            f"{folders_name[1]}/factor_2_predicted_vs_actual_scatter_clipped.png",
            f"{folders_name[1]}/odds_by_prediction_win_rates_and_counts_by_group_for_factor_2_largeScaleCloseLoopSim.png",
            f"{folders_name[1]}/portfolio_value_over_time_using_kelly_fraction_using_prediction_by_factor_2.png",
            1.40,
            "Volume Profile",
            0.09,
            "X Complete Flat in [-5, +5]",
            f"{folders_name[1]}/factor_3_predicted_vs_actual_scatter_clipped.png",
            f"{folders_name[1]}/odds_by_prediction_win_rates_and_counts_by_group_for_factor_3_largeScaleCloseLoopSim.png",
            f"{folders_name[1]}/portfolio_value_over_time_using_kelly_fraction_using_prediction_by_factor_3.png",
            2.03,
            "Market Trend",
            0.02,
            "🟢 Usable in [-15, +20]",
            f"{folders_name[1]}/factor_4_predicted_vs_actual_scatter_clipped.png",
            f"{folders_name[1]}/odds_by_prediction_win_rates_and_counts_by_group_for_factor_4_largeScaleCloseLoopSim.png",
            f"{folders_name[1]}/portfolio_value_over_time_using_kelly_fraction_using_prediction_by_factor_4.png",
            1.30,
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            f"{folders_name[1]}/win_rates_and_counts_by_group_for_all_rows_largeScaleCloseLoopSim_average_actual_price_change_scatter.png",
            f"{folders_name[1]}/odds_by_prediction_win_rates_and_counts_by_group_for_all_rows_largeScaleCloseLoopSim.png",
            f"{folders_name[1]}/portfolio_value_over_time_using_kelly_fraction_all_period.png",
            1.40,
            f"{folders_name[1]}/portfolio_value_over_time_using_kelly_fraction_equal_distributed_all_period.png",
            1.39,
            "Usable in [-7.5, +12]"
        ],
        "prompt_1.0.6_4o-mini_attempt2": [
            "prompt1.0.6_gpt-4omini_attempt2",
            "Historical Performance",
            0.06,
            "X Double Pick",
            f"{folders_name[2]}/factor_1_predicted_vs_actual_scatter_clipped.png",
            f"{folders_name[2]}/odds_by_prediction_win_rates_and_counts_by_group_for_factor_1_largeScaleCloseLoopSim.png",
            f"{folders_name[2]}/portfolio_value_over_time_using_kelly_fraction_using_prediction_by_factor_1.png",
            1.26,
            "Candle",
            0.02,
            "🟢 Usable in [-10, +15] (barely",
            f"{folders_name[2]}/factor_2_predicted_vs_actual_scatter_clipped.png",
            f"{folders_name[2]}/odds_by_prediction_win_rates_and_counts_by_group_for_factor_2_largeScaleCloseLoopSim.png",
            f"{folders_name[2]}/portfolio_value_over_time_using_kelly_fraction_using_prediction_by_factor_2.png",
            1.19,
            "Volume Profile",
            -0.08,
            "X Complete Flat in [-5, +5]",
            f"{folders_name[2]}/factor_3_predicted_vs_actual_scatter_clipped.png",
            f"{folders_name[2]}/odds_by_prediction_win_rates_and_counts_by_group_for_factor_3_largeScaleCloseLoopSim.png",
            f"{folders_name[2]}/portfolio_value_over_time_using_kelly_fraction_using_prediction_by_factor_3.png",
            1.16,
            "Market Trend",
            0.02,
            "X Complete Flat in [-5, +5]",
            f"{folders_name[2]}/factor_4_predicted_vs_actual_scatter_clipped.png",
            f"{folders_name[2]}/odds_by_prediction_win_rates_and_counts_by_group_for_factor_4_largeScaleCloseLoopSim.png",
            f"{folders_name[2]}/portfolio_value_over_time_using_kelly_fraction_using_prediction_by_factor_4.png",
            1.32,
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            f"{folders_name[2]}/win_rates_and_counts_by_group_for_all_rows_largeScaleCloseLoopSim_average_actual_price_change_scatter.png",
            f"{folders_name[2]}/odds_by_prediction_win_rates_and_counts_by_group_for_all_rows_largeScaleCloseLoopSim.png",
            f"{folders_name[2]}/portfolio_value_over_time_using_kelly_fraction_all_period.png",
            1.33,
            f"{folders_name[2]}/portfolio_value_over_time_using_kelly_fraction_equal_distributed_all_period.png",
            1.54,
            "Not usable"
        ],
        "prompt_1.0.6_4.1-mini_attempt1": [
            "prompt1.0.6_gpt-4.1mini_attempt1",
            "Historical Performance",
            0.15,
            "🟢 Usable in [-15, +15]",
            f"{folders_name[3]}/factor_1_predicted_vs_actual_scatter_clipped.png",
            f"{folders_name[3]}/odds_by_prediction_win_rates_and_counts_by_group_for_factor_1_largeScaleCloseLoopSim.png",
            f"{folders_name[3]}/portfolio_value_over_time_using_kelly_fraction_using_prediction_by_factor_1.png",
            0.86,
            "Candle",
            -0.01,
            "X Double Pick",
            f"{folders_name[3]}/factor_2_predicted_vs_actual_scatter_clipped.png",
            f"{folders_name[3]}/odds_by_prediction_win_rates_and_counts_by_group_for_factor_2_largeScaleCloseLoopSim.png",
            f"{folders_name[3]}/portfolio_value_over_time_using_kelly_fraction_using_prediction_by_factor_2.png",
            1.16,
            "Volume Profile",
            -0.13,
            "X Minus Relation in [-3, +3]",
            f"{folders_name[3]}/factor_3_predicted_vs_actual_scatter_clipped.png",
            f"{folders_name[3]}/odds_by_prediction_win_rates_and_counts_by_group_for_factor_3_largeScaleCloseLoopSim.png",
            f"{folders_name[3]}/portfolio_value_over_time_using_kelly_fraction_using_prediction_by_factor_3.png",
            1.20,
            "Market Trend",
            -0.04,
            "X Complete Flat",
            f"{folders_name[3]}/factor_4_predicted_vs_actual_scatter_clipped.png",
            f"{folders_name[3]}/odds_by_prediction_win_rates_and_counts_by_group_for_factor_4_largeScaleCloseLoopSim.png",
            f"{folders_name[3]}/portfolio_value_over_time_using_kelly_fraction_using_prediction_by_factor_4.png",
            1.20,
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            f"{folders_name[3]}/win_rates_and_counts_by_group_for_all_rows_largeScaleCloseLoopSim_average_actual_price_change_scatter.png",
            f"{folders_name[3]}/odds_by_prediction_win_rates_and_counts_by_group_for_all_rows_largeScaleCloseLoopSim.png",
            f"{folders_name[3]}/portfolio_value_over_time_using_kelly_fraction_all_period.png",
            1.25,
            f"{folders_name[3]}/portfolio_value_over_time_using_kelly_fraction_equal_distributed_all_period.png",
            1.38,
            "Flat, not usable"
        ],
        "prompt_1.2.16_4o-mini_attempt1": [
            "agent1.2.16_gpt-4omini",
            "Historical Performance",
            0.14,
            "X Double Pick",
            f"{folders_name[4]}/factor_1_predicted_vs_actual_scatter.png",
            f"{folders_name[4]}/odds_by_prediction_win_rates_and_counts_by_group_for_factor_1_largeScaleCloseLoopSim.png",
            f"{folders_name[4]}/portfolio_value_over_time_using_kelly_fraction_using_prediction_by_factor_1.png",
            1.08,
            "Candle",
            -0.01,
            "X Double Pick",
            f"{folders_name[4]}/factor_2_predicted_vs_actual_scatter.png",
            f"{folders_name[4]}/odds_by_prediction_win_rates_and_counts_by_group_for_factor_2_largeScaleCloseLoopSim.png",
            f"{folders_name[4]}/portfolio_value_over_time_using_kelly_fraction_using_prediction_by_factor_2.png",
            1.11,
            "Guidance",
            0.1,
            "🟢 Usable in [-7.5, +7.5]",
            f"{folders_name[4]}/factor_3_predicted_vs_actual_scatter.png",
            f"{folders_name[4]}/odds_by_prediction_win_rates_and_counts_by_group_for_factor_3_largeScaleCloseLoopSim.png",
            f"{folders_name[4]}/portfolio_value_over_time_using_kelly_fraction_using_prediction_by_factor_3.png",
            1.12,
            "Market Trend",
            0.06,
            "🟢 Usable in [-7.5, +7.5]",
            f"{folders_name[4]}/factor_4_predicted_vs_actual_scatter.png",
            f"{folders_name[4]}/odds_by_prediction_win_rates_and_counts_by_group_for_factor_4_largeScaleCloseLoopSim.png",
            f"{folders_name[4]}/portfolio_value_over_time_using_kelly_fraction_using_prediction_by_factor_4.png",
            1.17,
            "Macro Economy",
            -0.12,
            "X Double Pick",
            f"{folders_name[4]}/factor_5_predicted_vs_actual_scatter.png",
            f"{folders_name[4]}/odds_by_prediction_win_rates_and_counts_by_group_for_factor_5_largeScaleCloseLoopSim.png",
            f"{folders_name[4]}/portfolio_value_over_time_using_kelly_fraction_using_prediction_by_factor_5.png",
            1.11,
            f"{folders_name[4]}/win_rates_and_counts_by_group_for_all_rows_largeScaleCloseLoopSim_average_actual_price_change_scatter.png",
            f"{folders_name[4]}/odds_by_prediction_win_rates_and_counts_by_group_for_all_rows_largeScaleCloseLoopSim.png",
            f"{folders_name[4]}/portfolio_value_over_time_using_kelly_fraction_all_period.png",
            1.13,
            f"{folders_name[4]}/portfolio_value_over_time_using_kelly_fraction_equal_distributed_all_period.png",
            1.20,
            "Usable in [-2.5, +5]"
        ],
        "prompt_2.2.1_4o-mini_attempt2": [
            "prompt2.2.1_gpt-4omini_attempt2",
            "Historical Performance",
            "",
            "🟡 Usable in [0, +1]",
            f"{folders_name[5]}/factor_1_predicted_vs_actual_scatter_clipped.png",
            f"{folders_name[5]}/odds_by_prediction_win_rates_and_counts_by_group_for_factor_1_largeScaleCloseLoopSim.png",
            f"{folders_name[5]}/portfolio_value_over_time_using_kelly_fraction_using_prediction_by_factor_1.png",
            1.32,
            "Candle",
            "",
            "X Double Pick",
            f"{folders_name[5]}/factor_2_predicted_vs_actual_scatter_clipped.png",
            f"{folders_name[5]}/odds_by_prediction_win_rates_and_counts_by_group_for_factor_2_largeScaleCloseLoopSim.png",
            f"{folders_name[5]}/portfolio_value_over_time_using_kelly_fraction_using_prediction_by_factor_2.png",
            1.24,
            "Volume Profile",
            "",
            "X Complete Flat in [0, 1]",
            f"{folders_name[5]}/factor_3_predicted_vs_actual_scatter_clipped.png",
            f"{folders_name[5]}/odds_by_prediction_win_rates_and_counts_by_group_for_factor_3_largeScaleCloseLoopSim.png",
            f"{folders_name[5]}/portfolio_value_over_time_using_kelly_fraction_using_prediction_by_factor_3.png",
            1.32,
            "Market Trend",
            "",
            "X Complete Flat in [0, 1]",
            f"{folders_name[5]}/factor_4_predicted_vs_actual_scatter_clipped.png",
            f"{folders_name[5]}/odds_by_prediction_win_rates_and_counts_by_group_for_factor_4_largeScaleCloseLoopSim.png",
            f"{folders_name[5]}/portfolio_value_over_time_using_kelly_fraction_using_prediction_by_factor_4.png",
            1.39,
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            f"{folders_name[5]}/win_rates_and_counts_by_group_for_all_rows_largeScaleCloseLoopSim_average_actual_price_change_scatter.png",
            f"{folders_name[5]}/odds_by_prediction_win_rates_and_counts_by_group_for_all_rows_largeScaleCloseLoopSim.png",
            f"{folders_name[5]}/portfolio_value_over_time_using_kelly_fraction_all_period.png",
            1.32,
            f"{folders_name[5]}/portfolio_value_over_time_using_kelly_fraction_equal_distributed_all_period.png",
            1.38,
            "Unusable as overall, only as seperated factors"
        ],
        "prompt_1.0.6_4o-mini_attempt1_useOldDistToPredict": [
            "prompt1.0.6_gpt-4omini_attempt1_useOldDistToPredict",
            "Historical Performance",
            0.08,
            "X Double Pick",
            f"{folders_name[6]}/factor_1_predicted_vs_actual_scatter_clipped.png",
            f"{folders_name[6]}/odds_by_prediction_win_rates_and_counts_by_group_for_factor_1_largeScaleCloseLoopSim.png",
            f"{folders_name[6]}/portfolio_value_over_time_using_kelly_fraction_using_prediction_by_factor_1.png",
            1.28,
            "Candle",
            0.05,
            "🟢 Usable in [-10, +15]",
            f"{folders_name[6]}/factor_2_predicted_vs_actual_scatter_clipped.png",
            f"{folders_name[6]}/odds_by_prediction_win_rates_and_counts_by_group_for_factor_2_largeScaleCloseLoopSim.png",
            f"{folders_name[6]}/portfolio_value_over_time_using_kelly_fraction_using_prediction_by_factor_2.png",
            1.40,
            "Volume Profile",
            0.09,
            "X Complete Flat in [-5, +5]",
            f"{folders_name[6]}/factor_3_predicted_vs_actual_scatter_clipped.png",
            f"{folders_name[6]}/odds_by_prediction_win_rates_and_counts_by_group_for_factor_3_largeScaleCloseLoopSim.png",
            f"{folders_name[6]}/portfolio_value_over_time_using_kelly_fraction_using_prediction_by_factor_3.png",
            2.03,
            "Market Trend",
            0.02,
            "🟢 Usable in [-15, +20]",
            f"{folders_name[6]}/factor_4_predicted_vs_actual_scatter_clipped.png",
            f"{folders_name[6]}/odds_by_prediction_win_rates_and_counts_by_group_for_factor_4_largeScaleCloseLoopSim.png",
            f"{folders_name[6]}/portfolio_value_over_time_using_kelly_fraction_using_prediction_by_factor_4.png",
            1.30,
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            f"{folders_name[6]}/win_rates_and_counts_by_group_for_all_rows_largeScaleCloseLoopSim_average_actual_price_change_scatter.png",
            f"{folders_name[6]}/odds_by_prediction_win_rates_and_counts_by_group_for_all_rows_largeScaleCloseLoopSim.png",
            f"{folders_name[6]}/portfolio_value_over_time_using_kelly_fraction_all_period.png",
            1.40,
            f"{folders_name[6]}/portfolio_value_over_time_using_kelly_fraction_equal_distributed_all_period.png",
            1.39,
            "Usable in [-7.5, +12]"
        ]
    }
    
    df = pd.DataFrame(data)
    df = df.set_index("Metric")
    return df


@st.cache_data
def get_cost_data() -> pd.DataFrame:
    """
    Returns the monthly cost data as a pandas DataFrame.
    """
    calculator = CostCalculator()
    return calculator.calculate_costs_for_each_month()


@st.cache_data
def get_prediction_files() -> list:
    """
    Returns a list of CSV files in the predictions directory.
    """
    if not os.path.exists(PREDICTIONS_DIR):
        return []
    
    csv_files = glob.glob(os.path.join(PREDICTIONS_DIR, "*.csv"))
    # Return just the filename without the full path
    return [os.path.basename(f) for f in csv_files]


@st.cache_data
def load_prediction_csv(filename: str) -> pd.DataFrame:
    """
    Load a specific prediction CSV file and return as DataFrame.
    """
    filepath = os.path.join(PREDICTIONS_DIR, filename)
    if os.path.exists(filepath):
        return pd.read_csv(filepath)
    return pd.DataFrame()


# Load the hardcoded data
df = get_hardcoded_data()


###############################################################################
# 3. SIDEBAR – VIEW SELECTOR AND OPTIONS
###############################################################################
st.sidebar.title("📊 Dashboard")

# View selector - using selectbox instead of radio
view_mode = st.sidebar.selectbox(
    "Choose view:",
    ["📌 Prompts", "💰 Costs", "🔮 Predictions"],
    index=0
)

st.sidebar.markdown("---")

if view_mode == "📌 Prompts":
    # Existing prompt selector - also using selectbox
    st.sidebar.title("📌 Prompts")
    prompt_names = df.columns.tolist()
    selected_prompt = st.sidebar.selectbox(
        "Choose a model / prompt run:",
        prompt_names,
        index=0
    )

    # Add toggle button for images
    st.sidebar.markdown("---")
    show_images = st.sidebar.checkbox(
        "Show images", 
        value=True,
        help="Uncheck to hide images and focus on text data"
    )

elif view_mode == "💰 Costs":
    st.sidebar.title("💰 Cost Analysis")
    st.sidebar.write("Monthly cost breakdown for all services")

elif view_mode == "🔮 Predictions":
    st.sidebar.title("🔮 Predictions")
    prediction_files = get_prediction_files()
    
    if prediction_files:
        selected_prediction_file = st.sidebar.selectbox(
            "Choose a prediction file:",
            prediction_files,
            index=0
        )
    else:
        selected_prediction_file = None
        st.sidebar.write("No prediction files found")


###############################################################################
# 4. MAIN PANEL – DISPLAY CONTENT BASED ON VIEW MODE
###############################################################################

if view_mode == "📌 Prompts":
    # Existing prompt display logic
    st.header(f"🗂️ {selected_prompt}")

    col_data = df[selected_prompt]

    for metric, cell in col_data.items():
        # Skip empty strings
        if isinstance(cell, str) and cell.strip() == "":
            continue

        # Section header ──────────────────────────────────────────────────────────
        st.markdown(f"### {metric}")

        ###########################################################################
        # 4-A.  IS THIS CELL POINTING TO AN IMAGE?
        ###########################################################################
        # ❶  If the CSV cell holds an explicit file name
        if isinstance(cell, str) and re.search(r"\.(png|jpe?g|gif)$", cell, re.I):
            if show_images:
                # First try the direct path in the prompt subdirectory
                img_path_in_prompt = os.path.join(IMAGE_DIR, selected_prompt, cell)
                if os.path.isfile(img_path_in_prompt):
                    st.image(img_path_in_prompt, use_container_width=True)
                # Fallback to the old logic for absolute paths or direct IMAGE_DIR
                elif os.path.isabs(cell):
                    if os.path.isfile(cell):
                        st.image(cell, use_container_width=True)
                    else:
                        st.warning(f"Image not found: `{cell}`")
                else:
                    img_path = os.path.join(IMAGE_DIR, cell)
                    if os.path.isfile(img_path):
                        st.image(img_path, use_container_width=True)
                    else:
                        st.warning(f"Image not found: `{img_path}` or `{img_path_in_prompt}`")
            else:
                # Show image path instead of the image
                st.code(cell, language=None)

        # ❂  If Excel stored the word "Picture" instead of the file name
        elif isinstance(cell, str) and cell.strip().lower() == "picture":
            if show_images:
                # Attempt a best-guess file name: activeData/images/<prompt>/<metric>.png
                safe_metric = re.sub(r"\W+", "_", metric).lower()
                guess_path = os.path.join(IMAGE_DIR, selected_prompt, f"{safe_metric}.png")
                if os.path.isfile(guess_path):
                    st.image(guess_path, use_container_width=True)
                else:
                    st.info("📷 *(an image goes here – place it at "
                            f"`{guess_path}` and it will appear)*")
            else:
                # Show placeholder text
                st.write("📷 *[Image cachée]*")

        # ❸  Otherwise, show the raw value (number, text, NaN, …)
        else:
            # For floats with many decimals, tidy them up a bit
            if isinstance(cell, float):
                st.write(f"{cell:.4g}")
            else:
                st.write(cell)

    ###########################################################################
    # 5. (OPTIONAL) RAW DATA EXPANDER FOR PROMPTS
    ###########################################################################
    with st.expander("🔎 Peek raw data for this prompt"):
        st.dataframe(col_data.reset_index(), use_container_width=True)

elif view_mode == "💰 Costs":
    # Cost display logic
    st.header("💰 Monthly Cost Analysis")
    
    try:
        cost_df = get_cost_data()
        
        if not cost_df.empty:
            st.markdown("### 📊 Monthly Cost Breakdown")
            
            # Display the main cost table
            st.dataframe(
                cost_df.style.format({
                    'openai': '${:.2f}',
                    'ib_wall_street_horizon': '${:.2f}',
                    'miscellaneous_expenses': '${:.2f}'
                }),
                use_container_width=True
            )
            
            # Calculate total cost column
            cost_df_with_total = cost_df.copy()
            cost_df_with_total['total'] = cost_df_with_total.fillna(0).sum(axis=1)
            
            # Summary statistics
            st.markdown("### 💰 Cost Summary")
            
            # First row - Main totals
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric(
                    label="Total Cost", 
                    value=f"${cost_df_with_total['total'].sum():.2f}"
                )
            
            with col2:
                st.metric(
                    label="Average Monthly", 
                    value=f"${cost_df_with_total['total'].mean():.2f}"
                )
            
            with col3:
                st.metric(
                    label="Highest Month", 
                    value=f"${cost_df_with_total['total'].max():.2f}"
                )
            
            # Second row - Breakdown by service
            st.markdown("#### By Service:")
            col4, col5, col6 = st.columns(3)
            
            with col4:
                st.metric(
                    label="OpenAI", 
                    value=f"${cost_df['openai'].fillna(0).sum():.2f}"
                )
            
            with col5:
                st.metric(
                    label="IB Wall Street", 
                    value=f"${cost_df['ib_wall_street_horizon'].fillna(0).sum():.2f}"
                )
            
            with col6:
                st.metric(
                    label="Miscellaneous", 
                    value=f"${cost_df['miscellaneous_expenses'].fillna(0).sum():.2f}"
                )
            
            # Cost trend chart
            st.markdown("### 📈 Cost Trend Over Time")
            chart_df = cost_df.fillna(0)
            chart_df['Total'] = chart_df.sum(axis=1)
            st.line_chart(chart_df)
            
            # Monthly breakdown
            st.markdown("### 📅 Detailed Monthly Breakdown")
            
            # Create a more detailed breakdown
            detailed_df = cost_df_with_total.copy()
            detailed_df['Month Name'] = pd.to_datetime(detailed_df.index + '-01').strftime('%B %Y')
            detailed_df = detailed_df.reset_index()
            detailed_df = detailed_df[['month', 'Month Name', 'openai', 'ib_wall_street_horizon', 'miscellaneous_expenses', 'total']]
            detailed_df.columns = ['Month (YYYY-MM)', 'Month Name', 'OpenAI Cost', 'IB Wall Street Horizon', 'Miscellaneous Expenses', 'Total Cost']
            
            st.dataframe(
                detailed_df.style.format({
                    'OpenAI Cost': '${:.2f}',
                    'IB Wall Street Horizon': '${:.2f}',
                    'Miscellaneous Expenses': '${:.2f}',
                    'Total Cost': '${:.2f}'
                }),
                use_container_width=True,
                hide_index=True
            )
            
        else:
            st.warning("No cost data found. Please check if the OpenAI cost CSV files are available in the `activeData/costs/openai/` directory.")
            
    except Exception as e:
        st.error(f"Error loading cost data: {e}")
        st.info("Please ensure the cost calculation module is properly configured and the CSV files are accessible.")

elif view_mode == "🔮 Predictions":
    # Predictions display logic
    st.header("🔮 Trading Predictions")
    
    prediction_files = get_prediction_files()
    
    if not prediction_files:
        st.warning("No prediction files found in the predictions directory.")
        st.info(f"Please add CSV files to the `{PREDICTIONS_DIR}` directory.")
    else:
        # File overview section
        st.markdown("### 📋 Available Prediction Files")
        
        # Create a summary table of all files
        file_info = []
        for filename in prediction_files:
            filepath = os.path.join(PREDICTIONS_DIR, filename)
            if os.path.exists(filepath):
                # Get file info
                file_stats = os.stat(filepath)
                file_size = file_stats.st_size
                mod_time = datetime.fromtimestamp(file_stats.st_mtime)
                
                # Try to get row count
                try:
                    df_temp = pd.read_csv(filepath)
                    row_count = len(df_temp)
                except:
                    row_count = "N/A"
                
                file_info.append({
                    'Filename': filename,
                    'Size (KB)': f"{file_size/1024:.1f}",
                    'Rows': row_count,
                    'Last Modified': mod_time.strftime('%Y-%m-%d %H:%M')
                })
        
        files_df = pd.DataFrame(file_info)
        st.dataframe(files_df, use_container_width=True, hide_index=True)
        
        # File selection and download section
        st.markdown("### 📥 Download Files")
        
        # Create download buttons for each file
        for filename in prediction_files:
            filepath = os.path.join(PREDICTIONS_DIR, filename)
            
            if os.path.exists(filepath):
                # Load file content for download
                with open(filepath, 'rb') as file:
                    file_content = file.read()
                
                # Create columns for filename and download button
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    st.write(f"📄 **{filename}**")
                
                with col2:
                    st.download_button(
                        label="⬇️ Download",
                        data=file_content,
                        file_name=filename,
                        mime="text/csv",
                        key=f"download_{filename}"
                    )
        
        # File preview section
        if prediction_files:
            st.markdown("### 👀 File Preview")
            
            selected_file = st.selectbox(
                "Select a file to preview:",
                prediction_files,
                index=0
            )
            
            if selected_file:
                try:
                    df_preview = load_prediction_csv(selected_file)
                    
                    if not df_preview.empty:
                        st.markdown(f"**Preview of {selected_file}:**")
                        
                        # Show basic info
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.metric("Total Rows", len(df_preview))
                        with col2:
                            st.metric("Total Columns", len(df_preview.columns))
                        with col3:
                            # Check if there are any predictions
                            if 'symbol' in df_preview.columns:
                                st.metric("Unique Symbols", df_preview['symbol'].nunique())
                        
                        # Show the data
                        st.dataframe(df_preview, use_container_width=True)
                        
                        # Show column information
                        with st.expander("📊 Column Information"):
                            col_info = pd.DataFrame({
                                'Column': df_preview.columns,
                                'Data Type': df_preview.dtypes.astype(str),
                                'Non-Null Count': df_preview.count(),
                                'Null Count': df_preview.isnull().sum()
                            }).reset_index(drop=True)
                            st.dataframe(col_info, use_container_width=True, hide_index=True)
                        
                        # Additional download option in preview section
                        with open(os.path.join(PREDICTIONS_DIR, selected_file), 'rb') as file:
                            file_content = file.read()
                        
                        st.download_button(
                            label=f"⬇️ Download {selected_file}",
                            data=file_content,
                            file_name=selected_file,
                            mime="text/csv",
                            key=f"preview_download_{selected_file}"
                        )
                        
                    else:
                        st.warning(f"The file {selected_file} appears to be empty or could not be loaded.")
                        
                except Exception as e:
                    st.error(f"Error loading {selected_file}: {e}")
