import pandas as pd
import xgboost as xgb
from sklearn.model_selection import train_test_split
import random

def main():
    df = pd.read_csv("data/matchups_with_stats.csv")

    # Drop the DIFF column
    df = df.drop(columns=["DIFF"])

    # Split the dataframe into a features dataframe and a target dataframe
    X = df.drop(columns=["TEAM1_WIN"])
    y = df["TEAM1_WIN"]

    # Split the features and target dataframes into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Drop the TEAM columns from the training and testing sets
    X_train = X_train.drop(columns=["TEAM1", "TEAM2"])

    # Grab the TEAM columns from the testing set
    teams = X_test[["TEAM1", "TEAM2", "TEAM1_SEED", "TEAM2_SEED"]]
    X_test = X_test.drop(columns=["TEAM1", "TEAM2"])


    # Create an XGBoost random forest classifier
    model = xgb.XGBRFClassifier(n_estimators=100, random_state=random.randint(0, 10000), subsample=0.9)

    # Fit the model to the training data
    model.fit(X_train, y_train)

    # Print the accuracy of the model on the test data
    print(f"Accuracy: {model.score(X_test, y_test)}")

    # Predict the results of the test data
    predictions = model.predict(X_test)

    # Create a new dataframe with the team names, the team seeds, the predictions, and the correct outcome
    results = pd.DataFrame({"TEAM1": teams["TEAM1"], "TEAM2": teams["TEAM2"], "TEAM1_Seed": teams["TEAM1_SEED"], "TEAM2_Seed": teams["TEAM2_SEED"], "TEAM1_WIN": predictions, "ACTUAL_WIN": y_test})

    print(results)

if __name__ == "__main__":
    main()