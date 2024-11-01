import pandas as pd

# Step 1: Read the Excel file
excel_file = '/Users/abhisheksingh/Downloads/202303_Task1_Sessions.xlsx'
df = pd.read_excel(excel_file, sheet_name='in', header=None, names=['A'])

# Step 2: Split values in Column A into separate columns
df = df['A'].str.split(',', expand=True)

# Step 3: Optionally, convert columns to appropriate data types if needed
# df = df.apply(pd.to_numeric, errors='coerce')  # Example: Convert to numeric

# Step 4: Display the resulting dataframe
print(df.head())  # Display first few rows to verify

# Optionally, save the processed dataframe to a new Excel file
df.to_excel('/Users/abhisheksingh/Downloads/202303_Task1_Sessions_Clean_final.xlsx', index=False)

