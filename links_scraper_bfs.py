import requests
from bs4 import BeautifulSoup
from requests.exceptions import MissingSchema, ConnectTimeout,RequestException
import csv
import logging
import time

# Configure logging
logging.basicConfig(filename='web_crawler.log', level=logging.DEBUG, 
                    format='%(asctime)s:%(levelname)s:%(message)s')

def complete_url(href, base_url):
    """Completes a URL if it is relative."""
    if href.startswith('http'):
        return href
    return base_url.rstrip('/') + '/' + href.lstrip('/')

def get_urls_from_page(url, base_url, visited_urls):
    """Extracts and returns URLs from a webpage."""
    new_urls = {}
    try:
        response = requests.get(url, timeout=500)
        logging.debug(f'Processing url {url}, status code: {response.status_code}')
        time.sleep(0.4)  # Sleep to avoid overwhelming the server
        soup = BeautifulSoup(response.text, 'html.parser')
    except (ConnectTimeout, MissingSchema, RequestException) as e:
        logging.error(f'Exception found while processing {url}: {e}')
        return new_urls

    for link in soup.find_all('a'):
        href = link.get('href')
        anchor_text = link.get_text(strip=True)
        if href:  # Check if href is not None
            anchor_text = link.get_text(strip=True)
            if href.startswith(base_url) and not href.startswith(('javascript', '#')) and not href.lower().endswith(('.mp4','.pdf','.png','.jpg','.jpeg','.docx')):
                complete_href = complete_url(href, base_url)
                if complete_href not in visited_urls:
                    new_urls[complete_href] = anchor_text
    logging.debug(f'New URLs found: {len(new_urls)}')
    return new_urls

base_url = 'https://www.iitbbs.ac.in'
visited_urls = set()
temp_urls = [base_url]

try:
    initial_req = requests.get(base_url)
    time.sleep(0.4)
    initial_soup = BeautifulSoup(initial_req.text, 'html.parser')
except RequestException as e:
    logging.error(f"Error while fetching the base URL: {e}")
    exit()

for i in range(100):
    logging.info(f'Processing iteration {i}')
    print("Running iteration", i)
    urls_iteration = []
    for url in temp_urls:
        t_urls = get_urls_from_page(url, base_url, visited_urls)
        urls_iteration.extend(t_urls.keys())  # Accumulate URLs from this iteration
    if not urls_iteration:
        logging.info(f'Breaking at iteration {i}')
        break
    temp_urls.extend(urls_iteration)  # Add URLs from this iteration to temp_urls
    visited_urls.update(urls_iteration)  # Update visited_urls with new URLs
    print(len(visited_urls))
# Saving the URLs to a CSV file
with open('all_urls.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    for url, text in visited_urls.items():
        writer.writerow([url, text])