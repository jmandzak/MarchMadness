import pandas as pd
import xgboost as xgb
from sklearn.model_selection import train_test_split
import random

def train_with_seed_and_save(X_train, X_test, y_train, y_test):
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

    # Save the model to a file
    model.save_model("models/xgb_rf_classifier.model")

def train_without_seed_and_save(X_train, X_test, y_train, y_test):
    # Drop the seed columns
    X_train = X_train.drop(columns=["TEAM1_SEED", "TEAM2_SEED"])
    X_test = X_test.drop(columns=["TEAM1_SEED", "TEAM2_SEED"])

    # Grab the TEAM columns from the testing set
    teams = X_test[["TEAM1", "TEAM2"]]
    X_test = X_test.drop(columns=["TEAM1", "TEAM2"])


    # Create an XGBoost random forest classifier
    model = xgb.XGBRFClassifier(n_estimators=100, random_state=random.randint(0, 10000), subsample=0.9)

    # Fit the model to the training data
    model.fit(X_train, y_train)

    # Print the accuracy of the model on the test data
    print(f"Accuracy: {model.score(X_test, y_test)}")

    # Predict the results of the test data
    predictions = model.predict(X_test)

    # Create a new dataframe with the team names, the predictions, and the correct outcome
    results = pd.DataFrame({"TEAM1": teams["TEAM1"], "TEAM2": teams["TEAM2"],"TEAM1_WIN": predictions, "ACTUAL_WIN": y_test})

    print(results)

    # Save the model to a file
    model.save_model("models/xgb_rf_classifier_without_seed.model")

def fix_dataframe(df):
    team1_win_count = 0
    team1_loss_count = 0
    # iterate through each row of the dataframe
    for index, row in df.iterrows():
        if team1_win_count > team1_loss_count and row["TEAM1_WIN"] == 1:
            # flip the values of all columns with TEAM1 and TEAM2 prefixes except for TEAM1_WIN
            for column in df.columns:
                if "TEAM1" in column and column != "TEAM1_WIN":
                    temp = row[column]
                    df.at[index, column] = row[column.replace("TEAM1", "TEAM2")]
                    df.at[index, column.replace("TEAM1", "TEAM2")] = temp
            # flip the value of TEAM1_WIN
            df.at[index, "TEAM1_WIN"] = 0
        
        team1_win_count += df.at[index, "TEAM1_WIN"]
        team1_loss_count += 1 - df.at[index, "TEAM1_WIN"]

    return df
            

def main():
    df = pd.read_csv("data/matchups_with_stats.csv")

    fix_dataframe(df)

    # Drop the DIFF column
    df = df.drop(columns=["DIFF"])

    df = fix_dataframe(df)

    # Split the dataframe into a features dataframe and a target dataframe
    X = df.drop(columns=["TEAM1_WIN"])
    y = df["TEAM1_WIN"]

    # Split the features and target dataframes into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Drop the TEAM columns from the training and testing sets
    X_train = X_train.drop(columns=["TEAM1", "TEAM2"])

    train_with_seed_and_save(X_train, X_test, y_train, y_test)
    train_without_seed_and_save(X_train, X_test, y_train, y_test)



if __name__ == "__main__":
    main()