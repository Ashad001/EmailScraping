import os
import pandas as pd

csv_directory = r'E:\FifthSem\RAIN\messagingAutomation\csvs'
csv_files = [file for file in os.listdir(csv_directory) if file.endswith('.csv')]
print(csv_files)
combined_data = pd.DataFrame(columns=["Country", "Tag", "Email"])
for csv_file in csv_files:
    file_path = os.path.join(csv_directory, csv_file)
    data = pd.read_csv(file_path)
    combined_data = pd.concat([combined_data, data], ignore_index=True)
combined_data.to_csv('combined_email_data.csv', index=False)
