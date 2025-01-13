import streamlit as st
import pickle
import pandas as pd

# Load the saved Logistic Regression model and transformer
with open('output/model.pkl', 'rb') as model_file:
    model = pickle.load(model_file)

with open('output/transformer.pkl', 'rb') as transformer_file:
    trf = pickle.load(transformer_file)

# Function to predict probability using model and transformer
def predict_probability(model, trf, data):
    # Convert data to DataFrame format
    data = pd.DataFrame([data])


    data['run_left'] = data['first_inning_run'] - data['current_runs']
    data['crr'] = (data['current_runs'] * 6) / (120 - data['ball_left'])
    data['rrr'] = (data['run_left'] * 6) / data['ball_left']
    
    # Transform data using the trained transformer
    data_transformed  = trf.transform(data)
    
     # Ensure transformed data is a numpy array
    data_transformed = data_transformed .toarray() if hasattr(data_transformed, "toarray") else data_transformed
    
    
    # Predict probability for class 1
    probability = model.predict_proba(data_transformed)[:, 1][0]
    
    return probability

# Streamlit UI
st.title("IPL Win Probability Predictor")
st.write("Enter the match details below:")

# Inputs for the match details
batting_team = st.selectbox("Batting Team", ['Select Team','Chennai Super Kings', 'Mumbai Indians', 'Royal Challengers Bangalore', 'Kolkata Knight Riders', 'Delhi Capitals', 'Kings XI Punjab', 'Sunrisers Hyderabad', 'Rajasthan Royals'], index=0)
bowling_team = st.selectbox("Bowling Team",['Select Team','Chennai Super Kings', 'Mumbai Indians', 'Royal Challengers Bangalore', 'Kolkata Knight Riders', 'Delhi Capitals', 'Kings XI Punjab', 'Sunrisers Hyderabad', 'Rajasthan Royals'], index=0)
if batting_team != 'Select Team' and bowling_team != 'Select Team':
    toss_winner_options = [batting_team, bowling_team]
else:
    toss_winner_options = ['Select Team']

# Toss winner selection (options filtered based on batting and bowling team)
toss_winner = st.selectbox(
    "Toss Winner",
    toss_winner_options,
    index=0  # Set default value to "Select Team"
)
if toss_winner == batting_team:
    toss_decision = 'field'  # Batting team wins toss, chooses to field
elif toss_winner == bowling_team:
    toss_decision = 'bat'  # Bowling team wins toss, chooses to bat
else:
    toss_decision = 'Select Decision'  # Default value if no toss winner selected

# Show the toss decision based on the winner
st.selectbox("Toss Decision", toss_decision)


ball_left = st.number_input("Balls Left", min_value=1, max_value=120, value= 30)
wicket_left = st.number_input("Wickets Left", min_value=1, max_value=10, value=7)
first_inning_run = st.number_input("First Inning Runs", min_value=0, max_value=500, value=207)
current_runs = st.number_input("Current Runs", min_value=0, max_value=500, value=180)

# Prediction button
if st.button("Predict Win Probability"):
    # Collect input data
    input_data = {
        'batting_team': batting_team,
        'bowling_team': bowling_team,
        'toss_winner': toss_winner,
        'toss_decision': toss_decision,
        'ball_left': ball_left,
        'wicket_left': wicket_left,
        'first_inning_run': first_inning_run,
        'current_runs': current_runs
    }
    
    # Predict win probability
    probability = predict_probability(model, trf, input_data)
    
    # Display result
    st.write(f"Probability of winning for the batting team: {probability:.2%}")
