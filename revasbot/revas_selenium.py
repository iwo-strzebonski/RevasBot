import sys
import os
from time import sleep
from typing import NoReturn

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


class RevasSelenium:
    def __init__(self, usr_name: str, passwd: str, game_id: int) -> None:
        self.id_name = {
            'offer': 'serviceID',
            'suppliers': 'partSupplierID'
        }
        
        ff_prof = webdriver.FirefoxProfile()

        ff_prof.set_preference(
            'browser.download.folderList',
            2
        )
        ff_prof.set_preference(
            'browser.download.manager.showWhenStarting',
            False
        )
        ff_prof.set_preference(
            'browser.download.dir',
            os.path.join(os.getcwd(), 'temp')
        )
        ff_prof.set_preference(
            'browser.helperApps.neverAsk.saveToDisk',
            'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )

        self.driver = webdriver.Firefox(firefox_profile=ff_prof)
        self.driver.maximize_window()

        self.driver.get('https://gry.revas.pl/')

        self.usr_name = usr_name
        self.passwd = passwd
        self.game_id = game_id
        
        self.url = ''

    def login(self) -> str:
        self.driver.find_element_by_id('logEmail').send_keys(self.usr_name)
        self.driver.find_element_by_id(
            'logPassword').send_keys(self.passwd + Keys.RETURN)

        enter_game = WebDriverWait(self.driver, 3).until(
            EC.presence_of_element_located((By.ID, f'join_btn_{self.game_id}')))
        enter_game.click()

        url = self.driver.current_url
        self.url = url[:url.index('.pl/') + 4]

        return self.url

    def get_xlsx(self, item_id: int, mod: str) -> str:
        download_url = \
            self.url + \
            f'ajax.php?mod={mod}&action={mod}-export-to-exel&{self.id_name[mod]}=' + \
            str(item_id) + \
            '&tab=empty&atype=json'

        self.driver.set_page_load_timeout(2)

        try:
            self.driver.get(download_url)
        except TimeoutException:
            # sleep(2)
            self.driver.get(self.url)
            return os.listdir(os.path.join(os.getcwd(), 'temp'))[0]

        return ''

    def get_data_count(self, mod: str) -> int:
        self.driver.get(self.url + mod + '.php')

        WebDriverWait(self.driver, 1).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'light-well-item')))

        return len(self.driver.find_elements_by_class_name('light-well-item'))

    def scrap_xlsxs(self):
        for key in self.id_name:
            item_id = 0
            i = 0
            count = self.get_data_count(key)
            count = count if count else 6

            while i < count:
                spreadsheet = self.get_xlsx(item_id, key)

                if 'NOT_FOUND' not in spreadsheet:
                    os.rename(
                        os.path.join(os.getcwd(), 'temp', spreadsheet),
                        os.path.join(os.getcwd(), 'download', key, spreadsheet)
                    )
                    print(f'{item_id}: {spreadsheet}')
                    i += 1
                else:
                    os.remove(os.path.join(os.getcwd(), 'temp', spreadsheet))

                item_id += 1

    def quit(self, timeout: float = 0) -> NoReturn:
        sleep(timeout)

        self.driver.quit()
        sys.exit()
