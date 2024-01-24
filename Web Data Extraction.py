import requests
from bs4 import BeautifulSoup
import pandas as pd
import concurrent.futures
import logging
import time
import json

# Setting up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class DataFetcher:
    def __init__(self, user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64)'):
        self.user_agent = user_agent

    def fetch_website_data(self, url, retries=3, timeout=10):
        try_count = 0
        while try_count < retries:
            try:
                headers = {'User-Agent': self.user_agent}
                response = requests.get(url, headers=headers, timeout=timeout)
                response.raise_for_status()
                return response.text
            except requests.exceptions.RequestException as e:
                logging.error(f"Attempt {try_count + 1} failed for '{url}': {e}")
                try_count += 1
                time.sleep(1)  # Backoff before retrying
        return None

    def fetch_api_data(self, url):
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.json()
        except (requests.exceptions.RequestException, ValueError) as e:
            logging.error(f"Error while fetching data from API: {e}")
        return None

class DataExtractor:
    @staticmethod
    def extract_table_data(html_content, table_class=None):
        data, headers = [], []
        soup = BeautifulSoup(html_content, 'html.parser')
        table = soup.find('table', class_=table_class) if table_class else soup.find('table')
        if table:
            rows = table.find_all('tr')
            for row in rows:
                columns = row.find_all(['td', 'th'])
                row_data = [column.get_text(strip=True) for column in columns]
                if row_data:
                    if not headers:
                        headers = row_data
                    else:
                        data.append(row_data)
        return headers, data

class DataSaver:
    @staticmethod
    def save_to_file(data, output_file):
        if not data:
            logging.warning("No data to save.")
            return

        if output_file.endswith('.json'):
            with open(output_file, 'w') as json_file:
                json.dump(data, json_file, indent=4)
        else:
            headers, combined_data = data
            df = pd.DataFrame(combined_data, columns=headers)
            if output_file.endswith('.csv'):
                df.to_csv(output_file, index=False)
            else:
                df.to_excel(output_file, index=False)
        logging.info(f"Data successfully saved to '{output_file}'")

def main():
    data_fetcher = DataFetcher()
    data_extractor = DataExtractor()
    data_saver = DataSaver()

    website_data_config = [
        {
            "url": 'https://example.com',
            "output_file": 'website_data_1.csv',
            "table_class_name": 'data-table',
        },
        {
            "url": 'https://example2.com',
            "output_file": 'website_data_2.csv',
            "table_class_name": 'data-table',
        },
        # Add more website data configurations as needed
    ]

    api_data_config = [
        {
            "url": 'https://jsonplaceholder.typicode.com/posts/1',
            "output_file": 'api_data_1.json',
        },
        {
            "url": 'https://jsonplaceholder.typicode.com/posts/2',
            "output_file": 'api_data_2.json',
        },
        # Add more API data configurations as needed
    ]

    with concurrent.futures.ThreadPoolExecutor() as executor:
        website_futures = {executor.submit(data_fetcher.fetch_website_data, config["url"]): config for config in website_data_config}
        api_futures = {executor.submit(data_fetcher.fetch_api_data, config["url"]): config for config in api_data_config}

    website_data = [(html, config) for html, config in zip(concurrent.futures.as_completed(website_futures), website_data_config) if html]
    api_data = [(data, config["output_file"]) for data, config in zip(concurrent.futures.as_completed(api_futures), api_data_config) if data]

    with concurrent.futures.ThreadPoolExecutor() as executor:
        website_extracted_data = {executor.submit(data_extractor.extract_table_data, html, config["table_class_name"]): config for html, config in website_data}
        api_extracted_data = {executor.submit(data_extractor.extract_api_data, data): output_file for data, output_file in api_data}

    extracted_data = [(data, config["output_file"]) for data, config in zip(concurrent.futures.as_completed(website_extracted_data), website_data_config)]
    extracted_data.extend([(data, output_file) for data, output_file in zip(concurrent.futures.as_completed(api_extracted_data), [config["output_file"] for config in api_data_config])])

    for data, output_file in extracted_data:
        data_saver.save_to_file(data, output_file)

if __name__ == "__main__":
    main()