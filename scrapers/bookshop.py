from typing import List, Dict
from utils.utils import get_content, get_content_2


def booklinks_bookshop(keyword: str, page_count: int):
    keyword = keyword.strip().replace(' ', '+').lower()
    content=get_content_2(f"https://bookshop.org/search?keywords={keyword}", page_count)
        
    knygu_list_div = content.find("div", class_="columns is-multiline")

    if not knygu_list_div:
        print('No content')  
           
    books_links: List[Dict] = []
    all_knygos_div = knygu_list_div.find_all("div", class_="column is-one-fifth")
    for book_div in all_knygos_div:
        title = book_div.find("a", class_="has-text-dark").text.strip()
        link_to_book ='https://bookshop.org' + book_div.find("a")["href"]
        books_links.append({
            "title": title, 
            "link_to_book": link_to_book
        })
    return books_links


def scrape_books_bookshop(keyword: str, page_count: int):
    books_links=booklinks_bookshop(keyword, page_count)
    full_books: List[Dict] = []
    for book_link in books_links:
        content = get_content(book_link["link_to_book"])

        try:
            book_title = content.find("h1", class_="h1 leading-tight mb-2").text
        except AttributeError:
            book_title = ""
    
        try:
            about = content.find("div", class_="mb-8 title-description show-links").text
        except AttributeError:
            about = ""

        try:
            categories = content.find("div", class_="flex flex-wrap items-center").text.strip()
        except AttributeError:
            categories = ""

        full_books.append({
            "title": book_title, 
            "about": about,
            "categories": categories,
            "keyword": keyword,
        })
    return full_books
