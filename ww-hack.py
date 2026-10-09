from pathlib import Path
import pandas as pd

"""1. Converts Excel to Pd Dataframe
   2. header=3 uses the 4th row as the names for the columns.
   3. dtype=str just reads everything as a string.
   4. engine=xlrd is used to open .xls file."""
excel_file = Path(__file__).with_name("est24all.xls")
csv_file = Path(__file__).with_name("est24all.csv")

# Convert the downloaded Excel file to CSV
excel_df = pd.read_excel(excel_file, header=3, dtype=str, engine="xlrd")
excel_df.to_csv(csv_file, index=False)
excel_df.to_csv("csv_raw_file.csv", index=False)
# Read the CSV; use df for the rest of your code
df = pd.read_csv(csv_file, dtype=str)
df.columns = [
    "state_fips",
    "county_fips",
    "state_abbr",
    "county",
    "people_in_poverty",
    "poverty_count_ci90_low",
    "poverty_count_ci90_high",
    "poverty_rate_pct",
    "poverty_rate_ci90_low_pct",
    "poverty_rate_ci90_high_pct",
    "children_0_17_in_poverty",
    "children_0_17_count_ci90_low",
    "children_0_17_count_ci90_high",
    "children_0_17_poverty_rate_pct",
    "children_0_17_rate_ci90_low_pct",
    "children_0_17_rate_ci90_high_pct",
    "children_5_17_families_in_poverty",
    "children_5_17_count_ci90_low",
    "children_5_17_count_ci90_high",
    "children_5_17_poverty_rate_pct",
    "children_5_17_rate_ci90_low_pct",
    "children_5_17_rate_ci90_high_pct",
    "median_household_income_usd",
    "income_ci90_low_usd",
    "income_ci90_high_usd",
    "children_under_5_in_poverty",
    "children_under_5_count_ci90_low",
    "children_under_5_count_ci90_high",
    "children_under_5_poverty_rate_pct",
    "children_under_5_rate_ci90_low_pct",
    "children_under_5_rate_ci90_high_pct",
]

#For every state code, it removes blank spaces and puts zeros, e.g. 6 becomes 06.
state_fips = df["state_fips"].str.strip().str.zfill(2)
#Samew thing for counties, but instead of making it 2 char it makes it 3 char, e.g. 6 becomes 006.
county_fips = df["county_fips"].str.strip().str.zfill(3)
#Texas fips is 48 and "000" is the state summary, not the county. county_fips.ne("000") drops the county fips "000"
df_texas_counties = df.loc[state_fips.eq("48") & county_fips.ne("000")].copy()


text_columns = {"state_fips", "county_fips", "state_abbr", "county"}
for column in df_texas_counties.columns:
    if column not in text_columns:
        df_texas_counties[column] = pd.to_numeric(
            df_texas_counties[column].str.replace(",", "", regex=False),
            errors="coerce",
        )
# Save all Texas county estimates to a spreadsheet-friendly CSV.
#output_file = Path(__file__).with_name("texas_counties.csv")
#df_texas_counties.to_csv(output_file, index=False)
#print(f"\nSaved full table to: {output_file}")
df_texas_counties = df_texas_counties.drop(columns=[
    "state_fips",
    "county_fips",
    "state_abbr",
    "people_in_poverty",
    "poverty_count_ci90_low",
    "poverty_count_ci90_high",
    "poverty_rate_ci90_low_pct",
    "poverty_rate_ci90_high_pct",
    "children_0_17_count_ci90_low",
    "children_0_17_count_ci90_high",
    "children_0_17_rate_ci90_low_pct",
    "children_0_17_rate_ci90_high_pct",
    "children_5_17_count_ci90_low",
    "children_5_17_count_ci90_high",
    "children_5_17_rate_ci90_low_pct",
    "children_5_17_rate_ci90_high_pct",
    "income_ci90_low_usd",
    "income_ci90_high_usd",
    "children_under_5_count_ci90_low",
    "children_under_5_count_ci90_high",
    "children_under_5_rate_ci90_low_pct",
    "children_under_5_rate_ci90_high_pct",
    "children_under_5_in_poverty",
    "children_under_5_poverty_rate_pct",
    "children_5_17_families_in_poverty",
    "children_0_17_in_poverty"
])

print(f"Texas county rows: {len(df_texas_counties)}")
print(df_texas_counties.to_string(index=False))
df_texas_counties.to_csv("texas_counties.csv", index=False)
