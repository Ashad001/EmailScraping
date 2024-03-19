import os
import pandas as pd
from CREDS import FOLDER_NAME
from concurrent.futures import ThreadPoolExecutor

def process_csv(file):
    file_path = os.path.join(csv_directory, file)
    data = pd.read_csv(file_path)
    return data

csv_directory = './csvs' + '/' + FOLDER_NAME
csv_files = [file for file in os.listdir(csv_directory) if file.endswith('.csv')]
print(csv_files)

combined_data = pd.DataFrame(columns=["State", "Tag", "Name", "Email"])

with ThreadPoolExecutor() as executor:
    futures = [executor.submit(process_csv, file) for file in csv_files]
    for future in futures:
        data = future.result()
        combined_data = pd.concat([combined_data, data], ignore_index=True)

if not os.path.exists('combined_csvs'):
    os.makedirs('combined_csvs')
    
if not os.path.exists(f'./combined_csvs/' + FOLDER_NAME):
    os.makedirs(f'./combined_csvs/' + FOLDER_NAME)

combined_file = './combined_csvs/' + FOLDER_NAME + '/combined_email_data.csv'
combined_data.to_csv(combined_file, index=False)
