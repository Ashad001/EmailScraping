import re
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
import pandas as pd
import json

if not os.path.exists('./csvs'):
    os.mkdir('./csvs')

opt = webdriver.ChromeOptions()
opt.add_argument("--disable-popup-blocking")

EMAIL = ['gmail.com' , 'outlook.com', 'yahoo.com', 'hotmail.com']

tags = [
    # Put tags here
    "Affiliate Marketing",
    "Performance Marketing",
    # Add as many tags as possible.
]

country = 'us'

driver = webdriver.Chrome(options=opt)

for TAG in tags:
    for email_domain in EMAIL:
        unique_emails = set()  
        email_df = pd.DataFrame(columns=["Country", "Tag", "Name", "Email"])

        TAG = TAG.replace(' ', '+')
        driver.get(f'https://www.google.com/search?q=%22{TAG}%22++-intitle%3A%22profiles%22+-inurl%3A%22dir%2F+%22+email%3A+%22%40{email_domain}%22+site%3A{country}.linkedin.com%2Fin%2F+OR+site%3A{country}.linkedin.com%2Fpub%2F&sca_esv=580067936&sxsrf=AM9HkKmtLt0TG_t_ljUJfbHjL7qCuN306g%3A1699350983830&ei=xwlKZYOSMpaHxc8P0KK2iAg&ved=0ahUKEwjDkfXdz7GCAxWWQ_EDHVCRDYEQ4dUDCBA&uact=5&oq=%22Affiliate+Marketing%22++-intitle%3A%22profiles%22+-inurl%3A%22dir%2F+%22+email%3A+%22%40gmail.com%22+site%3A{country}.linkedin.com%2Fin%2F+OR+site%3A{country}.linkedin.com%2Fpub%2F&gs_lp=Egxnd3Mtd2l6LXNlcnAigwEiQWZmaWxpYXRlIE1hcmtldGluZyIgIC1pbnRpdGxlOiJwcm9maWxlcyIgLWludXJsOiJkaXIvICIgZW1haWw6ICJAZ21haWwuY29tIiBzaXRlOnBrLmxpbmtlZGluLmNvbS9pbi8gT1Igc2l0ZTpway5saW5rZWRpbi5jb20vcHViL0gAUABYAHAAeACQAQCYAQCgAQCqAQC4AQPIAQD4AQL4AQHiAwQYACBB&sclient=gws-wiz-serp')
        
        time.sleep(random.uniform(20, 30))
        scroll_amount = 30

        def scroll_down(scroll_amount):
            driver.execute_script("window.scrollBy(0, window.innerHeight);")
            time.sleep(random.uniform(5, 9))

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

        for _ in range(random.randint(2, 4)):
            try:
                scroll_down(scroll_amount)
                click_more_results_button()
            except Exception as e:
                print(e)
                continue

        page_source = driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')
        elements = soup.find_all(class_="MjjYud")
        TAG = TAG.replace('+', ' ')
        for element in elements:
            block = element.get_text()
            name = block.split(' - ')[0]
            if len(name) > 25:
                temp = block.split(' ')[:2]
                name = " ".join(temp)
            email = extract_emails(block)
            if name != "" and email != []:
                if email[0] not in unique_emails:
                    unique_emails.add(email[0])
                    new_row = pd.DataFrame({"Country": [country.upper()], "Tag": [TAG], "Name": [name], "Email": [email[0]]})
                    email_df = pd.concat([email_df, new_row], ignore_index=True)

        email_df.to_csv(f"./csvs/{country.upper()}_{TAG}_{email_domain}_email_data.csv", index=False)

driver.quit()
