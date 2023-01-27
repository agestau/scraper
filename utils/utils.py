
import time
import pandas as pd
from typing import List, Dict

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from bs4 import BeautifulSoup


def get_content(url: str):
    options = FirefoxOptions()
    options.headless = True
    driver = webdriver.Firefox(options=options)
    driver.get(url)
    time.sleep(2)
    content = BeautifulSoup(driver.page_source)
    driver.quit()
    return content


def get_content_2(url: str, page_count:int):
    options = FirefoxOptions()
    options.headless = True
    driver = webdriver.Firefox(options=options)
    driver.get(url)
    time.sleep(2)

    if page_count>1:
        for i in range(1, page_count): 
            show_more = driver.find_elements(By.XPATH, ("//*[contains(text(), 'Show More')]"))
            show_more[0].click()
            time.sleep(2)
        content = BeautifulSoup(driver.page_source)
        driver.quit()
    else:
        content = BeautifulSoup(driver.page_source)
        driver.quit()
    return content


def save_to_csv(scraped: list, csv_name: str):
    pd.DataFrame(scraped).to_csv(f"{csv_name}.csv")