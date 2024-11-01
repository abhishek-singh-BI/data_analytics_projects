import pandas as pd
import pandasql as psql

# Path to the Excel file
excel_file = '/Users/abhisheksingh/Downloads/Marketplace Ops - Home Task.xlsx'

# Read data from the 'SalesData' sheet
sheet_name = 'Demand'
df = pd.read_excel(excel_file, sheet_name=sheet_name)

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
        `Completed Orders` * (1 + `Shrinkage %` * 0.0025) AS `Potential Orders`
    FROM 
        df
),
RankedDemand AS (
    SELECT 
        City,
        date(Date) as date,
        Hour,
        CAST(ROUND(`Potential Orders`) as INT) as `Potential Orders`,
        ROW_NUMBER() OVER (PARTITION BY City ORDER BY `Potential Orders` DESC) AS Rank
    FROM 
        PotentialDemand
)
SELECT 
    City,
    Date,
    Hour,
    `Potential Orders`
FROM 
    RankedDemand
WHERE 
    Rank <= 5
ORDER BY 
    City, 
    Rank;
"""

# Execute the SQL query
result = psql.sqldf(query, locals())

# Display the result
print("Query result:")
print(result)

output_file = '/Users/abhisheksingh/Downloads/bolt_task_1.xlsx'
result.to_excel(output_file, index=False)

print(f"Result saved to {output_file}")

