import sys
from time import sleep
from typing import NoReturn

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class RevasSelenium:
    def __init__(self, usr_name: str, passwd: str, game_id: int):
        self.browser = webdriver.Firefox()
        self.browser.get('https://gry.revas.pl/')

        self.usr_name = usr_name
        self.passwd = passwd
        self.game_id = game_id

    def login(self) -> NoReturn:
        self.browser.find_element_by_id('logEmail').send_keys(self.usr_name)
        self.browser.find_element_by_id('logPassword').send_keys(self.passwd + Keys.RETURN)

        enter_game = WebDriverWait(self.browser, 1).until(
            EC.presence_of_element_located((By.ID, f'join_btn_{self.game_id}')))
        enter_game.click()

    def quit(self, timeout: float = 0) -> NoReturn:
        sleep(timeout)

        self.browser.quit()
        sys.exit()
