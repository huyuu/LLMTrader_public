# app.py
import os
import re
import pandas as pd
import streamlit as st


###############################################################################
# 1. CONFIG
###############################################################################
CSV_PATH   = "activeData/factorInsights.csv"     # rename if your file is different
IMAGE_DIR  = "activeData/images"             # updated path to match new hierarchy
ENCODING   = "latin1"                        # handles the weird bullets in file


###############################################################################
# 2. LOAD  &  CLEAN  DATA
###############################################################################
@st.cache_data
def load_data(path: str, encoding: str = "utf-8") -> pd.DataFrame:
    """
    Reads the CSV, strips extra whitespace,
    sets the first column as the row-index ('Metric').
    """
    df = pd.read_csv(path, encoding=encoding)
    # Excel added a trailing space to the header; normalise everything
    first_col_original = df.columns[0]  # Keep original name with space
    first_col_stripped = first_col_original.strip()  # Get stripped version
    df = df.rename(columns={first_col_original: "Metric"})  # Rename using original name
    df["Metric"] = df["Metric"].astype(str).str.strip()
    df = df.set_index("Metric")
    # strip whitespace from column headers too
    df.columns = [c.strip() for c in df.columns]
    return df


try:
    df = load_data(CSV_PATH, ENCODING)
except FileNotFoundError:
    st.error(f"⚠️  Could not find {CSV_PATH}.  "
             "Place the file in the same folder or edit `CSV_PATH`.")
    st.stop()


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
            st.image(img_path_in_prompt, use_column_width=True)
        # Fallback to the old logic for absolute paths or direct IMAGE_DIR
        elif os.path.isabs(cell):
            if os.path.isfile(cell):
                st.image(cell, use_column_width=True)
            else:
                st.warning(f"Image not found: `{cell}`")
        else:
            img_path = os.path.join(IMAGE_DIR, cell)
            if os.path.isfile(img_path):
                st.image(img_path, use_column_width=True)
            else:
                st.warning(f"Image not found: `{img_path}` or `{img_path_in_prompt}`")

    # ❂  If Excel stored the word "Picture" instead of the file name
    elif isinstance(cell, str) and cell.strip().lower() == "picture":
        # Attempt a best-guess file name: activeData/images/<prompt>/<metric>.png
        safe_metric = re.sub(r"\W+", "_", metric).lower()
        guess_path = os.path.join(IMAGE_DIR, selected_prompt, f"{safe_metric}.png")
        if os.path.isfile(guess_path):
            st.image(guess_path, use_column_width=True)
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
