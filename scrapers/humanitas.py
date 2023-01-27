import numpy as np
from typing import List, Dict
from utils.utils import get_content


def extract_page_info(url: str):
    content = get_content(url)
    
    knygu_list_div = content.find("div", class_="page-module")
    if not knygu_list_div:
        None

    books_links: List[Dict] = []
    all_knygos_div = knygu_list_div.find_all("div", class_="pure-u-1-2 pure-u-md-1-2 pure-u-lg-1-3 pure-u-xl-1-5")
    for book_div in all_knygos_div:
        link_to_book = book_div.find("a")["href"]

        books_links.append({
            "link_to_book": link_to_book
        }) 
    return books_links


def booklinks_humanitas(keyword: str, page_count: int):
    keyword = keyword.strip().replace(' ', '+').lower()
    recipes_links: List[Dict] = []

    if page_count==1:
        url = f"https://www.humanitas.lt/produktai/visos-kategorijos/?cntnt01page={page_count}&m575a2title_search={keyword}"
        recipes_links=extract_page_info(url)
    else:
        for page in range(1, page_count+1):
            url2 = f"https://www.humanitas.lt/produktai/visos-kategorijos/?cntnt01page={page}&m575a2title_search={keyword}"
            recipes_links.extend(extract_page_info(url2))
    return recipes_links


def scrape_books_humanitas(keyword: str, page_count: int):
    books_links=booklinks_humanitas(keyword, page_count)
    full_books: List[Dict] = []
    for book_link in books_links:
        content = get_content(book_link["link_to_book"])

        book_title = content.find("h1", class_="title").text.strip()

        try:
            author = content.find("div", class_="left").find("div", class_="author").text.strip()
        except AttributeError:
            author = ""

        main_image = content.find("div", class_="product-image-background").find("img").get("src")

        try:
            about = content.find("div", class_="product-about-container").text.strip().split(' ', 1)[1].strip()
        except AttributeError:
            about = ""
            
        price = content.find("div", class_="price-container").text.split('€', 1)[0].strip()

        book_info = content.find("div", class_="book-info")
        book_info_str = str(book_info)
        psl_info = book_info_str.split('br')[4]
        try:
            pages = float(''.join(filter(str.isdigit, psl_info)))
        except (AttributeError, ValueError):
            pages = float('NaN')

        full_books.append({
            "title": book_title,
            "author": author, 
            "image_url": main_image,
            "about": about,
            "price": price,
            "keyword": keyword
        })
    return full_books