# Supress all tf warnings and info logs
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

import pandas as pd
from keras.models import Sequential
from keras.layers import Dense
from keras.optimizers import Adam
from keras.callbacks import EarlyStopping
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix

def create_model(X_train) -> Sequential:
    # Create a neural network model
    model = Sequential()
    model.add(Dense(64, input_dim=X_train.shape[1], activation="relu"))
    model.add(Dense(32, activation="relu"))
    model.add(Dense(16, activation="relu"))
    model.add(Dense(1, activation="sigmoid"))

    # Compile the model
    model.compile(loss="binary_crossentropy", optimizer=Adam(learning_rate=0.001), metrics=["accuracy"])

    return model

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

    print(X_train.shape)

    # Create a neural network model
    model = create_model(X_train)

    # Fit the model to the training data
    model.fit(X_train, y_train, epochs=1000, batch_size=32, validation_split=0.2, callbacks=[EarlyStopping(patience=10)])

    # Print the accuracy of the model on the test data
    print(f"Accuracy: {model.evaluate(X_test, y_test)[1]}")

    # Predict the results of the test data
    predictions = model.predict(X_test)
    predictions = [1 if pred > 0.5 else 0 for pred in predictions]

    # Create a new dataframe with the team names, the team seeds, the predictions, and the correct outcome
    results = pd.DataFrame({"TEAM1": teams["TEAM1"], "TEAM2": teams["TEAM2"], "TEAM1_Seed": teams["TEAM1_SEED"], "TEAM2_Seed": teams["TEAM2_SEED"], "PRED_TEAM1_WIN": predictions, "ACTUAL_TEAM1_WIN": y_test})

    cm = confusion_matrix(y_test, predictions)
    print(cm)



if __name__ == "__main__":
    main()