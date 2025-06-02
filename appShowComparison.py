# app.py
import os
import re
import pandas as pd
import streamlit as st
import sys

# Add the src directory to the path to import our cost calculator
sys.path.append('src')
from calculateCostForEachMonth import CostCalculator

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


@st.cache_data
def get_cost_data() -> pd.DataFrame:
    """
    Returns the monthly cost data as a pandas DataFrame.
    """
    calculator = CostCalculator()
    return calculator.calculate_costs_for_each_month()


# Load the hardcoded data
df = get_hardcoded_data()


###############################################################################
# 3. SIDEBAR – VIEW SELECTOR AND OPTIONS
###############################################################################
st.sidebar.title("📊 Dashboard")

# View selector - using selectbox instead of radio
view_mode = st.sidebar.selectbox(
    "Choose view:",
    ["📌 Prompts", "💰 Costs"],
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
