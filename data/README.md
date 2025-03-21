# Data For Modeling

## tournament_matchups.csv
Found on Kaggle at https://www.kaggle.com/datasets/nishaanamin/march-madness-data?resource=download&select=Tournament+Matchups.csv
File is structured where every two rows is a matchup

## all_matchup_results.csv
Constructed from tournament_matchups.csv, has every matchup and the winning team

## all_matchup_differentials.csv
Constructed from tournament_matchups.csv, has every matchup and the differential between TEAM1 and TEAM2

## team_seeds_by_year.csv
Constructed from tournament_matchups.csv, has every cleaned team name combined with the year and the seed they were that year

## team_stats_{year}_.csv
Constructed from the scrape_team_stats.py script, has all team stats for teams from 2006-2024

## matchups_with_stats.csv
Constructed from multiple CSVs, this csv has all matchups where stats exist for both teams

## HOW TO UPDATE
Update year loop in `scrape_team_stats.py` to get new year, run
Update year in `extract_from_tournament_results.py`, run
Run `fix_name_discrepancies.py`, update name conversion chart in `scrape_team_stats.py` to make them match
Update year loop in `create_matchups_with_stats.py`, run
Run `advance_round.py` after updating round and year to advance each round as you predict