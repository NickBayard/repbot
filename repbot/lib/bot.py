from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class RepBot:

    def __init__(self, session):
        self.session = session
        self.driver = webdriver.Chrome()

    def run(self):
        pass
