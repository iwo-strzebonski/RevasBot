import sys
import os
from time import sleep
import time
from typing import Tuple

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

from msedge.selenium_tools import Edge, EdgeOptions
# from selenium.webdriver import 
# from selenium.webdriver.chrome.options import Options

class RevasSelenium:
    def __init__(self, usr_name: str, passwd: str, game_id: str) -> None:
        options = EdgeOptions()
        options.use_chromium = True
        # options.headless = True

        self.driver = Edge(options=options)
        self.driver.maximize_window()

        self.driver.get('https://gry.revas.pl/')

        self.usr_name = usr_name
        self.passwd = passwd
        self.game_id = game_id

        self.url = ''
        self.game_name = ''
        self.download_path = os.path.expanduser('~/Downloads')

    def login(self) -> None:
        self.driver.find_element_by_id('logEmail').send_keys(self.usr_name)
        self.driver.find_element_by_id(
            'logPassword').send_keys(self.passwd + Keys.RETURN)

        enter_game = WebDriverWait(self.driver, 3).until(
            EC.presence_of_element_located((By.ID, f'join_btn_{self.game_id}')))
        enter_game.click()

        WebDriverWait(self.driver, 1).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'game_url'))
        )

        url = self.driver.current_url

        self.url = url[:url.index('.pl/') + 4]
        self.game_name = url[8 : url.index('.')]

    def get_data_count(self, mod: str) -> int:
        self.driver.get(self.url + mod + '.php')

        try:
            WebDriverWait(self.driver, 3).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'light-well-item')))

            count = len(self.driver.find_elements_by_class_name('light-well-item'))
        except TimeoutException:
            count = 6

        return count

    def get_xlsx(self, item_data: Tuple[str, str, str, str]) -> str:
        id_name, item_id, mod, action = item_data

        download_url = \
            self.url + \
            f'ajax.php?mod={mod}&action={action}-export-to-exel&{id_name}=' + \
            f'{item_id}&tab=empty&atype=json'

        self.driver.set_page_load_timeout(1)

        self.driver.get(download_url)

        time.sleep(0.5)

        for down_file in os.listdir(os.path.join(self.download_path)):
            if (
                'Dostawca' in down_file or
                'Wymagania dotyczące usługi' in down_file or
                'Lista pracowników dostępnych na rynku pracy' in down_file or
                'Historia rachunku' in down_file
            ):
                return down_file

        return ''

    def quit(self, timeout: float=0) -> None:
        sleep(timeout)

        self.driver.quit()
        sys.exit()
