import pandas as pd
import numpy as np


def remove_2024_teams(df: pd.DataFrame) -> pd.DataFrame:
    # Drop all rows that have 2024 as the value of the YEAR column
    df = df[df['YEAR'] != 2024]
    return df

def clean_name_column(df: pd.DataFrame) -> pd.DataFrame:
    # Remove all special characters and spaces from the team name and make it uppercase and prepend the YEAR column value
    df['TEAM'] = df['YEAR'].astype(str) + df['TEAM'].str.replace(r'\W+', '').str.upper()
    return df

def write_team_seeds_by_year(df: pd.DataFrame) -> None:
    # Create a dictionary that contains the team name and the seed for each year
    team_seeds_by_year = dict(zip(df['TEAM'], df['SEED']))

    # Write the dictionary to a csv file using pandas with the header column names TEAM and SEED
    pd.DataFrame(list(team_seeds_by_year.items()), columns=['TEAM', 'SEED']).to_csv('team_seeds_by_year.csv', index=False)

def write_all_matchup_results(df: pd.DataFrame) -> None:
    # For every two rows in the dataframe, get the TEAM column value and the SCORE column value and figure out the winner
    new_df = pd.DataFrame()
    new_df['TEAM1'] = df['TEAM'].iloc[::2].reset_index(drop=True)
    new_df['TEAM2'] = df['TEAM'].iloc[1::2].reset_index(drop=True)
    new_df['WINNING_TEAM'] = np.where(df['SCORE'].iloc[::2].reset_index(drop=True) > df['SCORE'].iloc[1::2].reset_index(drop=True), new_df['TEAM1'], new_df['TEAM2'])
    new_df.to_csv('all_matchup_results.csv', index=False)


def write_all_matchup_differentials(df: pd.DataFrame) -> None:
    new_df = pd.DataFrame()
    new_df['TEAM1'] = df['TEAM'].iloc[::2].reset_index(drop=True)
    new_df['TEAM2'] = df['TEAM'].iloc[1::2].reset_index(drop=True)
    new_df['DIFF'] = df['SCORE'].iloc[::2].reset_index(drop=True) - df['SCORE'].iloc[1::2].reset_index(drop=True)
    new_df.to_csv('all_matchup_differentials.csv', index=False)


def write_2024_matchups(df: pd.DataFrame) -> None:
    # Get the rows that have 2024 as the value of the YEAR column and have 64 for the CURRENT ROUND column
    df = df[df['CURRENT ROUND'] == 64]
    df = df[df['YEAR'] == 2024]

    # For every two rows in the dataframe, get the TEAM column value and the SCORE column value and figure out the winner
    new_df = pd.DataFrame()
    new_df['TEAM1'] = df['TEAM'].iloc[::2].reset_index(drop=True)
    new_df['TEAM2'] = df['TEAM'].iloc[1::2].reset_index(drop=True)
    new_df.to_csv('2024_matchups.csv', index=False)


def main():
    df = pd.read_csv('tournament_matchups.csv')
    df = clean_name_column(df)

    write_2024_matchups(df)

    write_team_seeds_by_year(df)

    df = remove_2024_teams(df)
    write_all_matchup_results(df)
    write_all_matchup_differentials(df)

if __name__ == '__main__':
    main() 