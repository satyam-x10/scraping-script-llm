import pandas as pd
import requests
from bs4 import BeautifulSoup
import logging
import json
from datetime import datetime
from pathlib import Path
from typing import List, Set

# Use a session for HTTP requests
session = requests.Session()

# Define the CSS selectors for elements to exclude
selectors_to_exclude: List[str] = [
    #"body > div:nth-child(1) > nav",
    #"body > div:nth-child(1) > header > div > div.logo.col-md-3.col-sm-3 > div > div:nth-child(1)",
    "script",  # Exclude script elements
    "style"    # Exclude style elements
]

# Configure logging with timestamp
log_filename: str = f'scraping_logs_{datetime.utcnow().strftime("%Y%m%d_%H%M%S")}.log'
logging.basicConfig(filename=log_filename, level=logging.DEBUG, format='%(asctime)s: %(levelname)s: %(message)s')

def should_continue_scraping(url: str) -> bool:
    # Get the file extension from the URL
    file_extension: str = Path(url).suffix.lower()

    # List of file formats to skip
    skip_formats: tuple = ('.pdf', '.png')

    if file_extension in skip_formats:
        logging.warning("Skipping %s URL: %s", file_extension.upper(), url)
        return False

    return True

def filter_html(soup: BeautifulSoup, selectors_to_exclude: List[str]) -> None:
    # Remove excluded elements
    for selector in selectors_to_exclude:
        elements_to_exclude = soup.select(selector)
        for element in elements_to_exclude:
            element.decompose()

# Function to scrape content from a URL while excluding elements
def scrape_url_content(url: str, output_file: str, count, processed_urls: Set[str]) -> None:
    try:
        # Check if the URL has already been processed
        if url in processed_urls:
            logging.debug("URL Already Processed: %s", url)
            return

        # Check if we want to continue scraping this URL
        if not should_continue_scraping(url):
            return

        response = session.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')

            # Remove excluded elements using the new function
            filter_html(soup, selectors_to_exclude)

            # Extract text content
            all_text = soup.get_text()
            
            # Add the URL and its content to the scraped_data dictionary
            scraped_data[url] = all_text.strip()

            # Add the URL to the set of processed URLs
            processed_urls.add(url)

            logging.info("URL Done: %s - Count: %d", url, count)

        else:
            logging.error("Failed to retrieve data from %s. Status code: %d", url, response.status_code)
    except Exception as e:
        logging.error("An error occurred while processing %s: %s", url, str(e))

# Initialize a dictionary to keep track of URL and its scraped content
scraped_data = {}
# Load the csv file
csv_file = "crawled_urls.csv"
df = pd.read_csv(csv_file)

# Initialize a dictionary to keep track of URL and its scraped content
scraped_data = {}

# Initialize a set to keep track of processed URLs
processed_urls: Set[str] = set()

# Extract URLs from the "Urls" column and iterate through them
count = 0
total_urls = len(df['URL'])
for count, url in enumerate(df['URL']):
    if pd.notna(url):
        count += 1
        print(f"Scraping URL: {url} - Count: {count}/{total_urls}")
        scrape_url_content(url, scraped_data, count, processed_urls)

# Write the scraped data to a JSON file
with open('scraped_data_dfs.json', 'w', encoding='utf-8') as json_file:
    json.dump(scraped_data, json_file, ensure_ascii=False, indent=4)

print("Scraping completed. Data has been saved to scraped_data.json")
