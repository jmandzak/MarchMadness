import pandas as pd
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix
import random

def main():
    df = pd.read_csv("data/matchups_with_stats.csv")

    # Add a column called UPSET that is 1 if the TEAM1_WIN column is 0 and the TEAM1_SEED is less than the TEAM2_SEED or if the TEAM1_WIN column is 1 and the TEAM1_SEED is greater than the TEAM2_SEED
    df["UPSET"] = [1 if (df["TEAM1_WIN"].iloc[i] == 0 and df["TEAM1_SEED"].iloc[i] < df["TEAM2_SEED"].iloc[i]) or (df["TEAM1_WIN"].iloc[i] == 1 and df["TEAM1_SEED"].iloc[i] > df["TEAM2_SEED"].iloc[i]) else 0 for i in range(len(df))]

    # Drop the DIFF and TEAM1_WIN columns
    df = df.drop(columns=["DIFF", "TEAM1_WIN"])

    # Split the dataframe into a features dataframe and a target dataframe
    X = df.drop(columns=["UPSET"])
    y = df["UPSET"]

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
    results = pd.DataFrame({"TEAM1": teams["TEAM1"], "TEAM2": teams["TEAM2"], "TEAM1_Seed": teams["TEAM1_SEED"], "TEAM2_Seed": teams["TEAM2_SEED"], "PRED_UPSET": predictions, "ACTUAL_UPSET": y_test})

    # change the pandas options to print the entire dataframe
    pd.set_option("display.max_rows", None)

    # Remove index from results
    results.reset_index(drop=True, inplace=True)
    print(results)

    # Create a confusion matrix with the predictions
    cm = confusion_matrix(y_test, predictions)
    print(cm)

if __name__ == "__main__":
    main()