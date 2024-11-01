import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the summary statistics from the Excel file
file_path = '/mnt/data/image.png'  # Update this path to your file path
summary_stats = pd.read_excel(file_path)

# Ensure the correct data types
summary_stats = summary_stats.apply(pd.to_numeric, errors='coerce')

# Plot the mean values of numerical columns
plt.figure(figsize=(10, 6))
summary_stats.loc['mean'].plot(kind='bar')
plt.title('Mean Values of Numerical Columns')
plt.ylabel('Mean')
plt.show()

# Box plots for numerical columns
plt.figure(figsize=(14, 8))
sns.boxplot(data=summary_stats.loc[['25%', '50%', '75%', 'min', 'max', 'mean', 'std']].T)
plt.title('Box Plot of Numerical Columns')
plt.xticks(rotation=45)
plt.show()

# Count plot for categorical columns
categorical_columns = ['is_app', 'is_repeater', 'clickouts', 'bookings', 'session_duration', 'total_ctp']

for column in categorical_columns:
    plt.figure(figsize=(10, 6))
    sns.countplot(x=summary_stats.loc[:, column])
    plt.title(f'Count of Sessions by {column}')
    plt.show()
