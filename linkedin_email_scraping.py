import re
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
import pandas as pd

opt = webdriver.ChromeOptions()
opt.add_argument("--disable-popup-blocking")


tags = [
    # Put tags here
    "Affiliate Marketing",
    "Performance Marketing",
    # Add as many tags as possible.
]

EMAIL = ['gmail.com', 'outlook.com', 'yahoo.com', 'hotmail.com']

driver = webdriver.Chrome(options=opt)

for TAG in tags:
    for email_domain in EMAIL:
        email_df = pd.DataFrame(columns=["Country", "Tag", "Email"])
        
        TAG = TAG.replace(' ', '+')
        driver.get(f'https://www.google.com/search?q=%22{TAG}%22++-intitle%3A%22profiles%22+-inurl%3A%22dir%2F+%22+email%3A+%22%40{email_domain}%22+site%3Awww.linkedin.com%2Fin%2F+OR+site%3Awww.linkedin.com%2Fpub%2F&sca_esv=579408689&sxsrf=AM9HkKlcbT_aAr_y74r0pDww5DseY1OkPA%3A1699092525996&ei=LRhGZY6lPNSNxc8PhaSu-Ak&ved=0ahUKEwjO787zjKqCAxXURvEDHQWSC58Q4dUDCBA&uact=5&oq=%22{TAG}%22++-intitle%3A%22profiles%22+-inurl%3A%22dir%2F+%22+email%3A+%22%40{email_domain}%22+site%3Awww.linkedin.com%2Fin%2F+OR+site%3Awww.linkedin.com%2Fpub%2F&gs_lp=Egxnd3Mtd2l6LXNlcnAihQEiQWZmaWxpYXRlIE1hcmtldGluZyIgIC1pbnrpdGxlOiJwcm9maWxlcyIgLWludXJsOiJkaXIvICIgZW1haWw6ICJAZ21haWwuY29tIiBzaXRlOnd3dy5saW5rZWRpbi.3mNvbS9wdWIvSABQAFgAcAB4AJABAJgBAKABAKoBALgBA8gBAPgBAeIDBBgAIEE&sclient=gws-wiz-serp')

        time.sleep(random.uniform(9, 14))
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

        for _ in range(random.randint(20, 30)):
            try:
                scroll_down(scroll_amount)
                click_more_results_button()
            except Exception as e:
                print(e)
                continue

        page_source = driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')

        emails = set()

        for element in soup.find_all(['a', 'p', 'span', 'div']):
            text = element.get_text()
            extracted_emails = extract_emails(text)
            for email in extracted_emails:
                emails.add(email)

        TAG = TAG.replace('+', ' ')
        for email in emails:
            new_row = pd.DataFrame({"Country": ["US"], "Tag": [TAG], "Email": [email]})
            email_df = pd.concat([email_df, new_row], ignore_index=True)
        email_df.to_csv(f"./csvs/{TAG}_{email_domain}_email_data.csv", index=False)

driver.quit()

