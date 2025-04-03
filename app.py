import streamlit as st
import pandas as pd
import pickle

# Team Data (Colors)
teams_data = {
    'Royal Challengers Bengaluru': {'color': '#D71920'},  # Red
    'Mumbai Indians': {'color': '#045093'},  # Blue
    'Gujarat Titans': {'color': '#003366'},  # Dark Blue
    'Delhi Capitals': {'color': '#17449B'},  # Blue
    'Punjab Kings': {'color': '#D71920'},  # Red
    'Sunrisers Hyderabad': {'color': '#FB6424'},  # Orange
    'Rajasthan Royals': {'color': '#EC4899'},  # **Pink**
    'Chennai Super Kings': {'color': '#F8CD3C'},  # Yellow
    'Lucknow Super Giants': {'color': '#265FA6'},  # Blue
    'Kolkata Knight Riders': {'color': '#3A225D'}  # Purple
}

cities = [
    'Mumbai', 'Kolkata', 'Jaipur', 'Chennai', 'Hyderabad', 'Ahmedabad',
    'Dharamsala', 'Visakhapatnam', 'Ranchi', 'Delhi', 'Bengaluru',
    'Navi Mumbai', 'Lucknow'
]

pipe = pickle.load(open('pipe.pkl', 'rb'))

# Set Title
st.markdown("<h1 style='text-align: center; color: #FF4500;'>🏏 IPL Win Predictor 🏆</h1>", unsafe_allow_html=True)

# Team Selection with Default Option
st.subheader("Select Teams")
col1, col2 = st.columns(2)
with col1:
    batting_team = st.selectbox('🏏 Select the Batting Team', ['Select Team'] + sorted(teams_data.keys()))
with col2:
    balling_team = st.selectbox('🎯 Select the Bowling Team', ['Select Team'] + sorted(teams_data.keys()))

# Default background color (light gray)
default_color = "#D3D3D3"

# Set color dynamically only if a team is selected
batting_color = teams_data.get(batting_team, {}).get('color', default_color)
bowling_color = teams_data.get(balling_team, {}).get('color', default_color)

# Set Background Color Effect
st.markdown(f"""
    <style>
        .stApp {{
            background: linear-gradient(to right, #4A90E2, #50E3C2);
            # background: linear-gradient(to right, #FF7E5F, #FEB47B);
            # background: linear-gradient(to right, #8A2BE2, #4B0082);
            # background: linear-gradient(to right, #0F2027, #00C9FF);



            transition: background 0.5s ease;
        }}
    </style>
""", unsafe_allow_html=True)

# Host City Selection
selected_city = st.selectbox('📍 Select Host City', sorted(cities))

# Match Inputs
st.subheader("Match Situation")
col3, col4, col5 = st.columns(3)

with col3:
    target = st.number_input('🎯 Target', min_value=1)
with col4:
    score = st.number_input('🏏 Current Score', min_value=0)
with col5:
    overs = st.number_input('⏳ Overs Completed', min_value=0.0, max_value=20.0, step=0.1)

wickets = st.slider('❌ Wickets Lost', 0, 10, 0)

# Prediction Button
if st.button('🔮 Predict Probability'):
    runs_left = target - score
    balls_left = 120 - (overs * 6)
    wickets_remaining = 10 - wickets
    crr = score / overs if overs > 0 else 0
    rrr = (runs_left * 6) / balls_left if balls_left > 0 else 0

    input_df = pd.DataFrame({
        'batting_team': [batting_team],
        'bowling_team': [balling_team],
        'city': [selected_city],
        'runs_left': [runs_left],
        'balls_left': [balls_left],
        'wickets': [wickets_remaining],
        'total_runs_x': [target],
        'crr': [crr],
        'rrr': [rrr]
    })

    result = pipe.predict_proba(input_df)
    win1_prob = result[0][0] * 100
    win_prob = result[0][1] * 100

    st.success(f"🏆 **{batting_team} Winning Probability:** {win_prob:.2f}%")
    st.error(f"🎯 **{balling_team} Winning Probability:** {win1_prob:.2f}%")
