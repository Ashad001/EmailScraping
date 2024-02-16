import re
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
import csv
import pandas as pd
import json
import ssl
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import time
import os

def send_email(receiver_email, subject, message):
    smtp_server = "smtp.gmail.com"
    smtp_port = 465
    email_sender = 'ashadq345@gmail.com'
    email_password = 'ifmlgrerqieqrlaf'
    msg = MIMEMultipart()
    msg["Subject"] = subject
    msg["From"] = email_sender
    msg["To"] = receiver_email
    msg.attach(MIMEText(message, "plain"))

    context = ssl.create_default_context()
    server = smtplib.SMTP_SSL(smtp_server, smtp_port, context=context)
    server.login(email_sender, email_password )
    server.sendmail(email_sender, receiver_email, msg.as_string())
    server.quit()

opt = webdriver.ChromeOptions()
opt.add_argument("--disable-popup-blocking")


tags = [
    # "High School Counselor",
    "high school coach",
    "High school teacher",
    "High school advisor",
    "School Guidance Counselor",
    "Educational Counselor",
    "Student Advisor",
    "Career Guidance Counselor",
    "Academic Counselor",
    "College and Career Counselor",
    "Student Support Specialist",
    "Admissions Counselor",
    "School Intervention Counselor",
    "College Planning Advisor",
    "Youth Career Coach",
    "High School Wellness Coordinator",
]


EMAIL = ['gmail.com' ,'outlook.com', 'yahoo.com','hotmail.com']

usa_states = ["Alabama", "Alaska", "Arizona", "Arkansas", "California",  "Colorado","Connecticut", "Delaware",
    "Florida", "Georgia", "Hawaii", "Idaho", "Illinois", "Indiana", "Iowa", "Kansas", "Kentucky", "Louisiana", 
    "Maine", "Maryland", "Massachusetts", "Michigan", "Minnesota",  "Mississippi", "Missouri",
    "Montana", "Nebraska", "Nevada", "New Hampshire", "New Jersey", "New Mexico", "New York", "North Carolina",
    "North Dakota", "Ohio", "Oklahoma", "Oregon", "Pennsylvania", "Rhode Island","South Carolina",
    "South Dakota", "Tennessee", "Texas", "Utah", "Vermont", "Virginia", "Washington", "West Virginia",
    "Wisconsin", "Wyoming",]

# country = 'in'

driver = webdriver.Chrome(options=opt)

if not os.path.exists('./csvs'):
    os.mkdir('./csvs')
if not os.path.exists('./logs'):
    os.mkdir('./logs')

processed = []
if os.path.exists('./logs/processed.txt'):
    with open('./logs/processed.txt', 'r') as f:
        processed = f.read()
        processed = processed.split('\n')



for TAG in tags:
    if TAG in processed:
        print(f"Processed Already: {TAG}")
        continue
    for state in usa_states:
        for email_domain in EMAIL:
            unique_emails = set()  
            email_df = pd.DataFrame(columns=["State", "Tag", "Name", "Email"])

            TAG = TAG.replace(' ', '+')
            # driver.get(f'https://www.google.com/search?q=%22{TAG}%22++-intitle%3A%22profiles%22+-inurl%3A%22dir%2F+%22+email%3A+%22%40{email_domain}%22+site%3A{country}.linkedin.com%2Fin%2F+OR+site%3A{country}.linkedin.com%2Fpub%2F&sca_esv=580067936&sxsrf=AM9HkKmtLt0TG_t_ljUJfbHjL7qCuN306g%3A1699350983830&ei=xwlKZYOSMpaHxc8P0KK2iAg&ved=0ahUKEwjDkfXdz7GCAxWWQ_EDHVCRDYEQ4dUDCBA&uact=5&oq=%22Affiliate+Marketing%22++-intitle%3A%22profiles%22+-inurl%3A%22dir%2F+%22+email%3A+%22%40gmail.com%22+site%3A{country}.linkedin.com%2Fin%2F+OR+site%3A{country}.linkedin.com%2Fpub%2F&gs_lp=Egxnd3Mtd2l6LXNlcnAigwEiQWZmaWxpYXRlIE1hcmtldGluZyIgIC1pbnRpdGxlOiJwcm9maWxlcyIgLWludXJsOiJkaXIvICIgZW1haWw6ICJAZ21haWwuY29tIiBzaXRlOnBrLmxpbmtlZGluLmNvbS9pbi8gT1Igc2l0ZTpway5saW5rZWRpbi5jb20vcHViL0gAUABYAHAAeACQAQCYAQCgAQCqAQC4AQPIAQD4AQL4AQHiAwQYACBB&sclient=gws-wiz-serp')
            driver.get(f'https://www.google.com/search?q=%22{TAG}%22+%22{state}%22+-intitle%3A%22profiles%22+-inurl%3A%22dir%2F+%22+email%3A+%22%40{email_domain}%22+site%3Awww.linkedin.com%2Fin%2F+OR+site%3Awww.linkedin.com%2Fpub%2F&sca_esv=586505729&sxsrf=AM9HkKlmM9qSBgg1YHjj51rdhrAohck7Ng%3A1701319445914&ei=FRNoZZC8N5KRkdUP09-d4AU&ved=0ahUKEwjQmuTp9OqCAxWSSKQEHdNvB1wQ4dUDCBA&uact=5&oq=%22Affiliate+Marketing%22+%22United+States%22+-intitle%3A%22profiles%22+-inurl%3A%22dir%2F+%22+email%3A+%22%40gmail.com%22+site%3Awww.linkedin.com%2Fin%2F+OR+site%3Awww.linkedin.com%2Fpub%2F&gs_lp=Egxnd3Mtd2l6LXNlcnAilAEiQWZmaWxpYXRlIE1hcmtldGluZyIgIlVuaXRlZCBTdGF0ZXMiIC1pbnRpdGxlOiJwcm9maWxlcyIgLWludXJsOiJkaXIvICIgZW1haWw6ICJAZ21haWwuY29tIiBzaXRlOnd3dy5saW5rZWRpbi5jb20vaW4vIE9SIHNpdGU6d3d3LmxpbmtlZGluLmNvbS9wdWIvSABQAFgAcAB4AJABAJgBAKABAKoBALgBA8gBAPgBAeIDBBgAIEE&sclient=gws-wiz-serp')
            time.sleep(random.uniform(12, 30))
            scroll_amount = 30

            def scroll_down(scroll_amount):
                driver.execute_script("window.scrollBy(0, window.innerHeight);")
                time.sleep(random.uniform(2, 9))

            def click_more_results_button():
                try:
                    more_results_button = driver.find_element(By.XPATH, "//*[@id='botstuff']/div/div[3]/div[4]/a[1]/h3/div")
                    more_results_button.click()
                    print('Button Clicked')
                    time.sleep(2)
                except Exception as e:
                    print("More results button not found")
                    return

            def extract_emails(text):
                email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
                return re.findall(email_pattern, text)

            for _ in range(random.randint(25, 30)):
                try:
                    scroll_down(scroll_amount)
                    click_more_results_button()
                except Exception as e:
                    print(e)
                    continue

            page_source = driver.page_source
            captcha_present = any(keyword in page_source for keyword in ["CAPTCHA", "Captcha", "captcha"])

            if captcha_present:
                subject = "Captcha Detected!"
                body = "Captcha detected on the website. Please check and solve it manually."
                send_email("ashad001sp@gmail.com", subject, body)
                with open('captchas_file.txt', 'a', encoding='utf-8') as f:
                    time_detected = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                    f.write(f"{time_detected}, {TAG}, {state}, {email_domain}\n")
                exit(0)

            soup = BeautifulSoup(page_source, 'html.parser')
            elements = soup.find_all(class_="MjjYud")
            TAG = TAG.replace('+', ' ')
            for element in elements:
                block = element.get_text()
                name = block.split(' - ')[0]
                if len(name) > 25:
                    temp = name.split(' ')[:2]
                    name = " ".join(temp)
                    if len(name.split(' ')[1]) < 3 or len(name.split(' ')[1]) >= 20:
                        name = name.split(' ')[0]
                        
                email = extract_emails(block)
                if name != "" and email != []:
                    if email[0] not in unique_emails:
                        unique_emails.add(email[0])
                        new_row = pd.DataFrame({"State": [state.upper()], "Tag": [TAG], "Name": [name], "Email": [email[0]]})
                        email_df = pd.concat([email_df, new_row], ignore_index=True)
            email_df.to_csv(f"./csvs/{state.upper()}_{TAG}_{email_domain}_email_data.csv", index=False)
    with open('./logs/processed.txt', 'a') as f:
        f.write(f'{TAG}')
driver.quit()
