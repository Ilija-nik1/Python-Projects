import requests
from bs4 import BeautifulSoup
import pandas as pd
import concurrent.futures

def get_website_data(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for 4xx and 5xx status codes
        return url, response.text
    except requests.exceptions.RequestException as e:
        print(f"Failed to fetch the website content for '{url}': {e}")
        return url, None

def extract_data_from_html(url, html_content, table_class=None):
    data = []
    soup = BeautifulSoup(html_content, 'html.parser')

    # Modify this section according to your website's HTML structure to extract relevant data
    if table_class:
        table = soup.find('table', class_=table_class)
    else:
        table = soup.find('table')

    if table:
        rows = table.find_all('tr')
        for row in rows:
            columns = row.find_all(['td', 'th'])  # Consider both table data and table header elements
            row_data = [column.get_text(strip=True) for column in columns]
            if row_data:
                data.append(row_data)

    return url, data

def save_to_excel(data, output_file):
    df = pd.DataFrame(data)
    df.to_excel(output_file, index=False)
    print(f"Data successfully saved to '{output_file}'")

if __name__ == "__main__":
    # URLs to scan
    website_urls = ['https://podrska.callidus.hr/WorkOrder.do?woMode=viewWO&woID=40864#worklogs']
    output_excel_file = 'website_data.xlsx'
    table_class_name = 'data-table'  # Replace this with the class name of the table if applicable

    website_data = []
    with concurrent.futures.ThreadPoolExecutor() as executor:
        # Fetch website data in parallel using multithreading
        future_to_url = {executor.submit(get_website_data, url): url for url in website_urls}
        for future in concurrent.futures.as_completed(future_to_url):
            url = future_to_url[future]
            try:
                website_data.append(future.result())
            except Exception as e:
                print(f"An error occurred while processing '{url}': {e}")

    # Filter out None values (failed requests)
    website_data = [data for data in website_data if data[1] is not None]

    if not website_data:
        print("No data retrieved from any website.")
    else:
        extracted_data = []
        with concurrent.futures.ThreadPoolExecutor() as executor:
            # Extract data from HTML in parallel using multithreading
            future_to_data = {executor.submit(extract_data_from_html, url, html, table_class_name): url for url, html in website_data}
            for future in concurrent.futures.as_completed(future_to_data):
                url = future_to_data[future]
                try:
                    extracted_data.append(future.result())
                except Exception as e:
                    print(f"An error occurred while extracting data from '{url}': {e}")

        # Filter out None values (failed data extraction)
        extracted_data = [data for data in extracted_data if data[1]]

        if extracted_data:
            save_to_excel(extracted_data, output_excel_file)
        else:
            print("No data extracted from any website.")