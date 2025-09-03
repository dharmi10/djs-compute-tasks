import streamlit as st
import pandas as pd

data = pd.read_csv(r"C:\Users\User\ufc-fighters-statistics-CLEANED.csv")
st.set_page_config(page_title="Fighter Comparison", layout="wide")

st.title("🥊 UFC Fighter Comparison App")
st.sidebar.title("ℹ️ About")
st.sidebar.info(
    """
    This app allows you to compare the statistics of UFC fighters.
    Select two fighters and a feature from the main page to see a
    head-to-head comparison.
    """
)
st.sidebar.subheader("Data Source")
st.sidebar.markdown(
    "The data is from a public Kaggle dataset: "
    "[UFC Fighters Statistics](https://www.kaggle.com/datasets/rajeevw/ufcdata)."
)
col1, col2, col3 = st.columns(3)

fighter_names = data['name'].dropna().unique()

with col1:
    fighter1 = st.selectbox("Select Fighter 1", fighter_names, index=0)

with col2:
    fighter2 = st.selectbox("Select Fighter 2", fighter_names, index=1)


features = [
    'age', 'height_cm', 'weight_in_kg', 'reach_in_cm', 'stance',
    'significant_strikes_landed_per_minute',
    'significant_striking_accuracy',
    'significant_strikes_absorbed_per_minute',
    'significant_strike_defence',
    'average_takedowns_landed_per_15_minutes',
    'takedown_accuracy', 'takedown_defense',
    'average_submissions_attempted_per_15_minutes',
    'win_rate',
    'loss_rate',
    'win_loss_ratio'
    
]

features = [f for f in features if f in data.columns]

with col3:
    feature = st.selectbox("Select Feature to Compare", features)

def get_fighter_stat(fighter_name, feature_name):
    fighter_data = data.loc[data['name'] == fighter_name]
    if fighter_data.empty:
        return "N/A"
    value = fighter_data.iloc[0].get(feature_name, "N/A")
    if pd.isna(value):
        if pd.api.types.is_numeric_dtype(data[feature_name]):
            value = 0
        else:
            value = "N/A"
    return value


fighter1_value = get_fighter_stat(fighter1, feature)
fighter2_value = get_fighter_stat(fighter2, feature)


st.subheader(f"📊 Comparing '{fighter1}' vs '{fighter2}' on '{feature}'")
metric_col1, metric_col2 = st.columns(2)

with metric_col1:

    if pd.api.types.is_numeric_dtype(data[feature]):
        st.metric(label=fighter1, value=round(fighter1_value, 2))
    else:
        st.markdown(f"### {fighter1}")
        st.write(f"**{feature.replace('_', ' ').title()}:** {fighter1_value}")

with metric_col2:
    if pd.api.types.is_numeric_dtype(data[feature]):
        st.metric(label=fighter2, value=round(fighter2_value, 2))
    else:
        st.markdown(f"### {fighter2}")
        st.write(f"**{feature.replace('_', ' ').title()}:** {fighter2_value}")

st.write("---") 
st.write("### Fighter Details")
st.dataframe(
    data[data['name'].isin([fighter1, fighter2])][['name', 'wins', 'losses', 'draws']].fillna(0)
)