from typing import List, Optional

from bs4 import BeautifulSoup

from src.models.book import Book, BookLink
from src.models.base import BaseScraper


class Knyguklubas(BaseScraper):
    __items_per_page__: int = 32
    __domain__: str = "https://www.knyguklubas.lt"

    def _retrieve_items_list(self, pages_count: int, keyword: str) -> List[BookLink]:
        results: List[BookLink] = []
        keyword = keyword.replace(' ', '%20').lower()
        
        for page_num in range(2, pages_count + 2):
            content = self._get_page_content(f"paieska?sn.q={keyword}&sn.l=32&sn.s=-score&sn.o={(page_num-1)*32}")
            if content:
                knygu_list_div = content.find("div", class_="column main")
                if not knygu_list_div:
                    break
                all_knygos_div = knygu_list_div.find_all("li", class_="item product product-item")
                for book_div in all_knygos_div:
                    link_to_book = book_div.find("a")["href"]
                    results.append(BookLink(url=link_to_book)) 
            else:
                continue
        return results

    def _retrieve_knygos_info(self, link: BookLink) -> Optional[Book]:
        content = self._get_page_content(link.url)
        if content:
            try:
                book_title = content.find("h1", class_="page-title").find("span", class_="base").text
            except AttributeError:
                return None

            author = content.find("div", class_="product-info-main").find("p", class_="product-item-author").text
            main_image = content.find("img", class_="gallery-placeholder__image").get("src")
            about = content.find("div", class_="product-description").find("p").text
            price = content.find("div", class_="price-box price-final_price").find("span", class_="price").text

            additional_info = content.find("div", class_="product-more-details").find("p").text
            keyword = 'Puslapių skaičius:'
            before_keyword, keyword, after_keyword = additional_info.partition(keyword)
            try:
                pages = after_keyword.split(',')[0]
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
