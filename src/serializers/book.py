from pydantic import BaseModel


class BookSetter(BaseModel):
    title: str
    image_url: str
    about: str
    price: str
    pages: str


class BookGetter(BaseModel):
    id: int
    title: str
    image_url: str
    about: str
    price: str
    pages: str