import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

# Step 1: Read the CSV file with the correct delimiter
csv_file = '/Users/abhisheksingh/Downloads/Copy_of_virality_data_analyst_recruiting_test_2024.csv'
df = pd.read_csv(csv_file, delimiter=';')

# Convert delivery_week to datetime
df['delivery_week'] = df['delivery_week'].apply(lambda x: datetime.strptime(x + '-1', "%Y-W%W-%w"))

# Aggregate data to get weekly totals
weekly_data = df.groupby('delivery_week').agg({'boxes': 'sum'}).reset_index()

# Prepare data for prediction
weekly_data['week_number'] = weekly_data['delivery_week'].dt.isocalendar().week
weekly_data['year'] = weekly_data['delivery_week'].dt.year

# Pivot table to get weekly data by year
pivot_data = weekly_data.pivot(index='week_number', columns='year', values='boxes').fillna(0)

# Calculate mean boxes shipped for each week
pivot_data['mean'] = pivot_data.mean(axis=1)

# Predict boxes for the first 4 weeks of 2023
predicted_boxes = pivot_data['mean'].loc[1:4]

print("Predicted number of boxes for 2023-W01 to 2023-W04:")
print(predicted_boxes)

# Plotting the results
plt.figure(figsize=(10, 5))
plt.plot(pivot_data.index, pivot_data['mean'], label='Average Boxes Shipped')
plt.scatter(predicted_boxes.index, predicted_boxes, color='red', label='Predicted Boxes for 2023')
plt.title('Weekly Boxes Shipped and Prediction for 2023')
plt.xlabel('Week Number')
plt.ylabel('Number of Boxes')
plt.legend()
plt.grid(True)
plt.show()
