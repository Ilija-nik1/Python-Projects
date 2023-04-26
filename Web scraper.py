import requests
from bs4 import BeautifulSoup
import csv
import argparse
import logging

# Command line arguments
parser = argparse.ArgumentParser(description='Web scraper')
parser.add_argument('url', type=str, help='URL of the page to scrape')
parser.add_argument('-o', '--output', type=str, default='data.csv', help='Output filename')
args = parser.parse_args()

# URL and output filename
url = args.url
output_filename = args.output

# Logging configuration
logging.basicConfig(level=logging.INFO)

# Start scraping
logging.info('Scraping data from %s...', url)

# Get page
response = requests.get(url)

# Check for errors
if response.status_code != 200:
    print('Failed to load page:', response.status_code)
    exit()

# Parse HTML
soup = BeautifulSoup(response.text, 'html.parser')

# Find table
table = soup.find('table')

if not table:
    print('Table not found')
    exit()

# Find rows
rows = table.findAll('tr')

if not rows:
    print('No rows found in table')
    exit()

# Write data to CSV file
with open(output_filename, 'w', newline='') as file:
    writer = csv.writer(file)

    for row in rows:
        csv_row = []

        # Find cells
        cells = row.findAll(['td', 'th'])

        if not cells:
            print('No cells found in row:', row)
            continue

        # Add cell data to CSV row
        for cell in cells:
            csv_row.append(cell.get_text().strip())

        writer.writerow(csv_row)

print('Data saved to', output_filename)