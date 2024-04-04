import json
import re

processed_urls_count = 0

def clean_string(value):
    # Replace BOM, \n, \t, \r, and any non-printable characters with a single space
    value = re.sub(r'[\uFEFF\n\t\r\x00-\x1F\x7F]+', ' ', value)
    # Replace multiple spaces with a single space
    value = re.sub(r' +', ' ', value)
    # Strip leading/trailing spaces
    value = value.strip()
    return value

def clean_data(data):
    global processed_urls_count
    if isinstance(data, dict):
        # Recursive call for dictionaries
        return {key: clean_data(value) for key, value in data.items()}
    elif isinstance(data, list):
        # Recursive call for lists
        return [clean_data(item) for item in data]
    elif isinstance(data, str):
        # Clean the string
        processed_urls_count += 1  # Increment the count of processed URLs
        print(f"Processing URL {processed_urls_count}/{total_urls}")
        return clean_string(data)
    else:
        # Return the data as is if it's not a string, list, or dict
        return data

# Load your JSON data
with open('scraped_data_dfs.json', 'r', encoding='utf-8') as file:
    json_data = json.load(file)

# Total number of URLs
total_urls = len(json_data)

# Clean the data
cleaned_data = clean_data(json_data)

# Save the cleaned data back to a file
with open('cleaned_data.json', 'w', encoding='utf-8') as file:
    json.dump(cleaned_data, file, ensure_ascii=False, indent=4)


