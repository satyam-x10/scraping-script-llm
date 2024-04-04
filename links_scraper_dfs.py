import requests
from bs4 import BeautifulSoup
import csv
import time
from urllib.parse import urlparse, urljoin
import logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    handlers=[logging.FileHandler('link_scraper_dfs.log', 'w', 'utf-8'),])
def is_document_url(url):
    """Check if the URL points to a document based on its file extension."""
    doc_extensions = ('.pdf', '.doc', '.docx', '.ppt', '.pptx', '.xls', '.xlsx','.png','.jpg','.mp4','.jpeg')
    parsed_url = urlparse(url)
    return parsed_url.path.lower().endswith(doc_extensions)

def get_absolute_url(base, link):
    """Convert relative URL to absolute URL using urljoin."""
    return urljoin(f"{base.scheme}://{base.netloc}", link)

def crawl_website(start_url):
    visited = set()  # Keep track of visited URLs
    queue = [start_url]  # Use a list as a queue for DFS
    base_url = urlparse(start_url)
    url_count = 0

    while queue:
        if url_count>10:
            break
        current_url = queue.pop(0)  # Get the first URL from the queue
        if current_url in visited or is_document_url(current_url):
            continue
        url_count+=1
        print(f"Crawling: {current_url}- Count: {url_count}")
        logging.info(f"Crawling: {current_url} - Count: {url_count}")
        visited.add(current_url)  # Mark this URL as visited

        # Delay between requests to not overwhelm the server
        time.sleep(0.4)

        try:
            response = requests.get(current_url)
            soup = BeautifulSoup(response.content, 'html.parser')

            for link in soup.find_all('a', href=True):
                href = link.get('href')
                if not href.startswith(('javascript:', '#', 'mailto:')):
                    absolute_url = get_absolute_url(base_url, href)
                    if absolute_url not in visited and base_url.netloc in absolute_url:
                        queue.append(absolute_url)

        except requests.RequestException as e:
            print(f"Failed to fetch {current_url}: {e}")
            logging.error(f"Failed to fetch {current_url}: {e}")

    return visited

# Start URL for crawling
start_url = "https://www.iitbbs.ac.in/"

# Crawl the website starting from the given URL
crawled_urls = crawl_website(start_url)

# Write the crawled URLs to a CSV file
with open('crawled_urls.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['URL'])
    for url in crawled_urls:
        writer.writerow([url])

print(f"Crawling completed. Found {len(crawled_urls)} unique URLs.")
