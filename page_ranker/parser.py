from bs4 import BeautifulSoup
from crawler import Crawler


class WikiParser:

    def parse(self, website_content: str):
        _soup = BeautifulSoup(website_content, "html.parser")
        internal_url_links = []

        for link in _soup.find_all('a', href=True):
            if link.get('href').startswith('/wiki/') and ':' not in link.get('href'):
                internal_url_links.append(link['href'])

        return internal_url_links


if __name__ == '__main__':
    website = 'https://en.wikipedia.org/wiki/California_Distinguished_School'
    crawler = Crawler()
    parser = WikiParser()
    print(parser.parse(crawler(website)))

