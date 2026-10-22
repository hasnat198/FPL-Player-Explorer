
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Hasnat's FPL Player Data Explorer",
    page_icon="⚽",
    layout="wide"
)

st.title("⚽ FPL Player Data Explorer by Hasnat Ahsan")

# Below portin is added to accomodate "About" and "Column Definition"


# =====================================================
# ABOUT THE APPLICATION
# =====================================================

with st.expander("ℹ️ About This Tool", expanded=False):

    st.markdown("""
    ### What does this application do?

    The FPL Player Data Explorer helps Fantasy Premier League
    managers analyze player performance, recent form, and
    upcoming opponents.

    **Key features:**

    - Analyze player performance over the last 2 and 3 gameweeks.
    - Compare FPL points, expected goal involvements, goals,
      assists, minutes, and defensive statistics.
    - Examine upcoming opponents and their performance metrics.
    - Filter players using statistical criteria.
    - Sort players by selected performance indicators.
    - Choose which columns to display.
    - Download filtered results as CSV files.

    ### How is it different from the official FPL website?

    - **Rolling statistics:** Focuses on recent 2- and
      3-gameweek performance.
    - **Opponent analysis:** Adds information about upcoming
      opponents.
    - **Advanced filtering:** Allows customized player
      screening using multiple conditions.
    - **Flexible comparison:** Users can select and sort
      different statistical indicators.
    - **Export:** Filtered results can be downloaded for
      further analysis.

    **Disclaimer:** This is an independent analytical tool
    and is not affiliated with the official Fantasy Premier
    League. Historical performance does not guarantee
    future results.
    """)


# =====================================================
# COLUMN DEFINITIONS
# =====================================================

with st.expander("📖 Column Definitions", expanded=False):

    column_definitions = {
        "web_name": "Player's displayed FPL name",
        "name": "Player's football club",
        "singular_name_short": "Player position (GKP, DEF, MID, FWD)",
        "round": "Gameweek associated with the record",
        "id_player": "Unique player identifier",
        "points_last3": "Total FPL points in the last 3 gameweeks",
        "points_last2": "Total FPL points in the last 2 gameweeks",
        "egi_last3": "Expected goal involvements in the last 3 gameweeks",
        "egi_last2": "Expected goal involvements in the last 2 gameweeks",
        "goals_last3": "Goals scored in the last 3 gameweeks",
        "goals_last2": "Goals scored in the last 2 gameweeks",
        "assists_last3": "Assists in the last 3 gameweeks",
        "assists_last2": "Assists in the last 2 gameweeks",
        "minutes_last3": "Minutes played in the last 3 gameweeks",
        "minutes_last2": "Minutes played in the last 2 gameweeks",
        "dc_last3": "Defensive contributions in the last 3 gameweeks",
        "dc_last2": "Defensive contributions in the last 2 gameweeks",
        "egc_last3": "Expected goals conceded in the last 3 gameweeks",
        "egc_last2": "Expected goals conceded in the last 2 gameweeks",
        "cs_last3": "Clean sheets in the last 3 gameweeks",
        "cs_last2": "Clean sheets in the last 2 gameweeks",
        "saves_last3": "Goalkeeper saves in the last 3 gameweeks",
        "saves_last2": "Goalkeeper saves in the last 2 gameweeks",
        "next1gw_opponent": "Opponent in the next gameweek",
        "next1gw_gc": "Goals conceded by the next opponent",
        "next1gw_egc": "Expected goals conceded by the next opponent",
        "next1gw_gs": "Goals scored by the next opponent",
        "next1gw_egs": "Expected goals scored by the next opponent"
    }

    definitions_df = pd.DataFrame(
        [
            {
                "Column": (
                    "POS" if col == "singular_name_short"
                    else "team" if col == "name"
                    else col
                ),
                "Description": description
            }
            for col, description in column_definitions.items()
        ]
    )

    st.dataframe(
        definitions_df,
        hide_index=True,
        use_container_width=True
    )

    st.markdown("""
    **Naming conventions**

    - `_last3`: Statistics calculated over the last 3 gameweeks.
    - `_last2`: Statistics calculated over the last 2 gameweeks.
    - `next1gw_`: Opponent information for the next gameweek.
    - `next2gw_`: Opponent information for the second upcoming gameweek.
    - `next3gw_`: Opponent information for the third upcoming gameweek.
    - `next4gw_`: Opponent information for the fourth upcoming gameweek.

    **Note:** Opponent statistics reflect the calculation
    methods used to prepare the dataset.
    """)


# End of "About" and "Column Definition"


# =====================================================
# COLOR CODING EXPLANATION
# =====================================================

with st.expander("🎨 Color Coding", expanded=False):

    st.markdown("""
    ### How does the color coding work?

    The upcoming opponent columns (`next1gw_opponent`
    through `next4gw_opponent`) are color-coded based
    exclusively on **expected goals conceded (EGC)**.

    - **Lower EGC:** Indicates a stronger defense,
      making the fixture potentially more difficult
      for attacking players.
    - **Higher EGC:** Indicates a weaker defense,
      making the fixture potentially more favorable
      for attacking players.
    - **Percentile ranking:** Each opponent is ranked
      relative to other opponents using their EGC.
    - **Separate gameweeks:** Percentile rankings are
      calculated separately for each of the next
      four gameweeks.

    ### Color legend
    """)

    color_legend = [
        ("#F4B6B6", "0–20%", "Very strong", "Very difficult"),
        ("#F8CBAA", "20–40%", "Strong", "Difficult"),
        ("#FFE6A1", "40–60%", "Average", "Moderate"),
        ("#D8EDB2", "60–80%", "Weak", "Favorable"),
        ("#B9E8C5", "80–100%", "Very weak", "Very favorable")
    ]

    st.markdown(
        "| Color | EGC Percentile | Defensive Strength | Attacking Fixture |\n"
        "|---|---|---|---|\n"
        + "\n".join(
            f"| <span style='display:inline-block;"
            f"background-color:{color};width:45px;"
            f"height:18px;border-radius:4px;'>&nbsp;</span> "
            f"| {percentile} | {strength} | {difficulty} |"
            for color, percentile, strength, difficulty
            in color_legend
        ),
        unsafe_allow_html=True
    )

    st.markdown("""
    ### Important considerations

    - The colors reflect **defensive strength only**,
      measured by expected goals conceded.
    - They do not incorporate the opponent's attacking
      strength, home or away advantage, injuries,
      player form, or other match conditions.
    - A green fixture does not guarantee high FPL points.
    - The same opponent can have a different color
      across gameweeks if its relative EGC ranking changes.

    **Interpretation:** Red represents a stronger defense,
    while green represents a weaker defense.
    """)



# End of color coding
st.caption("Explore player performance, recent form and upcoming opponents.")

# Load your existing calculated data
@st.cache_data
def load_data():
    return pd.read_csv("points_f.csv")

df = load_data()


# =====================================================
# COLOR CODE NEXT 4 GAMEWEEK OPPONENTS BY xGC PERCENTILE
# =====================================================

# Calculate percentile reference values using unique opponents
opponent_percentiles = {}

for gw in range(1, 5):
    opponent_col = f"next{gw}gw_opponent"
    egc_col = f"next{gw}gw_egc"

    if opponent_col in df.columns and egc_col in df.columns:

        # Each opponent contributes only once per gameweek
        unique_opponents = df[
            [opponent_col, egc_col]
        ].copy()

        unique_opponents[egc_col] = pd.to_numeric(
            unique_opponents[egc_col],
            errors="coerce"
        )

        unique_opponents = (
            unique_opponents
            .dropna(subset=[opponent_col, egc_col])
            .drop_duplicates(subset=[opponent_col])
        )

        opponent_percentiles[egc_col] = (
            unique_opponents[egc_col]
            .rank(pct=True, method="average") * 100
        )

        # Store xGC values for comparison
        opponent_percentiles[egc_col] = (
            unique_opponents[egc_col]
            .reset_index(drop=True)
        )


def color_opponents(row):

    styles = [""] * len(row)

    for gw in range(1, 5):

        opponent_col = f"next{gw}gw_opponent"
        egc_col = f"next{gw}gw_egc"

        if opponent_col not in row.index:
            continue

        if egc_col not in row.index:
            continue

        egc = pd.to_numeric(
            row[egc_col], errors="coerce"
        )

        if pd.isna(egc):
            continue

        reference = opponent_percentiles.get(egc_col)

        if reference is None or reference.empty:
            continue

        # Percentile ranking against unique opponents
        percentile = (reference <= egc).mean() * 100

        if percentile <= 20:
            color = "#F4B6B6"  # Red
        elif percentile <= 40:
            color = "#F8CBAA"  # Orange
        elif percentile <= 60:
            color = "#FFE6A1"  # Yellow
        elif percentile <= 80:
            color = "#D8EDB2"  # Light green
        else:
            color = "#B9E8C5"  # Green

        idx = row.index.get_loc(opponent_col)

        styles[idx] = (
            f"background-color: {color}; "
            "color: #202020"
        )

    return styles


# End of color code

# Default display columns
default_columns = [
    "web_name",
    "name",
    "singular_name_short",
    "egi_last3",
    "goals_last3",
    "assists_last3",
    "egi_last2",
    "goals_last2",
    "assists_last2",
    "next1gw_opponent",
    "next1gw_gc",
    "next1gw_egc",
    "next2gw_opponent",
    "next2gw_gc",
    "next2gw_egc"
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

        # final_result = result.head(top_n)[selected_columns]

        # # st.dataframe(
        # #     final_result,
        # #     use_container_width=True,
        # #     hide_index=True
        # # )
        
        # # Below code (st.dataframe) is added to rename some columns while displaying
        # # Original column name stays same in the dataframe
        
        # st.dataframe(
        #     final_result,
        #     use_container_width=True,
        #     hide_index=True,
        #     column_config={
        #         "singular_name_short": st.column_config.TextColumn(
        #             "POS"
        #         ),
        #         "name": st.column_config.TextColumn(
        #             "team"
        #         )
        #     }
        # )
        
        # Updated final result
        
        
        # Keep all columns available for calculating colors
        # display_source = result.head(top_n).copy()

        # # Apply percentile-based colors
        # styled_result = display_source.style.apply(
        #     color_opponents,
        #     axis=1
        # )

        # # Show only the columns selected by the user
        # styled_result = styled_result.hide(
        #     subset=[
        #         col for col in display_source.columns
        #         if col not in selected_columns
        #     ],
        #     axis="columns"
        # )
        
        # Abobe portion is replaced by below portion to display selected columns
        
        
        # Keep all columns available for calculating colors
        display_source = result.head(top_n).copy()

        # Calculate colors using the full dataset
        styles = display_source.apply(
            color_opponents,
            axis=1,
            result_type="expand"
        )

        styles.columns = display_source.columns

        # Select only the requested columns
        final_result = display_source[selected_columns].copy()

        # Apply the previously calculated styles
        styled_result = final_result.style.apply(
            lambda _: styles[selected_columns],
            axis=None
        )


        
        # End of display selected columns

        # Display the styled results
        # st.dataframe(
        #     styled_result,
        #     use_container_width=True,
        #     hide_index=True,
        #     column_config={
        #         "singular_name_short": st.column_config.TextColumn("POS"),
        #         "name": st.column_config.TextColumn("team")
        #     }
        # )
        
        # Below part is the replacement of above to accomodate integer and float
        
        
        # Numeric column formatting
        column_config = {
            "singular_name_short": st.column_config.TextColumn("POS"),
            "name": st.column_config.TextColumn("team")
        }

        # Columns containing decimal-valued statistics
        decimal_keywords = ["egi", "egc", "egs", "expected", "xg", "xa"]

        # Columns containing integer-valued statistics
        integer_keywords = [
            "points", "goals", "assists", "minutes",
            "saves", "cs", "dc", "gc", "gs",
            "round", "id_player"
        ]

        for col in selected_columns:

            if not pd.api.types.is_numeric_dtype(final_result[col]):
                continue

            col_lower = col.lower()
            parts = col_lower.split("_")

            if any(keyword in parts for keyword in decimal_keywords):
                column_config[col] = st.column_config.NumberColumn(
                    col,
                    format="%.2f"
                )

            elif any(keyword in parts for keyword in integer_keywords):
                column_config[col] = st.column_config.NumberColumn(
                    col,
                    format="%d"
                )

            else:
                column_config[col] = st.column_config.NumberColumn(
                    col,
                    format="%.2f"
                )

        # Display styled results
        st.dataframe(
            styled_result,
            use_container_width=True,
            hide_index=True,
            column_config=column_config
        )

        
        # End of integer and float
        
        

        # Preserve the original CSV download functionality
        final_result = display_source[selected_columns]

        
        
        # Updated final result end

        

        # Download filtered results
        csv = final_result.to_csv(index=False)

        st.download_button(
            "Download Results as CSV",
            data=csv,
            file_name="fpl_results.csv",
            mime="text/csv"
        )
