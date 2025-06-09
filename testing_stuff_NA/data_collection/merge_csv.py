import os
import pandas as pd

# Directory containing the CSV files
csv_dir = os.path.join(os.path.dirname(__file__), 'location_csv')

# List to store dataframes
dataframes = []

# Iterate through all CSV files in the directory
for file_name in os.listdir(csv_dir):
    if file_name.endswith('.csv'):
        file_path = os.path.join(csv_dir, file_name)
        df = pd.read_csv(file_path)
        dataframes.append(df)

# Merge all dataframes
merged_df = pd.concat(dataframes, ignore_index=True)

# Save the merged dataframe to the root directory
output_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'merged_output.csv')
merged_df.to_csv(output_path, index=False)

print(f"Merged CSV saved at: {output_path}")