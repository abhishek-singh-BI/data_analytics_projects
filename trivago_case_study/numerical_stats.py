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

# Step 3: Convert columns to appropriate data types
df['ymd'] = pd.to_datetime(df['ymd'], format='%Y%m%d')
df['arrival_day'] = pd.to_datetime(df['arrival_day'], format='%Y%m%d', errors='coerce')
df['departure_day'] = pd.to_datetime(df['departure_day'], format='%Y%m%d', errors='coerce')
df['is_app'] = pd.to_numeric(df['is_app'], errors='coerce')
df['is_repeater'] = pd.to_numeric(df['is_repeater'], errors='coerce')
df['clickouts'] = pd.to_numeric(df['clickouts'], errors='coerce')
df['bookings'] = pd.to_numeric(df['bookings'], errors='coerce')
df['session_duration'] = pd.to_numeric(df['session_duration'], errors='coerce')
df['total_ctp'] = pd.to_numeric(df['total_ctp'], errors='coerce')

# Step 4: Replace placeholder values with NaN
df.replace('\\N', pd.NA, inplace=True)

# Step 5: Generate summary statistics for numerical columns
numeric_columns = ['is_app', 'is_repeater', 'clickouts', 'bookings', 'session_duration', 'total_ctp']
summary_stats = df[numeric_columns].describe()

# Summary statistics for categorical columns
categorical_columns = ['platform', 'traffic_type', 'country_name']
categorical_stats = df[categorical_columns].describe()

# Summary statistics for datetime columns
date_columns = ['ymd', 'arrival_day', 'departure_day']
date_stats = df[date_columns].agg(['min', 'max', 'mean'])

print("Numeric Summary Statistics:")
print(summary_stats)
print("\nCategorical Summary Statistics:")
print(categorical_stats)
print("\nDate Summary Statistics:")
print(date_stats)

# Optionally, save the processed dataframe to a new Excel file
summary_stats.to_excel('/Users/abhisheksingh/Downloads/summary_statistics_1.xlsx', sheet_name='Summary')
