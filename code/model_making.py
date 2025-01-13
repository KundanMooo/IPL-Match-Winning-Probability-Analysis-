import pickle
from pre_processing import preprocess_ipl_data
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GridSearchCV, TimeSeriesSplit

# Step 1: Preprocess data
preprocess_ipl_data("./data/matches.xls", "./data/deliveries.xls", "./output/pre_processed.csv")

#preprocess_ipl_data()

# Step 2: Load preprocessed data
ipl = pd.read_csv("./output/pre_processed.csv")
ipl['date'] = pd.to_datetime(ipl['date'])

# Step 3: Split dataset into training and testing
# Train: Data up to 2020, Test: Data from 2020 onwards
df_train = ipl[ipl['date'].dt.year <= 2020].drop(columns=['date'])
df_test = ipl[ipl['date'].dt.year > 2020].drop(columns=['date'])

X_train = df_train.iloc[:, :-1]
X_test = df_test.iloc[:, :-1]

y_train = df_train['winner']
y_test = df_test['winner']

# Step 4: Transform categorical features
trf = ColumnTransformer([
    ('one_hot', OneHotEncoder(drop='first',handle_unknown='ignore'), ['batting_team', 'bowling_team', 'toss_winner', 'toss_decision'])
], remainder='passthrough')

X_train = trf.fit_transform(X_train)
X_test = trf.transform(X_test)

# Step 5: Train Logistic Regression model with hyperparameter tuning
lr = LogisticRegression()
param_grid_lr = {
    'C': [0.01, 0.1, 1, 10],
    'solver': ['lbfgs', 'liblinear'],
    'max_iter': [100, 200, 300, 400, 500]
}

tscv = TimeSeriesSplit(n_splits=5)

# Perform grid search
grid_search_lr = GridSearchCV(estimator=lr, param_grid=param_grid_lr, scoring='accuracy', cv=tscv, n_jobs=-1)
grid_search_lr.fit(X_train, y_train)

# Step 6: Save the best model
best_lr_model = grid_search_lr.best_estimator_
pickle.dump(best_lr_model, open('./output/model.pkl', 'wb'))

print("#####$$$$-----------Model training completed and saved as model.pkl.")

pickle.dump(trf,open('./output/transformer.pkl','wb'))

print("Model training completed and saved as transformer.pkl.")