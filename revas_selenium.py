import sys
import os
from time import sleep
from typing import NoReturn
import threading

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class Revas_Selenium:
    def __init__(self, usr_name: str, passwd: str, game_id: int):
        path = os.getcwd()
        fp = webdriver.FirefoxProfile()
        fp.set_preference('browser.download.folderList', 2)
        fp.set_preference('browser.download.manager.showWhenStarting', False)
        fp.set_preference('browser.download.dir', os.path.join(os.getcwd(), 'temp'))
        fp.set_preference('browser.helperApps.neverAsk.saveToDisk', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        self.driver = webdriver.Firefox(firefox_profile=fp)
        self.driver.maximize_window()

        self.driver.get('https://gry.revas.pl/')

        self.usr_name = usr_name
        self.passwd = passwd
        self.game_id = game_id

    def login(self) -> NoReturn:
        self.driver.find_element_by_id('logEmail').send_keys(self.usr_name)
        self.driver.find_element_by_id('logPassword').send_keys(self.passwd + Keys.RETURN)

        enter_game = WebDriverWait(self.driver, 3).until(
            EC.presence_of_element_located((By.ID, f'join_btn_{self.game_id}')))
        enter_game.click()
        
        url = self.driver.current_url
        
        return url[:url.index('.pl/') + 4]
        
    def get_xlsx(self, url: str, id: int) -> str:
        download_url = f'{url}ajax.php?mod=offer&action=offer-export-to-exel&serviceID={id}&tab=empty&atype=json'
        
        self.driver.set_page_load_timeout(1)
        try:
            self.driver.get(download_url)
        except: # TimedPromise
            sleep(1)
            self.driver.get(url)
            return os.listdir(os.path.join(os.getcwd(), 'temp'))[0]
        
    def get_offer_count(self, url: str) -> int:
        self.driver.get(url + 'offer.php')

        WebDriverWait(self.driver, 3).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'light-well-item')))

        return len(self.driver.find_elements_by_class_name('light-well-item'))

    def quit(self, timeout: float = 0) -> NoReturn:
        sleep(timeout)

        self.driver.quit()
        sys.exit()
