from page_ranker_app.source.page_ranker import WikiPageRankInfoAccumulator
from page_ranker_app.source import utils


def main(url: str, limit: int):
    wiki_scraper = WikiPageRankInfoAccumulator(url, limit)
    wiki_scraper.scrap_data_till_limit()
    wiki_scraper.count_page_rank()

    distribution = utils.count_distribution(wiki_scraper.page_rank)
    utils.print_hist_and_plot_combined(distribution)


if __name__ == "__main__":
    test_url = "https://en.wikipedia.org/wiki/Superintendent"
    test_limit = 100
    main(test_url, test_limit)
