import typing

import pandas as pd

YEAR = 2025


def get_all_winning_teams(
    round_: str,
) -> typing.Tuple[typing.List[str], typing.List[str], typing.List[str]]:
    predictions_with_seeds = pd.read_csv(
        f"data/predictions_2025/with_seeds/{round_}_round_predictions.csv"
    )
    predictions_without_seeds = pd.read_csv(
        f"data/predictions_2025/without_seeds/{round_}_round_predictions.csv"
    )
    combined_predictions = pd.read_csv(
        f"data/predictions_2025/combined/{round_}_round_predictions.csv"
    )

    return (
        predictions_with_seeds["WINNING_TEAM"].tolist(),
        predictions_without_seeds["WINNING_TEAM"].tolist(),
        combined_predictions["WINNING_TEAM"].tolist(),
    )


def get_next_round_string(round: str) -> str:
    if round == "first":
        return "second"
    elif round == "second":
        return "third"
    elif round == "third":
        return "fourth"
    elif round == "fourth":
        return "fifth"
    elif round == "fifth":
        return "sixth"
    else:
        raise ValueError(f"Invalid round: {round}")


def advance_round(round_: str) -> None:
    (
        winning_with_seeds,
        winning_without_seeds,
        combined_winning_teams,
    ) = get_all_winning_teams(round_)

    # Create a DataFrame with the winning teams
    # Every two teams in the list are a matchup
    with_seeds = pd.DataFrame(
        {
            "TEAM1": winning_with_seeds[0::2],
            "TEAM2": winning_with_seeds[1::2],
        }
    )
    without_seeds = pd.DataFrame(
        {
            "TEAM1": winning_without_seeds[0::2],
            "TEAM2": winning_without_seeds[1::2],
        }
    )
    combined_seeds = pd.DataFrame(
        {
            "TEAM1": combined_winning_teams[0::2],
            "TEAM2": combined_winning_teams[1::2],
        }
    )

    # write the dataframes to csv files
    with_seeds.to_csv(
        f"data/predictions_2025/with_seeds/{get_next_round_string(round_)}_round_matchups.csv",
        index=False,
    )
    without_seeds.to_csv(
        f"data/predictions_2025/without_seeds/{get_next_round_string(round_)}_round_matchups.csv",
        index=False,
    )
    combined_seeds.to_csv(
        f"data/predictions_2025/combined/{get_next_round_string(round_)}_round_matchups.csv",
        index=False,
    )
