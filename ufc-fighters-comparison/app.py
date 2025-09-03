import streamlit as st
import pandas as pd
import os # Import the 'os' module

# --- Functions ---

@st.cache_data
def load_data(file_name):
    """
    Loads data from a CSV file located in the same directory as the script.
    This is a more robust way to find the file.
    """
    # Get the absolute path of the directory where this script is located
    script_dir = os.path.dirname(__file__)
    # Join the script's directory path with the file name to create an absolute path
    file_path = os.path.join(script_dir, file_name)

    try:
        df = pd.read_csv(file_path)
        return df
    except FileNotFoundError:
        st.error(f"Error: The data file '{file_name}' was not found.")
        st.warning(f"Please make sure your data file is in the same folder as your script. I was looking for it at: {file_path}")
        st.stop() # Stop the app if the file can't be found.

def get_fighter_stat(df, fighter_name, feature_name):
    """Safely retrieves a single statistic for a given fighter."""
    fighter_data = df[df['name'] == fighter_name]
    if fighter_data.empty:
        return None
    value = fighter_data.iloc[0].get(feature_name, None)
    return value

# --- Page Configuration ---
st.set_page_config(page_title="UFC Fighter Comparison", layout="wide", initial_sidebar_state="expanded")

# --- Load Data ---
# Now we call the function with just the file name
df = load_data('ufc-fighters-statistics-CLEANED.csv')

# --- Sidebar Content ---
st.sidebar.title("ℹ️ About")
st.sidebar.info(
    """
    This app allows you to compare the statistics of two UFC fighters
    head-to-head across a variety of metrics.
    """
)
st.sidebar.subheader("How to Use")
st.sidebar.markdown(
    """
    1.  Select **Fighter 1** from the first dropdown.
    2.  Select **Fighter 2** from the second dropdown.
    3.  Choose a **Feature to Compare**.
    4.  View the results and detailed stats below.
    """
)
st.sidebar.subheader("Data Source")
st.sidebar.markdown(
    "The data is from a public Kaggle dataset: "
    "[UFC Fighters Statistics](https://www.kaggle.com/datasets/rajeevw/ufcdata)."
)

# --- Main Page ---
st.title("🥊 UFC Fighter Comparison")
st.markdown("Select two fighters and a statistic to see how they stack up against each other.")

# --- Fighter & Feature Selection ---
col1, col2, col3 = st.columns(3)

fighter_names = sorted(df['name'].dropna().unique())

with col1:
    default_fighter_1 = "Jon Jones"
    default_index_1 = fighter_names.index(default_fighter_1) if default_fighter_1 in fighter_names else 0
    fighter1 = st.selectbox("Select Fighter 1", fighter_names, index=default_index_1, key="fighter1")

with col2:
    fighter2_options = [f for f in fighter_names if f != fighter1]
    default_fighter_2 = "Anderson Silva"
    default_index_2 = fighter2_options.index(default_fighter_2) if default_fighter_2 in fighter2_options else 0
    fighter2 = st.selectbox("Select Fighter 2", fighter2_options, index=default_index_2, key="fighter2")

features = [
    'age', 'height_cm', 'weight_in_kg', 'reach_in_cm', 'stance',
    'significant_strikes_landed_per_minute', 'significant_striking_accuracy',
    'significant_strikes_absorbed_per_minute', 'significant_strike_defence',
    'average_takedowns_landed_per_15_minutes', 'takedown_accuracy',
    'takedown_defense', 'average_submissions_attempted_per_15_minutes',
    'wins', 'losses', 'draws'
]
features_in_data = [f for f in features if f in df.columns]
with col3:
    default_feature_index = 5 if len(features_in_data) > 5 else 0
    feature = st.selectbox("Select Feature to Compare", features_in_data, index=default_feature_index)

# --- Comparison Logic ---
fighter1_stat = get_fighter_stat(df, fighter1, feature)
fighter2_stat = get_fighter_stat(df, fighter2, feature)

st.write("---")
st.subheader(f"📊 Head-to-Head: {feature.replace('_', ' ').title()}")

is_numeric = pd.api.types.is_numeric_dtype(df[feature]) and fighter1_stat is not None and fighter2_stat is not None

metric_col1, metric_col2 = st.columns(2)

with metric_col1:
    st.markdown(f"### {fighter1}")
    if is_numeric:
        delta = fighter1_stat - fighter2_stat
        lower_is_better = any(s in feature for s in ['absorbed', 'losses'])
        st.metric(
            label=feature.replace('_', ' ').title(),
            value=f"{fighter1_stat:.2f}",
            delta=f"{delta:.2f}",
            delta_color="inverse" if lower_is_better else "normal"
        )
    else:
        st.metric(label=feature.replace('_', ' ').title(), value=str(fighter1_stat))

with metric_col2:
    st.markdown(f"### {fighter2}")
    if is_numeric:
        delta = fighter2_stat - fighter1_stat
        lower_is_better = any(s in feature for s in ['absorbed', 'losses'])
        st.metric(
            label=feature.replace('_', ' ').title(),
            value=f"{fighter2_stat:.2f}",
            delta=f"{delta:.2f}",
            delta_color="inverse" if lower_is_better else "normal"
        )
    else:
        st.metric(label=feature.replace('_', ' ').title(), value=str(fighter2_stat))

# --- Fighter Details Table ---
st.write("---")
st.write("###  Fighter Details")
display_cols = ['wins', 'losses', 'draws', 'age', 'stance', 'height_cm', 'weight_in_kg']
fighter_details = df[df['name'].isin([fighter1, fighter2])].set_index('name')
final_cols = [col for col in display_cols if col in fighter_details.columns]
st.dataframe(fighter_details[final_cols].fillna(0))

