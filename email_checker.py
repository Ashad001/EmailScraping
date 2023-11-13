import csv
import re

class EmailProcessor:
    def __init__(self, input_file_path, valid_output_file_path, invalid_output_file_path):
        self.input_file_path = input_file_path
        self.valid_output_file_path = valid_output_file_path
        self.invalid_output_file_path = invalid_output_file_path
        self.emails = set()
        self.valid_rows = []
        self.invalid_rows = []

    def is_valid_email(self, email):
        email_pattern = r'^[a-zA-Z0-9._%+-]{3,}@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,3}$'
        return re.match(email_pattern, email)

    def remove_emojis(self, input_string):
        emoji_pattern = re.compile("["
                u"\U0001F600-\U0001F64F"  
                u"\U0001F300-\U0001F5FF"   
                u"\U0001F680-\U0001F6FF"   
                u"\U0001F700-\U0001F77F"   
                u"\U0001F780-\U0001F7FF"  
                u"\U0001F800-\U0001F8FF"  
                u"\U0001F900-\U0001F9FF"    
                u"\U0001FA00-\U0001FA6F"   
                u"\U0001FA70-\U0001FAFF"    
                u"\U00002702-\U000027B0"   
                u"\U000024C2-\U0001F251" 
            "]+", flags=re.UNICODE)

        result_string = emoji_pattern.sub(r'', input_string)

        return result_string

    def process_emails(self):
        with open(self.input_file_path, mode='r',encoding='utf-8', newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                email = row.get('Email')
                name = row.get('Name')
                name = self.remove_emojis(name)
                if email:
                    email = email.strip()
                    if email in self.emails:
                        # Duplicate email, skip it
                        continue

                    if '@' in email and self.is_valid_email(email):
                        self.emails.add(email)
                        row['Name'] = name  # Update the 'Name' field with the modified name
                        self.valid_rows.append(row)
                    else:
                        row['Name'] = name  # Update the 'Name' field with the modified name
                        self.invalid_rows.append(row)

    def save_emails_to_file(self, rows, output_file_path):
        with open(output_file_path, mode='w',encoding='utf-8', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=rows[0].keys())
            writer.writeheader()
            writer.writerows(rows)

    def process_and_save_emails(self):
        self.process_emails()
        self.save_emails_to_file(self.valid_rows, self.valid_output_file_path)
        self.save_emails_to_file(self.invalid_rows, self.invalid_output_file_path)

if __name__ == '__main__':
    input_file = 'combined_email_data.csv'
    valid_output_file = 'emails.csv'
    invalid_output_file = 'invalid_emails.csv'

    processor = EmailProcessor(input_file, valid_output_file, invalid_output_file)
    processor.process_and_save_emails()

    print(f"Valid emails are saved in '{valid_output_file}'")
    print(f"Invalid emails are saved in '{invalid_output_file}'")
