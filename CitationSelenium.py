# -*- coding: utf-8 -*-
"""
Created on Fri Nov 22 10:12:44 2024

# Thanks to ChatGPT! 
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import time

# Set up ChromeDriver (adjust the path to ChromeDriver if necessary)
chrome_driver_path = "path/to/chromedriver"  # Replace with your ChromeDriver path
service = Service(chrome_driver_path)
driver = webdriver.Chrome(service=service)

def fetch_google_scholar_articles(url):
    """
    Fetches article titles and publication years from a Google Scholar profile.
    """
    driver.get(url)
    time.sleep(3)  # Wait for the page to fully load

    # Scroll to the bottom of the page to load more articles, if necessary
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)  # Wait for new content to load
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    # Get page source and parse with BeautifulSoup
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")

    # Extract article titles and years
    articles = []
    for item in soup.select(".gs_rt"):  # CSS selector for article titles
        title = item.text.strip()
        articles.append(title)

    years = []
    for year_info in soup.select(".gs_a"):  # CSS selector for article metadata
        year_text = year_info.text
        year = "".join([s for s in year_text if s.isdigit() and len(s) == 4])
        years.append(year)

    return list(zip(articles, years))  # Combine titles with years

# Replace this URL with the Google Scholar profile URL
scholar_url = "https://scholar.google.ca/citations?user=hfGa2RMAAAAJ&hl=en"
articles_with_years = fetch_google_scholar_articles(scholar_url)

# Print the results
print("Articles published in the past 5 years:")
for title, year in articles_with_years:
    if year and int(year) >= (time.localtime().tm_year - 5):
        print(f"{title} ({year})")

# Close the browser
driver.quit()
