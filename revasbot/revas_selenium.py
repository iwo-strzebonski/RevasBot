import sys
import os
from time import sleep

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

class RevasSelenium:
    def __init__(self, usr_name: str, passwd: str, game_id: str) -> None:
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

    def login(self) -> None:
        self.driver.find_element_by_id('logEmail').send_keys(self.usr_name)
        self.driver.find_element_by_id(
            'logPassword').send_keys(self.passwd + Keys.RETURN)

        enter_game = WebDriverWait(self.driver, 3).until(
            EC.presence_of_element_located((By.ID, f'join_btn_{self.game_id}')))
        enter_game.click()

        url = self.driver.current_url
        self.url = url[:url.index('.pl/') + 4]

    def get_data_count(self, mod: str) -> int:
        self.driver.get(self.url + mod + '.php')

        try:
            WebDriverWait(self.driver, 3).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'light-well-item')))

            count = len(self.driver.find_elements_by_class_name('light-well-item'))
        except TimeoutException:
            count = 6
        # else:
        #    count = count if count else 6

        return count

    def get_xlsx(self, id_name: str, item_id: int, mod: str, tab: str='empty') -> str:
        action = mod.replace('_', '-')

        download_url = \
            self.url + \
            f'ajax.php?mod={mod}&action={action}-export-to-exel&{id_name}=' + \
            f'{str(item_id)}&tab={tab}&atype=json'

        self.driver.set_page_load_timeout(2)

        try:
            self.driver.get(download_url)
        except TimeoutException:
            return os.listdir(os.path.join(os.getcwd(), 'temp'))[0]

        return ''

    def quit(self, timeout: float=0) -> None:
        sleep(timeout)

        self.driver.quit()
        sys.exit()
