import csv
import argparse
import logging
import requests
from bs4 import BeautifulSoup

def scrape_data(url, output_filename):
    # Start scraping
    logging.info('Scraping data from %s...', url)

    # Get page
    try:
        response = requests.get(url)
        response.raise_for_status()  # Check for HTTP errors
    except requests.RequestException as e:
        logging.error('Failed to retrieve page: %s', e)
        exit(1)

    # Parse HTML
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find table
    table = soup.find('table')

    if not table:
        logging.error('Table not found')
        exit(1)

    # Find rows
    rows = table.find_all('tr')

    if not rows:
        logging.warning('No rows found in table')
        exit(1)

    # Write data to CSV file
    with open(output_filename, 'w', newline='') as file:
        writer = csv.writer(file)

        for row in rows:
            cells = row.find_all(['td', 'th'])

            if not cells:
                logging.warning('No cells found in row: %s', row)
                continue

            csv_row = [cell.get_text().strip() for cell in cells]
            writer.writerow(csv_row)

    logging.info('Data saved to %s', output_filename)


if __name__ == '__main__':
    # Command line arguments
    parser = argparse.ArgumentParser(description='Web scraper')
    parser.add_argument('url', type=str, help='URL of the page to scrape')
    parser.add_argument('-o', '--output', type=str, default='data.csv', help='Output filename')
    args = parser.parse_args()

    # Logging configuration
    logging.basicConfig(level=logging.INFO)

    # URL and output filename
    url = args.url
    output_filename = args.output

    # Scrape data
    scrape_data(url, output_filename)