from page_ranker_app.source.page_ranker import WikiPageRankInfoAccumulator
from page_ranker_app.source import utils, inverters


def main(url: str, limit: int):
    wiki_scrapper = WikiPageRankInfoAccumulator(url, limit)
    with utils.timer():
        wiki_scrapper.scrap_data_till_limit()
    # print(wiki_scrapper._page_links)
    with utils.timer():
        wiki_scrapper.count_page_rank()
        dict1 = wiki_scrapper.page_rank
    # print(wiki_scrapper.page_rank)
    with utils.timer():
        wiki_scrapper.inverter = inverters.DictionaryInverterProcessing
        wiki_scrapper.count_page_rank()
        dict2 = wiki_scrapper.page_rank
    with utils.timer():
        wiki_scrapper.inverter = inverters.DictionaryInverterSync
        wiki_scrapper.count_page_rank()
        dict3 = wiki_scrapper.page_rank
    print(dict1 == dict2 == dict3)


if __name__ == "__main__":
    test_url = "https://en.wikipedia.org/wiki/Superintendent"
    test_limit = 100
    main(test_url, test_limit)
