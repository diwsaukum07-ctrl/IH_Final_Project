import base64
import streamlit as st
import pandas as pd
import joblib


def add_background(image_file):

    with open(image_file, "rb") as file:
        encoded = base64.b64encode(file.read()).decode()

    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image:
                linear-gradient(rgba(0,0,0,0.75), rgba(0,0,0,0.75)),
                url("data:image/jpg;base64,{encoded}");

            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        }}

        h1, h2, h3 {{
            color: white;
        }}

        p {{
            color: white;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

add_background("background.jpeg")



# Page title
st.title("Dota 2 Match Outcome Predictor")

st.write("Select 5 Radiant heroes and 5 Dire heroes.")


# Load model
model = joblib.load("dota_model.pkl")

# Load feature columns
feature_columns = joblib.load("feature_columns.pkl")

# Load heroes dataset
heroes = pd.read_csv("heroes_cleaned.csv")


# Hero names for dropdowns
hero_names = heroes["localized_name"].tolist()


# -----------------------------
# Radiant team
# -----------------------------

radiant_col, dire_col = st.columns(2)

with radiant_col:

    st.subheader("🟢 RADIANT")

    radiant_1 = st.selectbox("Carry", hero_names, key="r1")
    radiant_2 = st.selectbox("Mid", hero_names, key="r2")
    radiant_3 = st.selectbox("Tank", hero_names, key="r3")
    radiant_4 = st.selectbox("Support 1", hero_names, key="r4")
    radiant_5 = st.selectbox("Support 2", hero_names, key="r5")


# -----------------------------
# Dire team
# -----------------------------

with dire_col:

    st.subheader("🔴 DIRE")

    dire_1 = st.selectbox("Carry", hero_names, key="d1")
    dire_2 = st.selectbox("Mid", hero_names, key="d2")
    dire_3 = st.selectbox("Tank", hero_names, key="d3")
    dire_4 = st.selectbox("Support 1", hero_names, key="d4")
    dire_5 = st.selectbox("Support 2", hero_names, key="d5")

# Store selected teams
radiant_team = [
    radiant_1,
    radiant_2,
    radiant_3,
    radiant_4,
    radiant_5
]

dire_team = [
    dire_1,
    dire_2,
    dire_3,
    dire_4,
    dire_5
]


# -----------------------------
# Prediction
# -----------------------------

if st.button("Predict Winner"):

    all_selected = radiant_team + dire_team

    # Check duplicate heroes
    if len(set(all_selected)) < 10:

        st.warning("Please select 10 different heroes.")

    else:

        # Create one empty row
        # All heroes start at 0
        input_data = pd.DataFrame(
            [[0] * len(feature_columns)],
            columns=feature_columns
        )


        # Radiant heroes = 1
        for hero_name in radiant_team:

            hero_id = heroes.loc[
                heroes["localized_name"] == hero_name,
                "hero_id"
            ].values[0]

            hero_column = f"hero_{hero_id}"

            if hero_column in input_data.columns:
                input_data.loc[0, hero_column] = 1


        # Dire heroes = -1
        for hero_name in dire_team:

            hero_id = heroes.loc[
                heroes["localized_name"] == hero_name,
                "hero_id"
            ].values[0]

            hero_column = f"hero_{hero_id}"

            if hero_column in input_data.columns:
                input_data.loc[0, hero_column] = -1


        # Predict winner
        prediction = model.predict(input_data)[0]


        # Predict probabilities
        probabilities = model.predict_proba(input_data)[0]

        dire_probability = probabilities[0]
        radiant_probability = probabilities[1]


        # Display result
        st.subheader("Prediction")

        if prediction == 1:
            st.success("Radiant is predicted to win!")
        else:
            st.success("Dire is predicted to win!")


        st.write(
            f"Radiant win probability: {radiant_probability * 100:.2f}%"
        )

        st.write(
            f"Dire win probability: {dire_probability * 100:.2f}%"
        )