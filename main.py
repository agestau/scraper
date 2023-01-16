from typing import Dict, List

from src.scrapers import SCRAPERS
from src.models.base import BaseScraper


from fastapi import FastAPI, HTTPException

from src.db.connection import db_connection
from src.models.sql import Book_table
from src.serializers.book import BookGetter, BookSetter

app = FastAPI()

book_module = Book_table(db_connection)


class Book_Scraper:
    def _parse_scrapers(self, scrapers: list[str]) -> List:
        return [SCRAPERS[scraper]() for scraper in scrapers]

    def scrape(
        self, books_per_scraper_count: int, keyword: str, scrapers: List[str]
    ) -> List[Dict]:
        parsed_scrapers: List[BaseScraper] = self._parse_scrapers(scrapers)
        results: List[Dict] = []

        for scraper in parsed_scrapers:
            print(f"Scraping with {scraper.__class__.__name__,} scraper...")
            results.append(
                {
                    "scraper": scraper.__class__.__name__,
                    "items": scraper.scrape(books_per_scraper_count, keyword),
                }
            )

        return results




