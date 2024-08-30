from selenium import webdriver
from contextlib import contextmanager


@contextmanager
def get_webdriver():
    driver = webdriver.Chrome()
    try:
        yield driver
    finally:
        driver.quit()
