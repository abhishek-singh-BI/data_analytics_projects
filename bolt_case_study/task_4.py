import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from statsmodels.tsa.arima.model import ARIMA
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt

# Load data
excel_file = '/Users/abhisheksingh/Downloads/Marketplace Ops - Home Task.xlsx'
demand_data = pd.read_excel(excel_file, sheet_name='Demand')
supply_data = pd.read_excel(excel_file, sheet_name='Supply')

# Filter for Warsaw
warsaw_demand = demand_data[demand_data['City'] == 'Warsaw'].copy()
warsaw_supply = supply_data[supply_data['City'] == 'Warsaw'].copy()

# Convert Date column to datetime
warsaw_demand['Date'] = pd.to_datetime(warsaw_demand['Date'])
warsaw_supply['Date'] = pd.to_datetime(warsaw_supply['Date'])

# Aggregate by week
warsaw_demand['Week'] = warsaw_demand['Date'].dt.isocalendar().week
warsaw_supply['Week'] = warsaw_supply['Date'].dt.isocalendar().week

weekly_demand = warsaw_demand.groupby(['Week']).agg({
    'Completed Orders': 'sum'
}).reset_index()

weekly_supply = warsaw_supply.groupby(['Week']).agg({
    'Online Hours': 'sum'
}).reset_index()

# Merge demand and supply data
weekly_data = pd.merge(weekly_demand, weekly_supply, on='Week')

# Create lagged features
for lag in range(1, 5):
    weekly_data[f'Orders_Lag_{lag}'] = weekly_data['Completed Orders'].shift(lag)
    weekly_data[f'Hours_Lag_{lag}'] = weekly_data['Online Hours'].shift(lag)

# Drop NaN values created by lagged features
weekly_data = weekly_data.dropna()

# Split data into training and testing sets
train_data, test_data = train_test_split(weekly_data, test_size=0.2, shuffle=False)

# Define features and target
features = [col for col in weekly_data.columns if 'Lag' in col]
target_orders = 'Completed Orders'
target_hours = 'Online Hours'

# Train models
def train_models(train_data, test_data, features, target):
    models = {
        'Linear Regression': LinearRegression(),
        'Random Forest': RandomForestRegressor(),
        'ARIMA': None  # Placeholder for ARIMA
    }

    # Fit Linear Regression and Random Forest
    for model_name, model in models.items():
        if model_name != 'ARIMA':
            model.fit(train_data[features], train_data[target])
            models[model_name] = model

    # Fit ARIMA separately
    arima_model = ARIMA(train_data[target], order=(5, 1, 0)).fit()
    models['ARIMA'] = arima_model

    # Make predictions
    predictions = {}
    for model_name, model in models.items():
        if model_name == 'ARIMA':
            preds = model.forecast(steps=len(test_data))
            preds = preds[:len(test_data)]  # Ensure predictions have the same length as the test set
        else:
            preds = model.predict(test_data[features])
        predictions[model_name] = preds

    return models, predictions

# Evaluate models
def evaluate_models(test_data, target, predictions):
    rmse_scores = {}
    for model_name, preds in predictions.items():
        rmse = np.sqrt(mean_squared_error(test_data[target], preds))
        rmse_scores[model_name] = rmse
    return rmse_scores

# Train and evaluate for orders
orders_models, orders_predictions = train_models(train_data, test_data, features, target_orders)
orders_rmse_scores = evaluate_models(test_data, target_orders, orders_predictions)

# Train and evaluate for online hours
hours_models, hours_predictions = train_models(train_data, test_data, features, target_hours)
hours_rmse_scores = evaluate_models(test_data, target_hours, hours_predictions)

# Select best models based on RMSE
best_orders_model_name = min(orders_rmse_scores, key=orders_rmse_scores.get)
best_orders_model = orders_models[best_orders_model_name]

best_hours_model_name = min(hours_rmse_scores, key=hours_rmse_scores.get)
best_hours_model = hours_models[best_hours_model_name]

# Forecast next 4 weeks using the best models
future_weeks = np.arange(weekly_data['Week'].max() + 1, weekly_data['Week'].max() + 5)

# Prepare features for the forecast
future_features = weekly_data[features].iloc[-4:].values

# Using the best model for orders
if best_orders_model_name == 'ARIMA':
    future_orders = best_orders_model.forecast(steps=4)
else:
    future_orders = best_orders_model.predict(future_features)

# Using the best model for hours
if best_hours_model_name == 'ARIMA':
    future_hours = best_hours_model.forecast(steps=4)
else:
    future_hours = best_hours_model.predict(future_features)

# Ensure future predictions have the correct length for plotting
if len(future_orders) < 4:
    future_orders = np.append(future_orders, [np.nan] * (4 - len(future_orders)))
if len(future_hours) < 4:
    future_hours = np.append(future_hours, [np.nan] * (4 - len(future_hours)))

# Print future predictions
print(f"Future Orders: {future_orders}")
print(f"Future Hours: {future_hours}")

# Plot the results
plt.figure(figsize=(14, 7))

plt.subplot(2, 1, 1)
plt.plot(weekly_data['Week'], weekly_data[target_orders], label='Actual Orders')
plt.plot(future_weeks, future_orders, label='Predicted Orders', linestyle='--')
plt.title('Orders Prediction')
plt.xlabel('Week')
plt.ylabel('Orders')
plt.legend()

plt.subplot(2, 1, 2)
plt.plot(weekly_data['Week'], weekly_data[target_hours], label='Actual Online Hours')
plt.plot(future_weeks, future_hours, label='Predicted Online Hours', linestyle='--')
plt.title('Online Hours Prediction')
plt.xlabel('Week')
plt.ylabel('Online Hours')
plt.legend()

plt.tight_layout()
plt.show()

# Generate a summary report
summary = {
    'Best Model for Orders': best_orders_model_name,
    'Orders RMSE': orders_rmse_scores[best_orders_model_name],
    'Best Model for Online Hours': best_hours_model_name,
    'Hours RMSE': hours_rmse_scores[best_hours_model_name],
    'Future Orders': future_orders,
    'Future Online Hours': future_hours
}

print(summary)
