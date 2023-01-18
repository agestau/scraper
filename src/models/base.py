import math
import os
from abc import ABC, abstractmethod
from decimal import DivisionByZero
from typing import Dict, List, Optional, Tuple

import pandas as pd
import requests
from bs4 import BeautifulSoup
from mysql.connector.connection_cext import CMySQLConnection
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from tqdm import tqdm

from src.models.book import Book, BookLink


class BaseScraper(ABC):
    __items_per_page__: int = 0
    __domain__: str = ""

    @abstractmethod
    def _retrieve_items_list(self, pages_count: int, keyword: str) -> List[BookLink]:
        pass

    def _get_page_content(self, query: str) -> Optional[BeautifulSoup]:
        options = Options()
        options.headless = True
        options.add_argument("--window-size=1920,1200")

        s=Service(os.getenv("SELENIUM_PATH"))
        driver = webdriver.Chrome(service=s,options=options)
        driver.get(f"{self.__domain__}/{query}")

        if requests.get(f"{self.__domain__}/{query}").status_code == 200:
            return BeautifulSoup(driver.page_source)
        raise Exception("Cannot reach content!")

    def scrape(self, books_count: int, keyword: str) -> List[Optional[Book]]:
        try:
            pages_count = math.ceil(books_count / self.__items_per_page__)
        except ZeroDivisionError:
            raise AttributeError("Books per page is set to 0!")
        book_links = self._retrieve_items_list(pages_count, keyword)
        scraped_books: List[Optional[Book]] = []
        for book_link in tqdm(book_links):
            scraped_book = self._retrieve_book_info(book_link)
            if scraped_book:
                scraped_books.append(scraped_book)
        return scraped_books



class BaseModel(ABC):
    __table__: Optional[str] = None

    def __init__(self, db_connection: CMySQLConnection) -> None:
        self._db_connection = db_connection
        self._create_table()

    def _create_table(self) -> None:
        query = self._initialization_query()
        cur = self._db_connection.cursor()
        cur.execute(query)

    @abstractmethod
    def _initialization_query(self) -> str:
        pass

    def insert(self, insert_values: Dict) -> None:
        cur = self._db_connection.cursor()
        insert_dimensions = ", ".join(
            [insert_title for insert_title in insert_values.keys()]
        )
        _insert_values = ", ".join(
            [f"'{insert_value}'" for insert_value in insert_values.values()]
        )
        query = f"""INSERT INTO {self.__table__}
            ({insert_dimensions}) values ({_insert_values});"""
        cur.execute(query)
        self._db_connection.commit()

        return None