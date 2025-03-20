import csv

import pandas as pd
import requests
from bs4 import BeautifulSoup

name_conversion_chart = {
    "BRIGHAMYOUNG": "BYU",
    "UCONN": "CONNECTICUT",
    "CHARLESTON": "COLLEGEOFCHARLESTON",
    "NCST": "NORTHCAROLINAST",
    "AMERICANUNIVERSITY": "AMERICAN",
    "STFRANCISPA": "SAINTFRANCIS",
    "OLEMISS": "MISSISSIPPI",
    "NEBRASKA": "NEBRASKAOMAHA",
}


def clean_name_column(df: pd.DataFrame, year: int) -> pd.DataFrame:
    # Remove all special characters and spaces from the team name and make it uppercase and prepend the year
    df["Team"] = str(year) + df["Team"].str.replace(r"\W+", "").str.upper()

    # Replace STATE with ST
    df["Team"] = df["Team"].str.replace("STATE", "ST")

    # If any of the keys in the name_conversion_chart are in the team name, replace it with the value
    for key, value in name_conversion_chart.items():
        df["Team"] = df["Team"].str.replace(key, value)
    return df


def main():
    # There is a website that follows the url pattern of https://basketball.realgm.com/ncaa/team-stats/{year}/Averages/{team_type}/0 where the year changes
    # There is a table on each page with the class name "tablesaw"
    # The two team types are Team_Totals and Opponent_Totals
    # Create a csv for each year from 2006-2024 that combines the data from both team types where the key is the Team name and the value is the data from the table
    # Get the column names from the first row of the table and use those as the header for the csv
    # The csv should be named team_stats_{year}.csv
    team_types = ["Team_Totals", "Opponent_Totals"]
    for year in range(2025, 2026):
        dataframes = []
        for team_type in team_types:
            url = f"https://basketball.realgm.com/ncaa/team-stats/{year}/Averages/{team_type}/0"
            response = requests.get(url)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, "html.parser")
                table = soup.find("table", class_="tablesaw")
                if table:
                    header = [
                        cell.get_text(strip=True)
                        for cell in table.find("tr").find_all("th")
                    ]
                    data = []
                    for row in table.find_all("tr")[1:]:
                        row_data = [
                            cell.get_text(strip=True) for cell in row.find_all("td")
                        ]
                        data.append(row_data)
                    df = pd.DataFrame(data, columns=header)
                    dataframes.append(df)
                else:
                    print(f"No table found for year {year} and team type {team_type}")
            else:
                print(
                    f"Failed to retrieve data for year {year} and team type {team_type}"
                )

        if dataframes:
            combined_df = pd.merge(
                dataframes[0], dataframes[1], on="Team", suffixes=("", "_Opp")
            )
            clean_name_column(combined_df, year)
            combined_df = combined_df.loc[:, ~combined_df.columns.str.startswith("#")]

            csv_file = f"team_stats_{year}.csv"
            combined_df.to_csv(csv_file, index=False)
            print(f"CSV file created for year {year}")

    # Create a csv from the table on that page with the class name "tablesaw tablesaw-swipe" for every year from 2006 to 2024

    # for year in range(2006, 2025):
    #     url = f"https://basketball.realgm.com/ncaa/team-stats/{year}/Averages/Team_Totals/0"
    #     response = requests.get(url)
    #     if response.status_code == 200:
    #         soup = BeautifulSoup(response.content, 'html.parser')
    #         table = soup.find('table', class_='tablesaw')
    #         if table:
    #             csv_file = f"team_stats_{year}.csv"
    #             with open(csv_file, 'w', newline='') as file:
    #                 writer = csv.writer(file)
    #                 for row in table.find_all('tr'):
    #                     data = [cell.get_text(strip=True) for cell in row.find_all('td')]
    #                     writer.writerow(data)
    #             print(f"CSV file created for year {year}")
    #         else:
    #             print(f"No table found for year {year}")
    #     else:
    #         print(f"Failed to retrieve data for year {year}")


if __name__ == "__main__":
    main()
