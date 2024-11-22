# -*- coding: utf-8 -*-
"""
Created on Fri Nov 22 09:20:39 2024

# Thanks to ChatGPT! 
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
from datetime import datetime


import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
from datetime import datetime

def fetch_articles(scholar_url, years=4):
    """
    Fetch articles published in the last `years` years from a Google Scholar profile.
    """
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"}
    response = requests.get(scholar_url, headers=headers)
    if response.status_code != 200:
        print(f"Failed to fetch {scholar_url}")
        return []
    
    soup = BeautifulSoup(response.text, "html.parser")
    articles = []
    current_year = datetime.now().year
    min_year = current_year - years

    for row in soup.select(".gs_r"):
        print('ok')
        title = row.select_one(".gs_rt").text if row.select_one(".gs_rt") else ""
        year_text = row.select_one(".gs_a").text if row.select_one(".gs_a") else ""
        # Extract year from text
        year_match = re.search(r"\b(20\d{2})\b", year_text)
        year = int(year_match.group(1)) if year_match else None
        
        if year and year >= min_year:
            articles.append(title)

    return articles

def find_coauthored_articles(professors):
    """
    Find coauthored articles from a list of professors' Google Scholar URLs.
    """
    all_articles = []

    for name, url in professors.items():
        print(f"Fetching articles for {name}...")
        articles = fetch_articles(url)
        all_articles.extend(articles)
    
    # Count article occurrences
    article_counts = pd.Series(all_articles).value_counts()
    coauthored_articles = article_counts[article_counts > 1]
    
    return coauthored_articles

# List of professors and their Scholar URLs
professors = {
    "Professor 1": "https://scholar.google.ca/citations?user=hfGa2RMAAAAJ&hl=en",
    "Professor 3": "https://scholar.google.com/citations?user=ygu2VxQAAAAJ&hl=en",
    "Professor 4": "https://scholar.google.ca/citations?user=cEepZOEAAAAJ&hl=en",
    "Professor 6": "https://scholar.google.ca/citations?user=G45xgdAAAAAJ&hl=en",
    "Professor 7": "https://scholar.google.com/citations?user=mFSmAqUAAAAJ&hl=en",
    "Professor 8": "https://scholar.google.com/citations?user=WjCG3owAAAAJ&hl=en",
    "Professor 9": "https://scholar.google.com/citations?user=LZyOFQoAAAAJ&hl=en",
    "Professor 10": "https://scholar.google.ca/citations?user=37FDILIAAAAJ&hl=en",
    # Add more professor URLs here
}

coauthored = find_coauthored_articles(professors)
print("\nCoauthored Articles:")
print(coauthored)





scholar_url="https://scholar.google.ca/citations?user=hfGa2RMAAAAJ&hl=en"
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"}
response = requests.get(scholar_url, headers=headers)


















