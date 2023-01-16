from typing import Optional

from pydantic import BaseModel


class Book(BaseModel):
    title: str
    image_url: Optional[str]
    about: Optional[str]
    price: Optional[str]
    pages: Optional[str]

class BookLink(BaseModel):
    url: str
