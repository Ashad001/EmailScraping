# Email Scraping with Selenium

This project is a Python-based educational demonstration of how to scrape emails from web pages using Selenium and BeautifulSoup. The purpose of this project is to provide a hands-on learning experience for those interested in web scraping and data extraction.

## Project Description

The script navigates through Google search results, looking for LinkedIn profiles related to specific marketing tags. It then extracts email addresses found on these pages. The extracted emails are stored in a DataFrame along with the associated tag and country, and finally exported to a CSV file.

## Technologies Used

- Python
- Selenium WebDriver
- BeautifulSoup
- pandas

## How to Run

1. Install the required Python libraries with pip:

```bash
pip install selenium beautifulsoup4 pandas
```

2. Download the appropriate [ChromeDriver](https://sites.google.com/a/chromium.org/chromedriver/) for your system and place it in your PATH.

3. Run the script:

```bash
python linkedin_email_scraping.py
```

## Note

This project is for educational purposes only. Web scraping should be done responsibly and in accordance with the terms of service of the website being scraped. Always respect privacy and do not use this for spam or any form of unsolicited communication.

## Future Improvements

- Implement a more robust error handling system.
- Improve the email extraction process to reduce false positives.


## Acknowledgements

- [Selenium](https://www.selenium.dev/)
- [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
- [pandas](https://pandas.pydata.org/)