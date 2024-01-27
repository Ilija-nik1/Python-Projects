import json
import asyncio
import aiohttp
from bs4 import BeautifulSoup

class Article:
    def __init__(self, source, title, link):
        self.source = source
        self.title = title
        self.link = link

class Aggregator:
    def __init__(self):
        self.articles_by_source = {}

    def add_article(self, source, title, link):
        if source not in self.articles_by_source:
            self.articles_by_source[source] = []
        self.articles_by_source[source].append(Article(source, title, link))

    def get_articles_by_source(self, source):
        return self.articles_by_source.get(source, [])

    def get_articles_by_keyword(self, keyword):
        keyword = keyword.lower()
        return [article for articles in self.articles_by_source.values() for article in articles if keyword in article.title.lower()]

    def get_all_sources(self):
        return list(self.articles_by_source.keys())

    def clear_articles(self):
        self.articles_by_source.clear()

    def count_articles(self):
        return sum(len(articles) for articles in self.articles_by_source.values())

    def export_to_file(self, filename):
        with open(filename, 'w') as file:
            for articles in self.articles_by_source.values():
                for article in articles:
                    file.write(f"Source: {article.source}\n")
                    file.write(f"Title: {article.title}\n")
                    file.write(f"Link: {article.link}\n\n")

    def import_from_file(self, filename):
        self.articles_by_source.clear()
        with open(filename, 'r') as file:
            article_data = file.read().split('\n\n')

        for data in article_data:
            lines = data.strip().split('\n')
            if len(lines) >= 3:
                source = lines[0].replace('Source: ', '')
                title = lines[1].replace('Title: ', '')
                link = lines[2].replace('Link: ', '')
                self.add_article(source, title, link)

class Source:
    def __init__(self, url, parse_config):
        self.url = url
        self.parse_config = parse_config

    async def fetch_data(self, aggregator):
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(self.url, timeout=10) as response:
                    response.raise_for_status()
                    content = await response.text()
                    soup = BeautifulSoup(content, 'html.parser')
                    articles = soup.select(self.parse_config['article_selector'])

                    for article in articles:
                        title = article.select_one(self.parse_config['title_selector']).text.strip()
                        link = article.select_one(self.parse_config['link_selector'])['href']
                        aggregator.add_article(self.url, title, link)

            except Exception as e:
                print(f"Error fetching data from source '{self.url}': {e}")

async def fetch_all_data(sources, aggregator):
    tasks = [source.fetch_data(aggregator) for source in sources]
    await asyncio.gather(*tasks)

async def main():
    # Create an instance of the aggregator
    aggregator = Aggregator()

    # Load sources from a configuration file
    with open('sources.json') as file:
        sources_data = json.load(file)

    sources = [Source(source_info['url'], source_info['parse_config']) for source_info in sources_data['sources']]

    # Fetch data from each source and add it to the aggregator
    await fetch_all_data(sources, aggregator)

    # Display the aggregated content
    print("Aggregated Content:")
    # Call display_content if needed

    # Get articles by source
    source_articles = aggregator.get_articles_by_source('https://news.source1.com')
    print(f"\nArticles from source 'https://news.source1.com':")
    for article in source_articles:
        print(article.title)

    # Get articles by keyword
    keyword_articles = aggregator.get_articles_by_keyword('Python')
    print(f"\nArticles containing the keyword 'Python':")
    for article in keyword_articles:
        print(article.title)

    # Get all sources
    sources = aggregator.get_all_sources()
    print("\nAvailable sources:")
    for source in sources:
        print(source)

    # Clear the articles
    aggregator.clear_articles()
    print(f"\nTotal articles after clearing: {aggregator.count_articles()}")

    # Export articles to a file
    aggregator.export_to_file('aggregated_articles.txt')
    print("\nArticles exported to 'aggregated_articles.txt'")

    # Import articles from a file
    aggregator.import_from_file('aggregated_articles.txt')
    print(f"\nTotal articles after importing: {aggregator.count_articles()}")

if __name__ == "__main__":
    asyncio.run(main())