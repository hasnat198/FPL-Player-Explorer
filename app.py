
import pandas as pd
import streamlit as st

# updated below 2 lines on 19th November, 2026 to include top 15 player graphics

import streamlit.components.v1 as components
from html import escape

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

# with st.expander("🎨 Color Coding", expanded=False):

#     st.markdown("""
#     ### How does the color coding work?

#     The upcoming opponent columns (`next1gw_opponent`
#     through `next4gw_opponent`) are color-coded based
#     exclusively on **expected goals conceded (EGC)**.

#     - **Lower EGC:** Indicates a stronger defense,
#       making the fixture potentially more difficult
#       for attacking players.
#     - **Higher EGC:** Indicates a weaker defense,
#       making the fixture potentially more favorable
#       for attacking players.
#     - **Percentile ranking:** Each opponent is ranked
#       relative to other opponents using their EGC.
#     - **Separate gameweeks:** Percentile rankings are
#       calculated separately for each of the next
#       four gameweeks.

#     ### Color legend
#     """)

#     color_legend = [
#         ("#F4B6B6", "0–20%", "Very strong", "Very difficult"),
#         ("#F8CBAA", "20–40%", "Strong", "Difficult"),
#         ("#FFE6A1", "40–60%", "Average", "Moderate"),
#         ("#D8EDB2", "60–80%", "Weak", "Favorable"),
#         ("#B9E8C5", "80–100%", "Very weak", "Very favorable")
#     ]

#     st.markdown(
#         "| Color | EGC Percentile | Defensive Strength | Attacking Fixture |\n"
#         "|---|---|---|---|\n"
#         + "\n".join(
#             f"| <span style='display:inline-block;"
#             f"background-color:{color};width:45px;"
#             f"height:18px;border-radius:4px;'>&nbsp;</span> "
#             f"| {percentile} | {strength} | {difficulty} |"
#             for color, percentile, strength, difficulty
#             in color_legend
#         ),
#         unsafe_allow_html=True
#     )

#     st.markdown("""
#     ### Important considerations

#     - The colors reflect **defensive strength only**,
#       measured by expected goals conceded.
#     - They do not incorporate the opponent's attacking
#       strength, home or away advantage, injuries,
#       player form, or other match conditions.
#     - A green fixture does not guarantee high FPL points.
#     - The same opponent can have a different color
#       across gameweeks if its relative EGC ranking changes.

#     **Interpretation:** Red represents a stronger defense,
#     while green represents a weaker defense.
#     """)

with st.expander("🎨 Color Coding", expanded=False):

    st.markdown("""
    ### How does the color coding work?

    The upcoming opponent performance columns
    (`gc`, `egc`, `gs`, `egs`) are color-coded
    based on their individual percentile rankings.

    The opponent name columns are not color-coded.

    - **GC:** Goals conceded by the opponent.
    - **EGC:** Expected goals conceded by the opponent.
    - **GS:** Goals scored by the opponent.
    - **EGS:** Expected goals scored by the opponent.

    Higher GC and EGC indicate weaker defensive performance.

    Higher GS and EGS indicate stronger attacking performance.

    Percentile rankings are calculated separately
    for each metric and gameweek.

    ### Color legend
    """)

    color_legend = [
        ("#F4B6B6", "0–20%", "Very difficult"),
        ("#F8CBAA", "20–40%", "Difficult"),
        ("#FFE6A1", "40–60%", "Moderate"),
        ("#D8EDB2", "60–80%", "Favorable"),
        ("#B9E8C5", "80–100%", "Very favorable")
    ]

    st.markdown(
        "| Color | Percentile | Fixture Difficulty |\n"
        "|---|---|---|\n"
        + "\n".join(
            f"| <span style='display:inline-block;"
            f"background-color:{color};width:45px;"
            f"height:18px;border-radius:4px;'>&nbsp;</span> "
            f"| {percentile} | {difficulty} |"
            for color, percentile, difficulty
            in color_legend
        ),
        unsafe_allow_html=True
    )

    st.markdown("""
    ### Important considerations

    - Each performance metric is ranked independently.
    - Red indicates a more difficult opponent.
    - Green indicates a more favorable opponent.
    - Defensive and attacking metrics use opposite
      percentile directions.
    - Rankings are calculated separately for
      each of the next four gameweeks.
    - Colors indicate relative team performance,
      not guaranteed FPL points.
    """)


# End of color coding
st.caption("Explore player performance, recent form and upcoming opponents. To start, hit the Show Results button.")

# Load your existing calculated data
@st.cache_data
def load_data():
    return pd.read_csv("points_f.csv")

df = load_data()

# updated below lines on 19th November, 2026 to include top 15 player graphics

# =====================================================
# TOP PLAYERS NEXT GAMEWEEK - PITCH VIEW
# =====================================================

@st.cache_data(ttl=300)
def load_top_players():
    return pd.read_csv("top_players_next_gw.csv")

# New football pitch function and display section
# Insert the remaining code from squad_block.txt here.

# =====================================================
# TOP PLAYERS NEXT GAMEWEEK - PITCH VIEW
# =====================================================

@st.cache_data(ttl=300)
def load_top_players():
    return pd.read_csv("top_players_next_gw.csv")


def show_top_players_pitch(players):
    required = {"web_name", "photo_url", "singular_name_short"}
    missing = required - set(players.columns)
    if missing:
        st.warning("Squad CSV missing columns: " + ", ".join(sorted(missing)))
        return

    def clean(value):
        return "" if pd.isna(value) else str(value).strip()

    def safe(value):
        return escape(clean(value), quote=True)

    positions = players["singular_name_short"].astype(str).str.strip().str.upper()
    rows = []
    for pos in ["GKP", "DEF", "MID", "FWD"]:
        cards = []
        for _, player in players.loc[positions == pos].iterrows():
            name = safe(player["web_name"])
            url = clean(player["photo_url"])
            photo = (f'<img src="{escape(url, quote=True)}" alt="{name}">'
                     if url.startswith(("https://", "http://")) else '<div class="no-photo">No photo</div>')
            price = pd.to_numeric(player.get("current_price"), errors="coerce")
            price_text = f"£{price:.1f}m" if pd.notna(price) else ""
            prediction = pd.to_numeric(player.get("predicted_point"), errors="coerce")
            points = f"{prediction:.2f} pts" if pd.notna(prediction) else ""
            opponent = safe(player.get("next1gw_opponent"))
            availability = clean(player.get("availability")).lower()
            status = "unavailable" if availability in ["injured", "suspended"] else "doubtful" if availability == "doubtful" else ""
            cards.append(f'''<div class="player">
                <div class="price">{price_text}</div>{photo}
                <div class="name {status}">{name}</div>
                <div class="fixture">{opponent}</div>
                <div class="points">{points}</div></div>''')
        rows.append(f'<div class="position-row">{"".join(cards)}</div>')

    html = '''<!doctype html><html><head><meta name="viewport" content="width=device-width, initial-scale=1"><style>
    *{box-sizing:border-box} body{margin:0;font-family:Arial,sans-serif;background:#24062e}
    .pitch{position:relative;overflow:hidden;max-width:960px;margin:auto;padding:12px 8px 18px;border-radius:12px;background:repeating-linear-gradient(0deg,#009b4e 0px,#009b4e 70px,#00a655 70px,#00a655 140px)}
    .banner{position:relative;text-align:center;background:linear-gradient(90deg,#00e4ec,#6879fa);color:#280833;font-weight:800;padding:10px;border-radius:8px;margin:0 8% 8px}
    .lines{position:absolute;inset:52px 0 0;width:100%;height:calc(100% - 52px);pointer-events:none}
    .position-row{position:relative;display:flex;justify-content:center;align-items:flex-start;flex-wrap:wrap;gap:clamp(5px,2vw,22px);min-height:155px;padding:7px 0}
    .player{width:clamp(55px,16vw,112px);text-align:center;border:1px solid #ffffff35;border-radius:5px;overflow:hidden;background:#07563788;color:white;font-size:12px;box-shadow:0 2px 5px #0002}
    .price{height:20px;font-weight:bold;padding:3px}.player img,.no-photo{width:100%;height:85px;object-fit:contain;display:block}.no-photo{padding-top:30px;font-size:10px}
    .name,.fixture,.points{background:#fff;color:#300b3b;padding:3px 2px;overflow-wrap:anywhere}.name{font-weight:bold}.fixture{background:#f0edf3;font-size:11px}.points{font-weight:bold;font-size:11px}.points:empty{display:none}.name.unavailable{background:#ff7777}.name.doubtful{background:#ffd700}
    </style></head><body><div class="pitch"><div class="banner">⚽ Top Players · Next Gameweek</div>
    <svg class="lines" viewBox="0 0 800 640" preserveAspectRatio="none" aria-hidden="true"><g stroke="white" stroke-width="2.5" fill="none" opacity=".85"><path d="M135 8 H665 L795 635 H5 Z"/><path d="M285 8 L265 105 H535 L515 8 M345 8 V44 H455 V8"/><path d="M68 340 H732"/><ellipse cx="400" cy="340" rx="90" ry="60"/><path d="M240 635 L255 535 H545 L560 635 M345 635 V600 H455 V635"/></g></svg>'''
    html += "".join(rows) + "</div></body></html>"
    # Allow enough vertical room if a position contains extra players.
    import math
    height = 95 + sum(180 * max(1, math.ceil(int((positions == pos).sum()) / 5)) for pos in ["GKP", "DEF", "MID", "FWD"])
    components.html(html, height=height, scrolling=True)
    if (~positions.isin(["GKP", "DEF", "MID", "FWD"])).any():
        st.caption("Rows with unrecognized positions were omitted from the pitch.")


with st.expander("⚽ Top Players for Next Gameweek", expanded=True):
    try:
        top_players = load_top_players()
    except (FileNotFoundError, pd.errors.EmptyDataError, pd.errors.ParserError) as exc:
        st.warning(f"Unable to load top_players_next_gw.csv: {exc}")
    else:
        show_top_players_pitch(top_players)



# =====================================================
# COLOR CODE NEXT 4 GAMEWEEK OPPONENTS BY xGC PERCENTILE
# =====================================================

# =====================================================
# COLOR CODE NEXT 4 GAMEWEEK OPPONENTS BY xGC PERCENTILE
# =====================================================

# # Calculate percentile reference values using unique opponents
# opponent_percentiles = {}

# for gw in range(1, 5):
#     opponent_col = f"next{gw}gw_opponent"
#     egc_col = f"next{gw}gw_egc"

#     if opponent_col in df.columns and egc_col in df.columns:

#         # Each opponent contributes only once per gameweek
#         unique_opponents = df[
#             [opponent_col, egc_col]
#         ].copy()

#         unique_opponents[egc_col] = pd.to_numeric(
#             unique_opponents[egc_col],
#             errors="coerce"
#         )

#         unique_opponents = (
#             unique_opponents
#             .dropna(subset=[opponent_col, egc_col])
#             .drop_duplicates(subset=[opponent_col])
#         )

#         opponent_percentiles[egc_col] = (
#             unique_opponents[egc_col]
#             .rank(pct=True, method="average") * 100
#         )

#         # Store xGC values for comparison
#         opponent_percentiles[egc_col] = (
#             unique_opponents[egc_col]
#             .reset_index(drop=True)
#         )

# =====================================================
# COLOR CODE NEXT 4 GAMEWEEK PERFORMANCE STATISTICS
# =====================================================

# Calculate percentile reference values using unique opponents
opponent_percentiles = {}

for gw in range(1, 5):

    opponent_col = f"next{gw}gw_opponent"

    for metric in ["gc", "egc", "gs", "egs"]:

        metric_col = f"next{gw}gw_{metric}"

        if opponent_col in df.columns and metric_col in df.columns:

            # Each opponent contributes only once per gameweek
            unique_opponents = df[
                [opponent_col, metric_col]
            ].copy()

            unique_opponents[metric_col] = pd.to_numeric(
                unique_opponents[metric_col],
                errors="coerce"
            )

            unique_opponents = (
                unique_opponents
                .dropna(subset=[opponent_col, metric_col])
                .drop_duplicates(subset=[opponent_col])
            )

            # Store metric values for percentile comparison
            opponent_percentiles[metric_col] = (
                unique_opponents[metric_col]
                .reset_index(drop=True)
            )


# def color_opponents(row):

#     styles = [""] * len(row)

#     for gw in range(1, 5):

#         opponent_col = f"next{gw}gw_opponent"
#         egc_col = f"next{gw}gw_egc"

#         if opponent_col not in row.index:
#             continue

#         if egc_col not in row.index:
#             continue

#         egc = pd.to_numeric(
#             row[egc_col], errors="coerce"
#         )

#         if pd.isna(egc):
#             continue

#         reference = opponent_percentiles.get(egc_col)

#         if reference is None or reference.empty:
#             continue

#         # Percentile ranking against unique opponents
#         percentile = (reference <= egc).mean() * 100

#         if percentile <= 20:
#             color = "#F4B6B6"  # Red
#         elif percentile <= 40:
#             color = "#F8CBAA"  # Orange
#         elif percentile <= 60:
#             color = "#FFE6A1"  # Yellow
#         elif percentile <= 80:
#             color = "#D8EDB2"  # Light green
#         else:
#             color = "#B9E8C5"  # Green

#         idx = row.index.get_loc(opponent_col)

#         styles[idx] = (
#             f"background-color: {color}; "
#             "color: #202020"
#         )

#     return styles

def color_opponents(row):

    styles = [""] * len(row)
    
    # web_name change color based on player availability;
    
    # Color player name based on availability
    if "availability" in row.index and "web_name" in row.index:

        availability = str(row["availability"]).strip().lower()

        if availability in ["suspended", "injured"]:
            name_color = "#FF0000"  # Red

        elif availability == "doubtful":
            name_color = "#FFD700"  # Yellow

        else:
            name_color = None

        if name_color is not None:
            idx = row.index.get_loc("web_name")

            styles[idx] = (
                f"background-color: {name_color}; "
                "color: #202020"
            )

    for gw in range(1, 5):

        for metric in ["gc", "egc", "gs", "egs"]:

            metric_col = f"next{gw}gw_{metric}"

            if metric_col not in row.index:
                continue

            value = pd.to_numeric(
                row[metric_col], errors="coerce"
            )

            if pd.isna(value):
                continue

            reference = opponent_percentiles.get(metric_col)

            if reference is None or reference.empty:
                continue

            # Percentile ranking against unique opponents
            percentile = (reference <= value).mean() * 100

            # For defensive metrics, higher values are favorable
            # For attacking metrics, lower values are favorable

            if metric in ["gs", "egs"]:
                percentile = 100 - percentile

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

            idx = row.index.get_loc(metric_col)

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
    "predicted_point",
    "current_price",
    "egi_last3",
    "goals_last3",
    "assists_last3",
    "egi_last2",
    "goals_last2",
    "assists_last2",
    "next1gw_opponent",
    "next1gw_gc",
    "next1gw_egc",
    "next1gw_gs",
    "next1gw_egs",
    "next2gw_opponent",
    "next2gw_gc",
    "next2gw_egc",
    "next2gw_gs",
    "next2gw_egs"
]

default_columns = [
    c for c in default_columns if c in df.columns
]

# -----------------------------
# FIRST FILTER
# -----------------------------

# st.subheader("1. Filter Players")

# col1, col2 = st.columns(2)

# with col1:
#     filter_column = st.selectbox(
#         "Filter Column",
#         ["No Filter"] + list(df.columns)
#     )

# with col2:
#     filter_value = st.text_input(
#         "Filter Value",
#         placeholder="Enter a value"
#     )

# # -----------------------------
# # SECOND FILTER
# # -----------------------------

# st.subheader("2. Numeric Filter")

# numeric_columns = df.select_dtypes(
#     include="number"
# ).columns.tolist()

# col3, col4, col5 = st.columns(3)

# with col3:
#     second_filter_column = st.selectbox(
#         "2nd Filter Column",
#         ["No Filter"] + numeric_columns
#     )

# with col4:
#     operator = st.selectbox(
#         "Comparison",
#         [">", "<", ">=", "<=", "=="]
#     )

# with col5:
#     second_filter_value = st.number_input(
#         "2nd Filter Value",
#         value=0.0
#     )

# # -----------------------------
# # SORTING
# # -----------------------------

# st.subheader("3. Sort Results")

# col6, col7, col8 = st.columns(3)

# with col6:
#     sort_column = st.selectbox(
#         "Sort Column",
#         list(df.columns),
#         index=(
#             list(df.columns).index("points_last3")
#             if "points_last3" in df.columns else 0
#         )
#     )

# with col7:
#     sort_order = st.selectbox(
#         "Sort Order",
#         ["Descending", "Ascending"]
#     )

# with col8:
#     top_n = st.number_input(
#         "Top N Rows",
#         min_value=1,
#         max_value=max(1, len(df)),
#         value=min(10, max(1, len(df))),
#         step=1
#     )

# =====================================================
# FILTERING AND SORTING - SINGLE ROW LAYOUT
# =====================================================

# filter1, filter2, filter3 = st.columns([1, 1.5, 1.5])

# filter1 column hidden
filter3, filter2 = st.columns([1, 1])

# -----------------------------
# FIRST FILTER
# -----------------------------

# with filter1:

    # st.subheader("1. Filter Players")

    # filter_column = st.selectbox(
    #     "Filter Column",
    #     ["No Filter"] + list(df.columns)
    # )

    # filter_value = st.text_input(
    #     "Filter Value",
    #     placeholder="Enter a value"
    # )
    
# First filter disabled
filter_column = "No Filter"
filter_value = ""


# -----------------------------
# SECOND FILTER
# -----------------------------

with filter2:

    st.subheader("2. Condition")

    numeric_columns = df.select_dtypes(
        include="number"
    ).columns.tolist()

    second_filter_column = st.selectbox(
        "Column",
        ["No Filter"] + numeric_columns
    )

    col4, col5 = st.columns(2)

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

with filter3:

    st.subheader("1. Sort")

    sort_column = st.selectbox(
        "Column",
        list(df.columns),
        index=(
            list(df.columns).index("predicted_point")
            if "points_last3" in df.columns else 0
        )
    )

    col7, col8 = st.columns(2)

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
        # final_result = display_source[selected_columns].copy()
        
        
        # Select only the requested columns
        final_result = display_source[selected_columns].copy()

        # Add player photo as the first column
        if "photo_url" in display_source.columns:

            # Avoid duplicate photo columns
            final_result = final_result.drop(
                columns=["photo_url"],
                errors="ignore"
            )

            final_result.insert(
                0,
                "photo_url",
                display_source["photo_url"]
            )


        # Apply the previously calculated styles
        # styled_result = final_result.style.apply(
        #     lambda _: styles[selected_columns],
        #     axis=None
        # )
        
        
        # Apply previously calculated opponent colors
        # Include the new photo column in the style matrix

        display_columns = final_result.columns.tolist()

        photo_styles = styles.reindex(
            index=final_result.index,
            columns=display_columns,
            fill_value=""
        )

        styled_result = final_result.style.apply(
            lambda _: photo_styles,
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
        # column_config = {
        #     "singular_name_short": st.column_config.TextColumn("POS"),
        #     "name": st.column_config.TextColumn("team")
        # }
        
        
        column_config = {
            "photo_url": st.column_config.ImageColumn(
                "Photo",
                help="Player photograph",
                width="small"
            ),
            "singular_name_short": st.column_config.TextColumn("POS"),
            "name": st.column_config.TextColumn("team"),
            "current_price": st.column_config.NumberColumn(
                "price",
                format="%.1f"
            )
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
            
            # Preserve custom column configurations
            if col in ["current_price"]:
                continue

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
