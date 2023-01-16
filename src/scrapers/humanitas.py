from typing import List, Optional

from bs4 import BeautifulSoup

from src.models.book import Book, BookLink
from src.models.base import BaseScraper


class Humanitas(BaseScraper):
    __items_per_page__: int = 20
    __domain__: str = "https://www.humanitas.lt/"

    def _retrieve_items_list(self, pages_count: int, keyword: str) -> List[BookLink]:
        results: List[BookLink] = []
        keyword = keyword.replace(' ', '-').lower()
        
        for page_num in range(2, pages_count + 2):
            content = self._get_page_content(f"produktai/{keyword}/?cntnt01page={page_num}")
            if content:
                knygu_list_div = content.find("div", class_="page-module")
                if not knygu_list_div:
                    break
                all_knygos_div = knygu_list_div.find_all("div", class_="pure-u-1-2 pure-u-md-1-2 pure-u-lg-1-3 pure-u-xl-1-5")
                for book_div in all_knygos_div:
                    link_to_book = book_div.find("a")["href"]
                    results.append(BookLink(url=link_to_book[25:])) 
            else:
                continue
        return results

    def _retrieve_knygos_info(self, link: BookLink) -> Optional[Book]:
        content = self._get_page_content(link.url)
        if content:
            try:
                book_title = content.find("div", class_="left").find("div", class_="title").text.strip()
            except AttributeError:
                return None

            author = content.find("div", class_="left").find("div", class_="author").text.strip()
            main_image = content.find("div", class_="product-image-background").find("img").get("src")
            about = content.find("div", class_="product-about-container").text.strip().split(' ', 1)[1].strip()
            price = content.find("div", class_="price-container").text.split('€', 1)[0]

            book_info = content.find("div", class_="book-info")
            book_info_str = str(book_info)
            psl_info = book_info_str.split('br')[4]
            try:
                pages = int(''.join(filter(str.isdigit, psl_info)))
            except KeyError:
                pages = None

            main_image = ""

            return Book(
                title=book_title,
                image_url=main_image,
                author=author,
                about=about,
                price=price,
                pages=pages,
            )
        else:
            return None

