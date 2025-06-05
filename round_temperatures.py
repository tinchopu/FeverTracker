import pandas as pd

# Read the CSV file
df = pd.read_csv('temperature_data.csv')

# Round temperature values to 1 decimal place
df['temperature'] = df['temperature'].round(1)

# Save back to CSV
df.to_csv('temperature_data.csv', index=False)

print("Successfully rounded all temperature values to 1 decimal place.")
