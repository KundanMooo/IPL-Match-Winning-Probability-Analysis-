import pandas as pd
import numpy as np

def preprocess_ipl_data(matches_file, deliveries_file, output_file):
    # Load data
    match = pd.read_csv(matches_file)
    delivery = pd.read_csv(deliveries_file)

    # Filter first innings total scores
    total_score_df = delivery[delivery['inning'] == 1]
    total_score_df = total_score_df.groupby('match_id')['total_runs'].sum().reset_index()

    # Merge total scores with match data
    match_df = match.merge(total_score_df, left_on='id', right_on='match_id')

    # Team standardization
    teams = [
        'Royal Challengers Bengaluru',
        'Mumbai Indians',
        'Kolkata Knight Riders',
        'Chennai Super Kings',
        'Delhi Capitals',
        'Rajasthan Royals', 
        'Punjab Kings',
        'Sunrisers Hyderabad',
        'Lucknow Super Giants',
        'Gujarat Titans' 
    ]

    team_replacements = {
        'Delhi Daredevils': 'Delhi Capitals',
        'Deccan Chargers': 'Sunrisers Hyderabad',
        'Royal Challengers Bangalore': 'Royal Challengers Bengaluru',
        'Kings XI Punjab': 'Punjab Kings'
    }

    for old_team, new_team in team_replacements.items():
        match_df['team1'] = match_df['team1'].str.replace(old_team, new_team)
        match_df['team2'] = match_df['team2'].str.replace(old_team, new_team)

    # Filter matches with consistent teams
    match_df = match_df[match_df['team1'].isin(teams)]
    match_df = match_df[match_df['team2'].isin(teams)]

    # Merge deliveries with match data
    delivery_df = match_df.merge(delivery, left_on='id', right_on='match_id', how='inner')

    # Filter second innings
    delivery_df = delivery_df[delivery_df['inning'] == 2]
    delivery_df['total_runs_y'] = pd.to_numeric(delivery_df['total_runs_y'], errors='coerce')
    
    # Calculate match statistics
    delivery_df['current_score'] = delivery_df.groupby('id')['total_runs_y'].cumsum()
    delivery_df['runs_left'] = delivery_df['total_runs_x'] - delivery_df['current_score']
    delivery_df['balls_left'] = 120 - (delivery_df['over'] * 6 + delivery_df['ball'])
    delivery_df['player_dismissed'] = delivery_df['player_dismissed'].fillna(0).apply(lambda x: 0 if x == 0 else 1)

    def calculate_wickets_left(group):
        group['wickets'] = group['player_dismissed'].cumsum()
        group['wickets_left'] = 10 - group['wickets']
        return group

    delivery_df = delivery_df.groupby('id', group_keys=False).apply(calculate_wickets_left)

    # Add date
    delivery_df['date'] = pd.to_datetime(delivery_df['date'])

    # Calculate run rates
    delivery_df['crr'] = (delivery_df['current_score'] * 6) / (120 - delivery_df['balls_left'])
    delivery_df['rrr'] = (delivery_df['runs_left'] * 6) / delivery_df['balls_left']

    # Select relevant columns
    columns_to_keep = [
        'batting_team', 'date', 'bowling_team', 'toss_winner', 'toss_decision', 'city',
        'balls_left', 'wickets_left', 'total_runs_x', 'current_score', 'runs_left',
        'crr', 'rrr', 'winner'
    ]
    filtered_df = delivery_df[columns_to_keep]

    # Rename columns
    filtered_df = filtered_df.rename(columns={
        'balls_left': 'ball_left',
        'wickets_left': 'wicket_left',
        'total_runs_x': 'first_inning_run',
        'current_score': 'current_runs',
        'runs_left': 'run_left'
    })

    # Add winner column
    def function(row):
        return 1 if row['batting_team'] == row['winner'] else 0

    filtered_df['winner'] = filtered_df.apply(function, axis=1)

    # Drop unnecessary columns and rows
    filtered_df = filtered_df.drop(columns=['city'])
    filtered_df = filtered_df.dropna()

    # Filter for current teams
    all_current_teams = [
        'Sunrisers Hyderabad', 'Mumbai Indians', 'Royal Challengers Bengaluru',
        'Kolkata Knight Riders', 'Delhi Capitals', 'Punjab Kings',
        'Chennai Super Kings', 'Rajasthan Royals'
    ]
    filtered_df = filtered_df[filtered_df['batting_team'].isin(all_current_teams)]
    filtered_df = filtered_df[filtered_df['bowling_team'].isin(all_current_teams)]

    # Standardize toss winner names
    for old_team, new_team in team_replacements.items():
        filtered_df['toss_winner'] = filtered_df['toss_winner'].str.replace(old_team, new_team)

    filtered_df = filtered_df[filtered_df['ball_left'] != 0]

    # Save final dataframe to CSV
    filtered_df.to_csv(output_file, index=False)
    print(f'####*****=====Final preprocessed dataframe saved to {output_file}')

# Example usage
if __name__ == "__main__":
    preprocess_ipl_data("./data/matches.xls", "./data/deliveries.xls", "./output/pre_processed.csv")
