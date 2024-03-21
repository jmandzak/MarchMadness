import xgboost as xgb
import pandas as pd

# ROUND = "first"
# ROUND = "second"
# ROUND = "third"
# ROUND = "fourth"
# ROUND = "fifth"
# ROUND = "sixth"

def predict_and_save(matchups, teams, use_model_with_seeds=True):
    # Load the model
    model = xgb.XGBRFClassifier()
    if use_model_with_seeds:
        model.load_model("models/xgb_rf_classifier.model")
    else:
        model.load_model("models/xgb_rf_classifier_without_seed.model")
        # drop the seed columns
        matchups = matchups.drop(columns=["TEAM1_SEED", "TEAM2_SEED"])

    # Predict the results of the matchups
    predictions = model.predict(matchups)
    
    # Create a list matching the predictions to the teams and seeds
    results = pd.DataFrame({"TEAM1": teams["TEAM1"], "TEAM2": teams["TEAM2"], "TEAM1_Seed": teams["TEAM1_SEED"], "TEAM2_Seed": teams["TEAM2_SEED"], "TEAM1_WIN": predictions})

    # Add a column called UPSET that is 1 if team1_win is 1 and team1 is the higher seed or if team_1_win is 0 and team2 is the higher seed, otherwise 0
    results["UPSET"] = results.apply(lambda row: 1 if (row["TEAM1_WIN"] == 1 and row["TEAM1_Seed"] > row["TEAM2_Seed"]) or (row["TEAM1_WIN"] == 0 and row["TEAM1_Seed"] < row["TEAM2_Seed"]) else 0, axis=1)
    

    # If team1_win is 1, replace the value with the name of the team in the TEAM1 column, otherwise replace the value with the name of the team in the TEAM2 column
    results["TEAM1_WIN"] = results.apply(lambda row: row["TEAM1"] if row["TEAM1_WIN"] == 1 else row["TEAM2"], axis=1)

    # Rename the TEAM1_WIN column to be WINNING_TEAM
    results = results.rename(columns={"TEAM1_WIN": "WINNING_TEAM"})

    # Write the results to a csv file
    if use_model_with_seeds:
        results.to_csv(f"data/predictions_2024/{ROUND}_round_predictions_with_seeds.csv", index=False)
    else:
        results.to_csv(f"data/predictions_2024/{ROUND}_round_predictions_without_seeds.csv", index=False)

def main():
    matchups = pd.read_csv(f"data/predictions_2024/{ROUND}_round_matchups.csv")
    stats = pd.read_csv("data/team_stats_2024.csv")
    seeds = pd.read_csv("data/team_seeds_by_year.csv")

    # Merge the matchups dataframe with the stats dataframe twice on the TEAM1 and TEAM2 columns
    matchups = matchups.merge(stats.add_prefix("TEAM1_"), how="left", left_on="TEAM1", right_on="TEAM1_Team")
    matchups = matchups.merge(stats.add_prefix("TEAM2_"), how="left", left_on="TEAM2", right_on="TEAM2_Team")

    # Drop the TEAM1_Team and TEAM2_Team columns
    matchups = matchups.drop(columns=["TEAM1_Team", "TEAM2_Team"])

    # Merge the matchups dataframe with the seeds dataframe twice on the TEAM1 and TEAM2 columns
    matchups = matchups.merge(seeds.add_prefix("TEAM1_"), how="left", left_on="TEAM1", right_on="TEAM1_TEAM")
    matchups = matchups.merge(seeds.add_prefix("TEAM2_"), how="left", left_on="TEAM2", right_on="TEAM2_TEAM")

    # Drop the TEAM1_TEAM and TEAM2_TEAM columns
    matchups = matchups.drop(columns=["TEAM1_TEAM", "TEAM2_TEAM"])

    # Drop the TEAM1 and TEAM2 columns but save the teams and seeds to a new dataframe
    teams = matchups[["TEAM1", "TEAM2", "TEAM1_SEED", "TEAM2_SEED"]]
    matchups = matchups.drop(columns=["TEAM1", "TEAM2"])

    # predict_and_save(matchups, teams, True)
    predict_and_save(matchups, teams, False)

    

if __name__ == "__main__": 
    main()