import pandas as pd
from utils.utils import save_to_csv
from scrapers.bookshop import scrape_books_bookshop
from scrapers.humanitas import scrape_books_humanitas


def bookshop_scraper(keyword: str, page_count: int):
    result=scrape_books_bookshop(keyword,page_count)
    return save_to_csv(result,keyword)

def humanitas_scraper(keyword: str, page_count: int):
    result=scrape_books_humanitas(keyword,page_count)
    return save_to_csv(result,keyword)