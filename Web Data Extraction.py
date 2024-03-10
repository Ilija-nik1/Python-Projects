import requests
from bs4 import BeautifulSoup
import pandas as pd
import concurrent.futures
import logging
import time
import json
from typing import Optional, Tuple, List, Dict, Any

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class DataFetcher:
    def __init__(self, user_agent: str = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)') -> None:
        self.session = requests.Session()
        self.session.headers.update({'User-Agent': user_agent})

    def fetch_website_data(self, url: str, retries: int = 3, timeout: int = 10) -> Optional[str]:
        for try_count in range(retries):
            try:
                response = self.session.get(url, timeout=timeout)
                response.raise_for_status()
                return response.text
            except requests.exceptions.RequestException as e:
                logging.error(f"Attempt {try_count + 1} failed for '{url}': {e}")
                time.sleep(1)  # Exponential backoff can be considered here
        return None

    def fetch_api_data(self, url: str) -> Optional[Dict]:
        try:
            response = self.session.get(url)
            response.raise_for_status()
            return response.json()
        except (requests.exceptions.RequestException, ValueError) as e:
            logging.error(f"Error fetching data from API: {e}")
        return None

class DataExtractor:
    @staticmethod
    def extract_table_data(html_content: str, table_class: Optional[str] = None) -> Tuple[List[str], List[List[str]]]:
        soup = BeautifulSoup(html_content, 'html.parser')
        table = soup.find('table', class_=table_class) if table_class else soup.find('table')
        headers, data = [], []
        if table:
            headers = [th.get_text(strip=True) for th in table.find_all('th')]
            data = [[td.get_text(strip=True) for td in tr.find_all('td')] for tr in table.find_all('tr')[1:]]  # Skip header row
        return headers, data

class DataSaver:
    @staticmethod
    def save_to_file(data: Any, output_file: str) -> None:
        if not data:
            logging.warning("No data to save.")
            return

        if output_file.endswith('.json'):
            with open(output_file, 'w') as json_file:
                json.dump(data, json_file, indent=4)
        elif output_file.endswith('.csv') or output_file.endswith('.xlsx'):
            headers, rows = data
            df = pd.DataFrame(rows, columns=headers)
            if output_file.endswith('.csv'):
                df.to_csv(output_file, index=False)
            else:
                df.to_excel(output_file, index=False)
        logging.info(f"Data successfully saved to '{output_file}'")

def main() -> None:
    data_fetcher = DataFetcher()
    data_extractor = DataExtractor()
    data_saver = DataSaver()

    website_data_config = [
        {"url": 'https://example.com', "output_file": 'website_data_1.csv', "table_class_name": 'data-table'},
        {"url": 'https://example2.com', "output_file": 'website_data_2.csv', "table_class_name": 'data-table'},
    ]

    api_data_config = [
        {"url": 'https://jsonplaceholder.typicode.com/posts/1', "output_file": 'api_data_1.json'},
        {"url": 'https://jsonplaceholder.typicode.com/posts/2', "output_file": 'api_data_2.json'},
    ]

    def process_website_data(config: Dict[str, str]) -> Tuple[List[str], List[List[str]], str]:
        html = data_fetcher.fetch_website_data(config["url"])
        if html:
            return (*data_extractor.extract_table_data(html, config.get("table_class_name")), config["output_file"])
        return ([], [], config["output_file"])

    def process_api_data(config: Dict[str, str]) -> Tuple[Dict, str]:
        data = data_fetcher.fetch_api_data(config["url"])
        return (data, config["output_file"])

    with concurrent.futures.ThreadPoolExecutor() as executor:
        website_data_futures = [executor.submit(process_website_data, config) for config in website_data_config]
        api_data_futures = [executor.submit(process_api_data, config) for config in api_data_config]

        for future in concurrent.futures.as_completed(website_data_futures + api_data_futures):
            data_saver.save_to_file(*future.result())

if __name__ == "__main__":
    main()