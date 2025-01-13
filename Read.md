# IPL Match Win Probability Predictor

This project predicts the probability of a team winning an IPL match during the second innings based on current match statistics. The project includes data preprocessing, model training, and deployment using a web-based user interface built with Streamlit.

## Project Structure

```
|-- data/
|   |-- matches.xls           # Raw matches data
|   |-- deliveries.xls        # Raw deliveries data
|
|-- output/
|   |-- pre_processed.csv     # Preprocessed data for modeling
|   |-- model.pkl             # Trained Logistic Regression model
|   |-- transformer.pkl       # Trained data transformer
|
|--code
|   |-- pre_processing.py     # Script for data preprocessing
|   |-- model_making.py       # Script for training and saving the model
|-- app.py                    # Streamlit application for prediction
|-- README.md                 # Project documentation
```

## Prerequisites

Make sure you have the following installed:

- Python 3.8 or later
- Required Python libraries:
  ```bash
  pip install -r requirements.txt
  ```

The `requirements.txt` file should include:

```
streamlit
pandas
numpy
scikit-learn
pickle5
```

## How to Use

### Step 1: Data Preprocessing

Run the `pre_processing.py` script to preprocess the IPL dataset and generate the `pre_processed.csv` file in the `output/` directory:

```bash
python pre_processing.py
```

Make sure the raw datasets (`matches.xls` and `deliveries.xls`) are placed in the `data/` directory.

### Step 2: Model Training

Run the `model_making.py` script to train the Logistic Regression model and save the trained model (`model.pkl`) and transformer (`transformer.pkl`) in the `output/` directory:

```bash
python model_making.py
```

### Step 3: Running the Web Application

Launch the Streamlit application to use the win probability predictor:

```bash
streamlit run app.py
```

Access the app in your web browser at `http://localhost:8501`.

## Detailed Workflow

### 1. **Preprocessing**

The `pre_processing.py` script:

- Loads and cleans the raw `matches` and `deliveries` datasets.
- Filters relevant data for analysis.
- Computes match-specific statistics like balls left, wickets left, and required run rate.
- Outputs the processed data as `pre_processed.csv`.

### 2. **Model Training**

The `model_making.py` script:

- Loads the preprocessed data.
- Splits the data into training (up to 2020) and testing (post-2020) sets.
- Transforms categorical features using `OneHotEncoder`.
- Trains a Logistic Regression model with hyperparameter tuning using GridSearchCV.
- Saves the trained model and transformer as `model.pkl` and `transformer.pkl`.

### 3. **Web Application**

The `app.py` script:

- Provides an interactive interface for users to input match details.
- Predicts the probability of the batting team winning the match.
- Displays the probability in percentage format.

## Input Fields for Prediction

The following inputs are required in the app:

- **Batting Team**: Select the batting team from the dropdown.
- **Bowling Team**: Select the bowling team from the dropdown.
- **Toss Winner**: Select the team that won the toss.
- **Toss Decision**: Select whether the toss winner chose to bat or field.
- **Balls Left**: Enter the number of balls left in the second innings.
- **Wickets Left**: Enter the number of wickets remaining for the batting team.
- **First Inning Runs**: Enter the total runs scored in the first innings.
- **Current Runs**: Enter the current score of the batting team.

## Outputs

- **Win Probability**: The app predicts the probability of the batting team winning the match based on the input data.

