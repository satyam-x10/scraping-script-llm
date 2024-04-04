# scraping-script-llm
This is the script for scraping IITBBS website.
The workflow of the repo is as follows:
1. Run `link_scraper_dfs.py` to extract the links from the website.This stores the links to `crawled_urls.csv`.
2. Now run the `scraping script.py` to extract content from the links collected in `cawled_ursl.csv` and save it to `scraped_data_dfs.json`.
3. Run`preprocessed_data.py` to remove unwanted characters from the collected data and store it to `cleaned_json.py`.
   
