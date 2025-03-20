import pandas as pd


def main():
    # get TEAM1 and TEAM2 values from 2025_matchups.csv
    matchups_2025 = pd.read_csv("2025_matchups.csv")

    # Remove rows if one of the team column values has already appeared in a row before it
    # REMOVE THIS AFTER FIRST FOUR IS OVER
    # matchups_2025 = matchups_2025.drop_duplicates(subset=['TEAM1'], keep='first')
    # matchups_2025 = matchups_2025.drop_duplicates(subset=['TEAM2'], keep='first')

    team_names_kaggle_2025 = list(
        set(list(matchups_2025["TEAM1"].values) + list(matchups_2025["TEAM2"].values))
    )

    # Get team values from 2025 stats
    stats_2025 = pd.read_csv("team_stats_2025.csv")
    team_names_stats_2025 = list(stats_2025["Team"].values)

    # Find the teams in team_names_kaggle_2025 that are not in team_names_stats_2025
    non_matching_teams_2025 = set(team_names_kaggle_2025) - set(team_names_stats_2025)
    print(non_matching_teams_2025)

    # non_matching_teams = set(team_names_stats) - set(team_names_kaggle)
    # print(non_matching_teams)
    # print(len(non_matching_teams))

    # for year in range(2006, 2025):
    #     team_names_kaggle_year = [team for team in team_names_kaggle if str(year) in team]
    #     team_names_stats_year = [team for team in team_names_stats if str(year) in team]
    #     # print the number of team names in team_names_kaggle_year that are in team_names_stats_year
    #     print(year, len(set(team_names_kaggle_year) & set(team_names_stats_year)))

    # # There are some team names in team_name_stats that are very close to matching the team names in team_names_kaggle but do not match exactly, find them
    # for team in team_names_stats:
    #     if team not in team_names_kaggle:
    #         for kaggle_team in team_names_kaggle:
    #             if (team in kaggle_team or kaggle_team in team) and "ST" not in team and "ST" not in kaggle_team:
    #                 print(team, kaggle_team)


if __name__ == "__main__":
    main()
