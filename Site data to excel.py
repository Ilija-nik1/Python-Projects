import requests
from bs4 import BeautifulSoup
import pandas as pd
import concurrent.futures
import logging
import time

# Setting up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_website_data(url, user_agent, retries=3, timeout=10):
    try_count = 0
    while try_count < retries:
        try:
            headers = {'User-Agent': user_agent}
            response = requests.get(url, headers=headers, timeout=timeout)
            response.raise_for_status()
            return url, response.text
        except requests.exceptions.RequestException as e:
            logging.error(f"Attempt {try_count + 1} failed for '{url}': {e}")
            try_count += 1
            time.sleep(1)  # Backoff before retrying
    return url, None

def extract_data_from_html(url, html_content, table_class=None):
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
    return url, headers, data

def save_to_file(data, output_file, file_format='csv'):
    if not data:
        logging.warning("No data to save.")
        return

    headers = data[0][1]
    combined_data = [row for _, _, rows in data for row in rows]

    df = pd.DataFrame(combined_data, columns=headers)
    if file_format == 'csv':
        df.to_csv(output_file, index=False)
    else:
        df.to_excel(output_file, index=False)
    logging.info(f"Data successfully saved to '{output_file}'")

if __name__ == "__main__":
    website_urls = ['https://example.com']
    output_file = 'website_data.csv'
    table_class_name = 'data-table'
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'

    with concurrent.futures.ThreadPoolExecutor() as executor:
        future_to_url = {executor.submit(get_website_data, url, user_agent): url for url in website_urls}
        website_data = [future.result() for future in concurrent.futures.as_completed(future_to_url)]

    website_data = [data for data in website_data if data[1]]

    if website_data:
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future_to_data = {executor.submit(extract_data_from_html, url, html, table_class_name): url for url, html in website_data}
            extracted_data = [future.result() for future in concurrent.futures.as_completed(future_to_data)]

        save_to_file(extracted_data, output_file)