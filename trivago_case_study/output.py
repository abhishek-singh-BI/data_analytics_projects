import pandas as pd
from pandasql import sqldf

# Step 1: Read the Excel file
excel_file = '/Users/abhisheksingh/Downloads/202303_Task1_Sessions.xlsx'
df = pd.read_excel(excel_file, sheet_name='in', header=1, names=['A'])

# Step 2: Split values in Column A into separate columns
df = df['A'].str.split(',', expand=True)

df.columns = ['ymd', 'session_id', 'tracking_id', 'platform', 'is_app', 'is_repeater',
              'traffic_type', 'country_name', 'agent_id', 'clickouts', 'bookings',
              'session_duration', 'entry_page', 'total_ctp', 'arrival_day', 'departure_day', 'na1', 'na2']

# Step 3: Optionally, convert columns to appropriate data types if needed
# df = df.apply(pd.to_numeric, errors='coerce')  # Example: Convert to numeric

# Step 4: Display the resulting dataframe
print(df.head())  # Display first few rows to verify

pysqldf = lambda q: sqldf(q, globals())

# Example SQL query to select specific columns and filter data
query = """
SELECT ymd, session_id, tracking_id, country_name
FROM df
WHERE country_name='United Kingdom'
"""

# Execute the SQL query using pandasql
result_df = pysqldf(query)

# Display the result
print(result_df.head())
df.to_excel('/Users/abhisheksingh/Downloads/202303_Task1_Sessions_clean.xlsx', index=False)
##descriptive analysis
#Select sessions with no bookings but clicks-->empty conversions
#Select sessions with bookings and clicks
#Look at repeat bookings


