import os

from mysql import connector

db_connection = connector.connect(
    user=os.environ.get("DB_USER"),
    password=os.environ.get("DB_PASSWORD"),
    database=os.environ.get("DB_DATABASE"),
    port=int(os.environ.get("DB_PORT","3336")),
    host=os.environ.get("DB_HOST")
)
