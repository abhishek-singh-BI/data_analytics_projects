import pandas as pd

# Load your data

# Path to the Excel file
excel_file = '/Users/abhisheksingh/Downloads/Marketplace Ops - Home Task.xlsx'

sheet_name = 'Demand'
demand_data = pd.read_excel(excel_file, sheet_name=sheet_name)

sheet_name_2 = 'Supply'
supply_data = pd.read_excel(excel_file, sheet_name=sheet_name_2)

# Convert to appropriate data types
demand_data['Date'] = pd.to_datetime(demand_data['Date'])
supply_data['Date'] = pd.to_datetime(supply_data['Date'])

# Extract week number
demand_data['Week'] = demand_data['Date'].dt.isocalendar().week
supply_data['Week'] = supply_data['Date'].dt.isocalendar().week

# Calculate potential orders
demand_data['Potential Orders'] = demand_data['Completed Orders'] * (1 + demand_data['Shrinkage %'] * 0.25 / 100)

# Aggregate data by week
weekly_demand = demand_data.groupby(['City', 'Week']).agg({
    'Completed Orders': 'sum',
    'Shrinkage %': 'mean',
    'Potential Orders': 'sum'
}).reset_index()

# Identify the week with the highest shrinkage per city
highest_shrinkage = weekly_demand.loc[weekly_demand.groupby('City')['Shrinkage %'].idxmax()].reset_index(drop=True)

# Calculate additional courier hours and cost
highest_shrinkage['Additional Courier Hours'] = highest_shrinkage['Shrinkage %'] * 0.25
highest_shrinkage['Cost'] = highest_shrinkage['Additional Courier Hours'] * 8

# Calculate additional revenue
highest_shrinkage['Revenue per Order'] = 16 * 0.25 + 1
highest_shrinkage['Additional Revenue'] = highest_shrinkage['Potential Orders'] * highest_shrinkage['Revenue per Order']

# Output results
print(highest_shrinkage)

output_file = '/Users/abhisheksingh/Downloads/bolt_task_3.xlsx'
highest_shrinkage.to_excel(output_file, index=False)

print(f"Result saved to {output_file}")
