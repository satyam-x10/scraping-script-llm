import requests
from bs4 import BeautifulSoup
import pandas as pd

# Function to check if a URL is part of the target domain
def is_target_domain(url, domain='iitbbs.ac.in'):
    return domain in url

# Function to check if a URL points to a downloadable file
def is_downloadable(url):
    try:
        h = requests.head(url, allow_redirects=True, timeout=5)
        header = h.headers
        content_type = header.get('content-type', '')
        if 'pdf' in content_type.lower() or 'image' in content_type.lower() or 'document' in content_type.lower():
            return True
    except requests.RequestException:
        return None  # Indicates a connection error
    return False

# Function to scrape content from a URL
def scrape_content(url):
    if not is_target_domain(url) or 'mailto:' in url:
        return "Skipped: Non-target domain or email URL"
    
    if is_downloadable(url):
        return "Skipped: Downloadable content"

    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 404:
            return "Skipped: 404 error"

        soup = BeautifulSoup(response.content, 'html.parser')

        # Remove script, style, and other non-essential elements
        for script_or_style in soup(['script', 'style', 'header', 'footer', 'nav', 'form']):
            script_or_style.decompose()
        
        texts = soup.stripped_strings
        return " ".join(texts)
    except requests.RequestException:
        return "Connection Error"

# Load the CSV file
file_path = 'crawled_urls.csv'  # Update this with the path to your CSV file
urls_df = pd.read_csv(file_path)

# Open text files for writing the results
with open('scraped_content_bfs.txt', 'w', encoding='utf-8') as scraped_file, open('skipped_urls.txt', 'w', encoding='utf-8') as skipped_file:
    for index, row in urls_df.iterrows():
        content = scrape_content(row['URL'])
        if "Skipped:" in content or "Connection Error" in content:
            skipped_file.write(f"URL: {row['URL']}\nContent: {content}\n\n")
        else:
            scraped_file.write(f"URL: {row['URL']}\nContent: {content}\n\n")
