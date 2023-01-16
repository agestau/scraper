from typing import Dict
from mysql.connector.connection_cext import CMySQLConnection
from src.models.base import BaseModel


class Book_table(BaseModel):
    __table__: str = "books"

    def __init__(self, db_connection: CMySQLConnection) -> None:
        super().__init__(db_connection)

    def _initialization_query(self) -> str:
        query = """CREATE TABLE IF NOT EXISTS books (
            id int NOT NULL AUTO_INCREMENT,
            title varchar(255) NOT NULL,
            image_url varchar(255) NOT NULL,
            about varchar(2555) NOT NULL,
            price varchar(255) NOT NULL,
            pages varchar(255) NOT NULL,
            PRIMARY KEY(id)
        );"""
        return query
