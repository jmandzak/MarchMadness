import pandas as pd


def main():
    # get names and seeds
    seed_df = pd.read_csv("team_seeds_by_year.csv")

    # get all matchups
    matchups = pd.read_csv("all_matchup_results.csv")
    # reset the WINNING_TEAM column to be either a 1 if TEAM1 won or a 0 if TEAM2 won
    matchups["WINNING_TEAM"] = matchups.apply(
        lambda row: 1 if row["WINNING_TEAM"] == row["TEAM1"] else 0, axis=1
    )
    # rename the WINNING_TEAM column to be TEAM1_WIN
    matchups = matchups.rename(columns={"WINNING_TEAM": "TEAM1_WIN"})

    matchups_with_differentials = pd.read_csv("all_matchup_differentials.csv")
    # Add the DIFF column from the matchups_with_differentials dataframe to the matchups dataframe where the team1 and team2 columns match
    matchups = matchups.merge(
        matchups_with_differentials[["TEAM1", "TEAM2", "DIFF"]],
        how="left",
        left_on=["TEAM1", "TEAM2"],
        right_on=["TEAM1", "TEAM2"],
    )

    # Grab all team_stats{year}.csv files and concatenate them into one dataframe
    team_stats = pd.concat(
        [pd.read_csv(f"team_stats_{year}.csv") for year in range(2006, 2026)]
    )
    all_team_names_with_stats = team_stats["Team"].unique()

    """This step should be removed when I figure out how to handle the non-matching names from the stats and the matchups dataframes."""
    # Remove rows from the matchups dataframe where the team1 or team2 columns are not in the all_team_names list
    matchups = matchups[
        matchups["TEAM1"].isin(all_team_names_with_stats)
        & matchups["TEAM2"].isin(all_team_names_with_stats)
    ]

    # Merge the matchups dataframe with the team_stats dataframe on the TEAM1 column and prepend all the column headers from the team_stats dataframe with "TEAM1_"
    matchups = matchups.merge(
        team_stats.add_prefix("TEAM1_"),
        how="left",
        left_on="TEAM1",
        right_on="TEAM1_Team",
    )
    # Drop the TEAM1_Team column
    matchups = matchups.drop(columns="TEAM1_Team")

    # Merge the matchups dataframe with the team_stats dataframe on the TEAM2 column and prepend all the column headers from the team_stats dataframe with "TEAM2_"
    matchups = matchups.merge(
        team_stats.add_prefix("TEAM2_"),
        how="left",
        left_on="TEAM2",
        right_on="TEAM2_Team",
    )
    # Drop the TEAM2_Team column
    matchups = matchups.drop(columns="TEAM2_Team")

    # Add two new seed columns TEAM1_SEED and TEAM2_SEED to the matchups dataframe by using the seed_df dataframe to match the team names
    matchups = matchups.merge(
        seed_df.add_prefix("TEAM1_"), how="left", left_on="TEAM1", right_on="TEAM1_TEAM"
    )
    matchups = matchups.merge(
        seed_df.add_prefix("TEAM2_"), how="left", left_on="TEAM2", right_on="TEAM2_TEAM"
    )

    matchups = matchups.drop(columns="TEAM1_TEAM")
    matchups = matchups.drop(columns="TEAM2_TEAM")

    # Move the TEAM1_WIN column and the DIFF column to the end of the dataframe
    matchups = matchups[
        [col for col in matchups if col not in ["TEAM1_WIN", "DIFF"]]
        + ["TEAM1_WIN", "DIFF"]
    ]

    # Write the final dataframe to a csv file
    matchups.to_csv("matchups_with_stats.csv", index=False)

    print(matchups.head())


if __name__ == "__main__":
    main()
