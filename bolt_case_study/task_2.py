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
),
AggregatedData AS (
    SELECT
        d.City,
        d.Hour,
        AVG(`Potential Orders`) AS AvgPotentialDemand,
        AVG(s.`Deliveries per Hour` * s.`Online Hours`) AS AvgSupply
    FROM
        PotentialDemand d
    LEFT JOIN
        df2 s
    ON
        d.City = s.City AND d.Date = s.Date AND d.Hour = s.Hour
    GROUP BY
        d.City, d.Hour
)
SELECT
    City,
    Hour,
    AvgPotentialDemand,
    AvgSupply,
    CASE 
        WHEN AvgPotentialDemand > AvgSupply THEN 'Undersupplied'
        ELSE 'Adequately Supplied'
    END AS SupplyStatus
FROM
    AggregatedData
ORDER BY
    City, Hour;
"""

# Execute the SQL query
result = psql.sqldf(query, locals())

# Display the result
print("Query result:")
print(result)

output_file = '/Users/abhisheksingh/Downloads/bolt_task_2_1.xlsx'
result.to_excel(output_file, index=False)

print(f"Result saved to {output_file}")

