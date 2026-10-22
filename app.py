
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Hasnat's FPL Player Data Explorer",
    page_icon="⚽",
    layout="wide"
)

st.title("⚽ FPL Player Data Explorer by Hasnat Ahsan")
st.caption("Explore player performance, recent form and upcoming opponents.")

# Load your existing calculated data
@st.cache_data
def load_data():
    return pd.read_csv("points_f.csv")

df = load_data()

# Default display columns
default_columns = [
    "web_name",
    "name",
    "singular_name_short",
    "round",
    "points_last3",
    "points_last2",
    "egi_last3",
    "egi_last2",
    "minutes_last3",
    "next1gw_opponent"
]

default_columns = [
    c for c in default_columns if c in df.columns
]

# -----------------------------
# FIRST FILTER
# -----------------------------

st.subheader("1. Filter Players")

col1, col2 = st.columns(2)

with col1:
    filter_column = st.selectbox(
        "Filter Column",
        ["No Filter"] + list(df.columns)
    )

with col2:
    filter_value = st.text_input(
        "Filter Value",
        placeholder="Enter a value"
    )

# -----------------------------
# SECOND FILTER
# -----------------------------

st.subheader("2. Numeric Filter")

numeric_columns = df.select_dtypes(
    include="number"
).columns.tolist()

col3, col4, col5 = st.columns(3)

with col3:
    second_filter_column = st.selectbox(
        "2nd Filter Column",
        ["No Filter"] + numeric_columns
    )

with col4:
    operator = st.selectbox(
        "Comparison",
        [">", "<", ">=", "<=", "=="]
    )

with col5:
    second_filter_value = st.number_input(
        "2nd Filter Value",
        value=0.0
    )

# -----------------------------
# SORTING
# -----------------------------

st.subheader("3. Sort Results")

col6, col7, col8 = st.columns(3)

with col6:
    sort_column = st.selectbox(
        "Sort Column",
        list(df.columns),
        index=(
            list(df.columns).index("points_last3")
            if "points_last3" in df.columns else 0
        )
    )

with col7:
    sort_order = st.selectbox(
        "Sort Order",
        ["Descending", "Ascending"]
    )

with col8:
    top_n = st.number_input(
        "Top N Rows",
        min_value=1,
        max_value=max(1, len(df)),
        value=min(10, max(1, len(df))),
        step=1
    )

# -----------------------------
# SELECT DISPLAY COLUMNS
# -----------------------------

st.subheader("4. Select Columns to Display")

selected_columns = st.multiselect(
    "Choose Columns",
    options=list(df.columns),
    default=default_columns
)

# -----------------------------
# SHOW RESULTS
# -----------------------------

if st.button("Show Results", type="primary"):

    result = df.copy()

    # First filter
    if filter_column != "No Filter" and filter_value.strip():

        if pd.api.types.is_numeric_dtype(
            result[filter_column]
        ):
            try:
                value = float(filter_value)
                result = result[
                    result[filter_column] == value
                ]
            except ValueError:
                st.error("Enter a valid numeric filter value.")
                st.stop()

        else:
            result = result[
                result[filter_column]
                .astype(str)
                .str.contains(
                    filter_value,
                    case=False,
                    na=False,
                    regex=False
                )
            ]

    # Second filter
    if second_filter_column != "No Filter":

        series = pd.to_numeric(
            result[second_filter_column],
            errors="coerce"
        )

        v = second_filter_value

        if operator == ">":
            result = result[series > v]
        elif operator == "<":
            result = result[series < v]
        elif operator == ">=":
            result = result[series >= v]
        elif operator == "<=":
            result = result[series <= v]
        elif operator == "==":
            result = result[series == v]

    # Sorting
    result = result.sort_values(
        by=sort_column,
        ascending=(sort_order == "Ascending"),
        na_position="last"
    )

    # Display
    if not selected_columns:
        st.warning("Please select at least one display column.")
    else:
        st.success(
            f"{len(result)} matching rows. "
            f"Displaying top {min(top_n, len(result))}."
        )

        final_result = result.head(top_n)[selected_columns]

        # st.dataframe(
        #     final_result,
        #     use_container_width=True,
        #     hide_index=True
        # )
        
        # Below code (st.dataframe) is added to rename some columns while displaying
        # Original column name stays same in the dataframe
        
        st.dataframe(
            final_result,
            use_container_width=True,
            hide_index=True,
            column_config={
                "singular_name_short": st.column_config.TextColumn(
                    "POS"
                ),
                "name": st.column_config.TextColumn(
                    "team"
                )
            }
        )

        

        # Download filtered results
        csv = final_result.to_csv(index=False)

        st.download_button(
            "Download Results as CSV",
            data=csv,
            file_name="fpl_results.csv",
            mime="text/csv"
        )
