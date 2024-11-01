import pandas as pd
import pandasql as psql

# Path to the Excel file
excel_file = '/Users/abhisheksingh/Downloads/Marketplace Ops - Home Task.xlsx'

# Read data from the 'SalesData' sheet
sheet_name = 'Demand'
df = pd.read_excel(excel_file, sheet_name=sheet_name)

sheet_name_2 = 'Supply'
df2 = pd.read_excel(excel_file, sheet_name=sheet_name_2)

# Display the DataFrame
print("DataFrame content:")
print(df)

# Define an SQL query to select rows where 'Sales' is greater than 1000
query = """
WITH PotentialDemand AS (
    SELECT 
        City,
        Date,
        Hour,
        `Completed Orders`,
        `Shrinkage %`,
        `Completed Orders` * (1 + `Shrinkage %` * 0.25 / 100) AS `Potential Orders`
    FROM 
        df
)
, WeeklyAggregated AS (
    SELECT
        City,
        strftime('%W', Date) AS Week,
        SUM(`Completed Orders`) AS `Completed Orders`,
        AVG(`Shrinkage %`) AS `Average Shrinkage %`,
        SUM(`Potential Orders`) AS `Potential Orders`
    FROM
        PotentialDemand
    GROUP BY
        City, Week
)
, HighestShrinkageWeek AS (
    SELECT
        City,
        Week,
        `Completed Orders`,
        `Average Shrinkage %`,
        `Potential Orders`
    FROM (
        SELECT
            City,
            Week,
            `Completed Orders`,
            `Average Shrinkage %`,
            `Potential Orders`,
            ROW_NUMBER() OVER (PARTITION BY City ORDER BY `Average Shrinkage %` DESC) AS rn
        FROM
            WeeklyAggregated
    )
    WHERE rn = 1
)
, Calculations AS (
    SELECT
        City,
        Week,
        `Completed Orders`,
        `Average Shrinkage %`,
        `Potential Orders`,
        `Average Shrinkage %` * 0.25 AS `Additional Courier Hours`,
        (`Average Shrinkage %` * 0.25) * 8 AS `Cost`,
        (16 * 0.25 + 1) AS `Revenue per Order`,
        `Potential Orders` * (16 * 0.25 + 1) AS `Additional Revenue`
    FROM
        HighestShrinkageWeek
)
SELECT
    City,
    Week,
    `Completed Orders`,
    `Average Shrinkage %`,
    `Potential Orders`,
    `Additional Courier Hours`,
    `Cost`,
    `Revenue per Order`,
    `Additional Revenue`
FROM
    Calculations
ORDER BY
    City, Week;
"""

# Execute the SQL query
result = psql.sqldf(query, locals())

# Display the result
print("Query result:")
print(result)

output_file = '/Users/abhisheksingh/Downloads/bolt_task_3_2_2.xlsx'
result.to_excel(output_file, index=False)

print(f"Result saved to {output_file}")

