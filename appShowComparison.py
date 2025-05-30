# app.py
import os
import re
import pandas as pd
import streamlit as st


###############################################################################
# 1. CONFIG
###############################################################################
IMAGE_DIR  = "activeData/images"             # updated path to match new hierarchy


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
                    "prompt_2.2.1_4o-mini_attempt2"]
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
        ]
    }
    
    df = pd.DataFrame(data)
    df = df.set_index("Metric")
    return df


# Load the hardcoded data
df = get_hardcoded_data()


###############################################################################
# 3. SIDEBAR – PROMPT PICKER
###############################################################################
st.sidebar.title("📌 Prompts")
prompt_names = df.columns.tolist()
selected_prompt = st.sidebar.radio(
    "Choose a model / prompt run:",
    prompt_names,
    index=0,
    format_func=lambda x: x  # (keeps original header as label)
)


###############################################################################
# 4. MAIN PANEL – PRETTY PRINT ONE COLUMN
###############################################################################
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

    # ❂  If Excel stored the word "Picture" instead of the file name
    elif isinstance(cell, str) and cell.strip().lower() == "picture":
        # Attempt a best-guess file name: activeData/images/<prompt>/<metric>.png
        safe_metric = re.sub(r"\W+", "_", metric).lower()
        guess_path = os.path.join(IMAGE_DIR, selected_prompt, f"{safe_metric}.png")
        if os.path.isfile(guess_path):
            st.image(guess_path, use_container_width=True)
        else:
            st.info("📷 *(an image goes here – place it at "
                    f"`{guess_path}` and it will appear)*")

    # ❸  Otherwise, show the raw value (number, text, NaN, …)
    else:
        # For floats with many decimals, tidy them up a bit
        if isinstance(cell, float):
            st.write(f"{cell:.4g}")
        else:
            st.write(cell)


###############################################################################
# 5. (OPTIONAL) RAW DATA EXPANDER
###############################################################################
with st.expander("🔎 Peek raw data for this prompt"):
    st.dataframe(col_data.reset_index(), use_container_width=True)
