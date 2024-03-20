import pandas as pd
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error
import random

def main():
    df = pd.read_csv("data/matchups_with_stats.csv")

    # Drop the TEAM1_WIN column
    df = df.drop(columns=["TEAM1_WIN"])

    # Split the dataframe into a features dataframe and a target dataframe
    X = df.drop(columns=["DIFF"])
    y = df["DIFF"]

    # Split the features and target dataframes into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Drop the TEAM columns from the training and testing sets
    X_train = X_train.drop(columns=["TEAM1", "TEAM2"])

    # Grab the TEAM columns from the testing set
    teams = X_test[["TEAM1", "TEAM2", "TEAM1_SEED", "TEAM2_SEED"]]
    X_test = X_test.drop(columns=["TEAM1", "TEAM2"])


    # Create an XGBoost random forest classifier
    model = xgb.XGBRFRegressor(n_estimators=100, max_depth=10, random_state=random.randint(0, 10000), subsample=0.9)

    # Fit the model to the training data
    model.fit(X_train, y_train)

    # Predict the test set
    predictions = model.predict(X_test)
    # Use the correct values to compute mean absolute error
    mae = mean_absolute_error(y_test, predictions)
    print(f"Mean Absolute Error: {mae}")

    # Create a new dataframe with the team names, the team seeds, the predictions, and the correct outcome
    results = pd.DataFrame({"TEAM1": teams["TEAM1"], "TEAM2": teams["TEAM2"], "TEAM1_Seed": teams["TEAM1_SEED"], "TEAM2_Seed": teams["TEAM2_SEED"], "PREDICTED_DIFF": predictions, "ACTUAL_DIFF": y_test})

    print(results)

    # Create a list of 1s and 0s for each time the sign of the predicted difference matches the sign of the actual difference
    correct_sign = [1 if (results["PREDICTED_DIFF"].iloc[i] > 0 and results["ACTUAL_DIFF"].iloc[i] > 0) or (results["PREDICTED_DIFF"].iloc[i] < 0 and results["ACTUAL_DIFF"].iloc[i] < 0) else 0 for i in range(len(results))]
    # Print the number of correct signs out of all predictions
    print(f"Correct Sign: {sum(correct_sign) / len(correct_sign)}")

if __name__ == "__main__":
    main()