# Supress all tf warnings and info logs
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

import pandas as pd
from keras.models import Sequential
from keras.layers import Dense
from keras.optimizers import Adam
from keras.callbacks import EarlyStopping
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, mean_absolute_error
import random

def create_model(X_train) -> Sequential:
    # Create a neural network model
    model = Sequential()
    model.add(Dense(64, input_dim=X_train.shape[1], activation="relu"))
    model.add(Dense(32, activation="relu"))
    model.add(Dense(16, activation="relu"))
    model.add(Dense(1, activation="linear"))

    # Compile the model
    model.compile(loss="mean_absolute_error", optimizer=Adam(learning_rate=0.001), metrics=["mean_absolute_error"])

    return model

    # # Create a neural network model
    # model = Sequential()
    # model.add(Dense(64, input_dim=X_train.shape[1], activation="relu"))
    # model.add(Dense(32, activation="relu"))
    # model.add(Dense(16, activation="relu"))
    # model.add(Dense(1, activation="sigmoid"))

    # # Compile the model
    # model.compile(loss="binary_crossentropy", optimizer=Adam(learning_rate=0.001), metrics=["accuracy"])

    # return model

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


    # Create a neural network model
    model = create_model(X_train)

    # Fit the model to the training data
    model.fit(X_train, y_train, epochs=1000, batch_size=32, validation_split=0.2, callbacks=[EarlyStopping(patience=25)])

    # Print the accuracy of the model on the test data
    print(f"Mean Absolute Error: {model.evaluate(X_test, y_test)[1]}")

    # Predict the test set
    predictions = model.predict(X_test)
    
    # Remove the extra dimension from the predictions
    predictions = predictions.flatten()

    # Use the correct values to compute mean absolute error
    mae = mean_absolute_error(y_test, predictions)
    print(f"Mean Absolute Error: {mae}")

    # Create a new dataframe with the team names, the team seeds, the predictions, and the correct outcome
    results = pd.DataFrame({"TEAM1": teams["TEAM1"], "TEAM2": teams["TEAM2"], "TEAM1_Seed": teams["TEAM1_SEED"], "TEAM2_Seed": teams["TEAM2_SEED"], "PREDICTED_DIFF": predictions, "ACTUAL_DIFF": y_test})

    print(results)

    # Create a list of 1s and 0s for each time the sign of the predicted difference matches the sign of the actual difference
    correct_sign = [1 if (results["PREDICTED_DIFF"].iloc[i] > 0 and results["ACTUAL_DIFF"].iloc[i] > 0) or (results["PREDICTED_DIFF"].iloc[i] < 0 and results["ACTUAL_DIFF"].iloc[i] < 0) else 0 for i in range(len(results))]
    actual_sign = [1 if results["ACTUAL_DIFF"].iloc[i] > 0 else 0 for i in range(len(results))]
    
    # Print a confusion matrix with the signs
    cm = confusion_matrix(actual_sign, correct_sign)
    print(cm)

if __name__ == "__main__":
    main()