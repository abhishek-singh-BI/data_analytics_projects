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
# Convert 'ymd' to datetime for easier manipulation
df['ymd'] = pd.to_datetime(df['ymd'], format='%Y%m%d', errors='coerce')
df['session_duration'] = pd.to_numeric(df['session_duration'], errors='coerce')
df['clickouts'] = pd.to_numeric(df['clickouts'], errors='coerce')
df['bookings'] = pd.to_numeric(df['bookings'], errors='coerce')
df['total_ctp'] = pd.to_numeric(df['total_ctp'], errors='coerce')

# Drop columns 'na1' and 'na2' if they contain mostly null or irrelevant data
df = df.drop(columns=['na1', 'na2'])

# Display the resulting dataframe
print(df.head())  # Display first few rows to verify

# Step 4: Descriptive statistics
# Summary statistics
summary_stats = df.describe(include='all')
print("\nSummary Statistics:")
print(summary_stats)

# Group by traffic_type and calculate mean session duration, clickouts, and bookings
traffic_type_stats = df.groupby('traffic_type').agg({
    'session_duration': 'mean',
    'clickouts': 'mean',
    'bookings': 'mean'
}).reset_index()
print("\nStatistics by Traffic Type:")
print(traffic_type_stats)

# Count of sessions per country
country_sessions = df['country_name'].value_counts().reset_index()
country_sessions.columns = ['country_name', 'session_count']
print("\nSession Count by Country:")
print(country_sessions)

# Count of sessions per platform
platform_sessions = df['platform'].value_counts().reset_index()
platform_sessions.columns = ['platform', 'session_count']
print("\nSession Count by Platform:")
print(platform_sessions)

# Count of repeat sessions
repeat_sessions = df['is_repeater'].value_counts().reset_index()
repeat_sessions.columns = ['is_repeater', 'session_count']
print("\nCount of Repeat Sessions:")
print(repeat_sessions)

# Calculate conversion rate (bookings/clickouts) only where clickouts > 0 to avoid division by zero
df['conversion_rate'] = df.apply(lambda row: row['bookings'] / row['clickouts'] if row['clickouts'] > 0 else 0, axis=1)
conversion_rate_stats = df['conversion_rate'].describe()
print("\nConversion Rate Statistics:")
print(conversion_rate_stats)

# Saving the summary statistics to an Excel file
summary_stats.to_excel('/Users/abhisheksingh/Downloads/summary_statistics.xlsx', sheet_name='Summary')
traffic_type_stats.to_excel('/Users/abhisheksingh/Downloads/traffic_type_statistics.xlsx', sheet_name='Traffic_Type')
country_sessions.to_excel('/Users/abhisheksingh/Downloads/country_sessions.xlsx', sheet_name='Country')
platform_sessions.to_excel('/Users/abhisheksingh/Downloads/platform_sessions.xlsx', sheet_name='Platform')
repeat_sessions.to_excel('/Users/abhisheksingh/Downloads/repeat_sessions.xlsx', sheet_name='Repeat')
conversion_rate_stats.to_excel('/Users/abhisheksingh/Downloads/conversion_rate_statistics.xlsx', sheet_name='Conversion_Rate')

# Conversion rate by traffic type
traffic_conversion = df.groupby('traffic_type')['conversion_rate'].describe()
print("\nConversion Rate by Traffic Type:")
print(traffic_conversion)

# Conversion rate by country
country_conversion = df.groupby('country_name')['conversion_rate'].describe()
print("\nConversion Rate by Country:")
print(country_conversion)

# Conversion rate by platform
platform_conversion = df.groupby('platform')['conversion_rate'].describe()
print("\nConversion Rate by Platform:")
print(platform_conversion)

# Conversion rate by repeater status
repeater_conversion = df.groupby('is_repeater')['conversion_rate'].describe()
print("\nConversion Rate by Repeater Status:")
print(repeater_conversion)
