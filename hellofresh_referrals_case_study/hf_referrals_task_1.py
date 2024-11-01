import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pandasql import sqldf

# Step 1: Read the CSV file with the correct delimiter
csv_file = '/Users/abhisheksingh/Downloads/Copy_of_virality_data_analyst_recruiting_test_2024.csv'
df = pd.read_csv(csv_file, delimiter=';')

# Step 2: Convert week column to datetime for proper calculations
df['delivery_week'] = pd.to_datetime(df['delivery_week'] + '-1', format='%Y-W%U-%w')

# Step 3: Use pandasql to run SQL queries
pysqldf = lambda q: sqldf(q, globals())

# SQL query
query = """
WITH base AS (
    SELECT *
    FROM df
    WHERE substr(strftime('%Y', delivery_week), 1, 4) = '2022'
),
CustomerCohorts AS (
    SELECT
        customer_id,
        customer_acquisition_channel,
        MIN(delivery_week) AS acquisition_week
    FROM base
    GROUP BY customer_id, customer_acquisition_channel
),
CohortMetrics AS (
    SELECT
        cc.acquisition_week,
        cc.customer_acquisition_channel,
        d.delivery_week,
        CAST(strftime('%W', d.delivery_week) AS INTEGER) - CAST(strftime('%W', cc.acquisition_week) AS INTEGER) AS weeks_since_acquisition,
        COUNT(DISTINCT d.customer_id) AS active_customers,
        SUM(d.net_revenue) AS total_net_revenue,
        SUM(d.gross_revenue) AS total_gross_revenue,
        SUM(d.gross_revenue - d.net_revenue) AS total_discount
    FROM CustomerCohorts cc
    JOIN base d ON cc.customer_id = d.customer_id
    WHERE weeks_since_acquisition >= 0
    GROUP BY cc.acquisition_week, cc.customer_acquisition_channel, weeks_since_acquisition
),
CohortBase AS (
    SELECT
        acquisition_week,
        customer_acquisition_channel,
        COUNT(DISTINCT customer_id) AS acquired_customers
    FROM CustomerCohorts
    GROUP BY acquisition_week, customer_acquisition_channel
),
CohortRetention AS (
    SELECT
        cm.acquisition_week,
        cm.customer_acquisition_channel,
        cm.weeks_since_acquisition,
        SUM(cm.active_customers) AS active_customers,
        cb.acquired_customers,
        SUM(cm.total_net_revenue) AS total_net_revenue,
        SUM(cm.total_gross_revenue) AS total_gross_revenue,
        SUM(cm.total_discount) AS total_discount
    FROM CohortMetrics cm
    JOIN CohortBase cb ON cm.acquisition_week = cb.acquisition_week AND cm.customer_acquisition_channel = cb.customer_acquisition_channel
    GROUP BY cm.acquisition_week, cm.customer_acquisition_channel, cm.weeks_since_acquisition, cb.acquired_customers
)
SELECT
    acquisition_week,
    customer_acquisition_channel,
    weeks_since_acquisition,
    active_customers,
    acquired_customers,
    (active_customers * 100.0 / acquired_customers) AS retention_rate,
    total_net_revenue,
    total_gross_revenue,
    total_discount,
    (total_discount * 100.0 / total_gross_revenue) AS discount_rate
FROM CohortRetention
ORDER BY acquisition_week, customer_acquisition_channel, weeks_since_acquisition;
"""

# Execute the SQL query using pandasql
result_df = pysqldf(query)

# Display the result
print(result_df.head())

# Step 4: Plotting the results
# Plot retention rate
plt.figure(figsize=(12, 6))
sns.lineplot(data=result_df, x='weeks_since_acquisition', y='retention_rate', hue='customer_acquisition_channel')
plt.title('Weekly Retention Rate by Acquisition Channel')
plt.xlabel('Weeks Since Acquisition')
plt.ylabel('Retention Rate (%)')
plt.legend(title='Acquisition Channel')
plt.grid(True)
plt.show()

# Plot net revenue and discount rate
fig, ax1 = plt.subplots(figsize=(12, 6))

color = 'tab:blue'
ax1.set_xlabel('Weeks Since Acquisition')
ax1.set_ylabel('Total Net Revenue', color=color)
sns.lineplot(data=result_df, x='weeks_since_acquisition', y='total_net_revenue', hue='customer_acquisition_channel', ax=ax1)
ax1.tick_params(axis='y', labelcolor=color)
ax1.legend(title='Acquisition Channel', loc='upper left')

ax2 = ax1.twinx()
color = 'tab:green'
ax2.set_ylabel('Discount Rate (%)', color=color)
sns.lineplot(data=result_df, x='weeks_since_acquisition', y='discount_rate', hue='customer_acquisition_channel', ax=ax2, linestyle='--')
ax2.tick_params(axis='y', labelcolor=color)
ax2.legend(title='Acquisition Channel', loc='upper right')

plt.title('Weekly Net Revenue and Discount Rate by Acquisition Channel')
plt.grid(True)
plt.show()
