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


def print_data(csv_filename):
    # Read data from CSV file and print it
    with open(csv_filename, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            print(row)


def count_rows(csv_filename):
    # Count the number of rows in the CSV file
    with open(csv_filename, 'r') as file:
        reader = csv.reader(file)
        row_count = sum(1 for _ in reader)
        return row_count


if __name__ == '__main__':
    # Command line arguments
    parser = argparse.ArgumentParser(description='Web scraper')
    parser.add_argument('url', type=str, help='URL of the page to scrape')
    parser.add_argument('-o', '--output', type=str, default='data.csv', help='Output filename')
    parser.add_argument('-p', '--print', action='store_true', help='Print the data after scraping')
    parser.add_argument('-c', '--count', action='store_true', help='Count the number of rows')
    args = parser.parse_args()

    # Logging configuration
    logging.basicConfig(level=logging.INFO)

    # URL and output filename
    url = args.url
    output_filename = args.output

    # Scrape data
    scrape_data(url, output_filename)

    # Print data if specified
    if args.print:
        print_data(output_filename)

    # Count rows if specified
    if args.count:
        row_count = count_rows(output_filename)
        print(f"Number of rows: {row_count}")