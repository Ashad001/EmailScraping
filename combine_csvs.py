import os
import pandas as pd
from CREDS import FOLDER_NAME
from concurrent.futures import ThreadPoolExecutor

class CSVProcessor:
    def __init__(self):
        self.csv_directory = './csvs' + '/' + FOLDER_NAME
        self.combined_data = pd.DataFrame(columns=["State", "Tag", "Name", "Email"])

    def process_csv(self, file):
        file_path = os.path.join(self.csv_directory, file)
        data = pd.read_csv(file_path)
        return data

    def combine_csvs(self):
        self.csv_files = [file for file in os.listdir(self.csv_directory) if file.endswith('.csv')]
        with ThreadPoolExecutor() as executor:
            futures = [executor.submit(self.process_csv, file) for file in self.csv_files]
            for future in futures:
                data = future.result()
                self.combined_data = pd.concat([self.combined_data, data], ignore_index=True)

    def save_combined_csv(self):
        if not os.path.exists('combined_csvs'):
            os.makedirs('combined_csvs')
        
        if not os.path.exists(f'./combined_csvs/' + FOLDER_NAME):
            os.makedirs(f'./combined_csvs/' + FOLDER_NAME)

        combined_file = './combined_csvs/' + FOLDER_NAME + '/combined_email_data.csv'
        self.combined_data.to_csv(combined_file, index=False)

if __name__ == "__main__":
    processor = CSVProcessor()
    processor.combine_csvs()
    processor.save_combined_csv()
