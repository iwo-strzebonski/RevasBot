import sys
import os
from time import sleep
from typing import Any

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC

from selenium.common.exceptions import TimeoutException

# from revasbot.revas_console import RevasConsole as console
from revasbot.revas_core import RevasCore
from revasbot.revas_pandas import RevasPandas
from revasbot.revas_cache import RevasCache
from revasbot.selenium.revas_drivers import select_driver

class RevasSelenium:
    usr_name = ''
    passwd = ''
    url = ''
    game_name = ''
    game_id = ''
    company_name = ''
    round_no = 0

    def __init__(self, usr_name: str, passwd: str) -> None:
        self.driver = select_driver()

        self.usr_name = usr_name
        self.passwd = passwd

    def login(self) -> None:
        self.driver.find_element(By.ID, 'logEmail').send_keys(self.usr_name)
        self.driver.find_element(
            By.ID, 'logPassword'
        ).send_keys(self.passwd + Keys.RETURN)

        WebDriverWait(self.driver, 3).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'join_btn'))
        )

        games = RevasCore.get_games(self.driver)
        self.game_id, self.company_name = RevasCore.choose_game(games)

        self.driver.find_element(By.ID, f'join_btn_{self.game_id}').click()

        round_no = WebDriverWait(self.driver, 3).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'current-round-number'))
        ).text.split()[0]

        url = self.driver.current_url

        self.url = url[:url.rindex('/') + 1]
        self.game_name = url[8 : url.index('.')]
        self.round_no = int(round_no)

        RevasCache.store_game_name(self.game_name)

    def get_data_count(self, mod: str) -> int:
        self.driver.get(self.url + mod + '.php')

        try:
            WebDriverWait(self.driver, 3).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'light-well-item'))
            )

            return len(self.driver.find_elements(By.CLASS_NAME, 'light-well-item'))
        except TimeoutException:
            return 0

    def get_xlsx(self, item_data: tuple[str, str, str, str]) -> str:
        id_name, item_id, mod, action = item_data

        download_url = \
            self.url + \
            f'ajax.php?mod={mod}&action={action}-export-to-exel&{id_name}=' + \
            f'{item_id}&tab=empty&atype=json'

        self.driver.set_page_load_timeout(2)
        self.driver.get(download_url)

        sleep(1)

        for down_file in os.listdir(RevasCore.home_path()):
            if (
                'Dostawca' in down_file or
                'Wymagania dotyczące usługi' in down_file or
                'Lista pracowników dostępnych na rynku pracy' in down_file or
                'Historia rachunku' in down_file
            ):
                return down_file

        return ''

    def get_schedule(self) -> None:
        self.driver.get('https://gry.revas.pl/default.php')

        schedule_path = WebDriverWait(self.driver, 3).until(
            EC.presence_of_element_located((
                By.XPATH,
                f'//TR[TD/BUTTON/@playergameid={self.game_id}]/TD/A[@data-toggle]'
            ))
        ).get_attribute('href')

        self.driver.get(schedule_path)

        table = WebDriverWait(self.driver, 3).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'table-in-modal-dialog'))
        )

        rows = table.find_elements(By.TAG_NAME, 'tr')

        arr = []

        for row in rows:
            cells = row.find_elements(By.XPATH, './*')

            if cells[0].tag_name == 'th':
                arr.append([cell.text for cell in cells])
            else:
                arr.append([
                    cells[0].text,
                    cells[1].text,
                    not (cells[2].find_element(By.XPATH, './*').tag_name == 'hr' or
                    'blocked' in cells[2].find_element(By.XPATH, './*').get_attribute('src'))
                ])

        RevasPandas.muli_dim_arr_to_csv(
            arr,
            f'download/schedule/{self.game_id}.csv'
        )

        self.driver.get_screenshot_as_file(
            f'download/schedule/{self.game_id}.png'
        )

        self.driver.minimize_window()
        self.driver.back()
        self.driver.back()

    def get_scores(self) -> dict[str, dict[str, int]]:
        self.driver.get(f'{self.url}ajax.php?mod=sale&tab=results')

        scores = [
            i.get_attribute('data-title')
            for i in self.driver.find_elements(
                By.XPATH, './/div[contains(@class, "group_well_item_title")]/i'
            )
        ]

        data = [
            {
                row.find_elements(
                    By.TAG_NAME, 'td'
                )[0].text:
                    float(
                        row.find_elements(By.TAG_NAME, 'td')[1].text.replace(' %', 'e-2')
                        if '%' in row.find_elements(By.TAG_NAME, 'td')[1].text
                        else row.find_elements(By.TAG_NAME, 'td')[1].text.replace(' ', '')
                        if len(row.find_elements(By.TAG_NAME, 'td')[1].text)
                        else 0
                    )
                for row in body.find_elements(By.TAG_NAME, 'tr')
            }
            for body in self.driver.find_elements(By.TAG_NAME, 'tbody')
        ]

        self.driver.back()

        return dict(zip(scores, data))

    def get_products(self, shop_no: int) -> dict[str, dict[str, str]]:
        buttons = WebDriverWait(self.driver, 3).until(
            EC.presence_of_all_elements_located((
                By.XPATH,
                './/a[contains(@class, "btn-more") and not(contains(@class, "supplier-basket"))]'
            ))
        )
        shop_names = [
            shop.text.lower()
            for shop in self.driver.find_elements(By.CLASS_NAME, 'light-well-title')
        ]

        buttons[shop_no].click()

        # HACK: This is a workaround for the select element not being found
        # Normally I would use the WebDriverWait, but it doesn't work here

        sleep(1)

        # Select(WebDriverWait(self.driver, 3).until(
        #     EC.element_to_be_clickable((By.TAG_NAME, 'select'))
        # )).select_by_value('100')

        Select(
            self.driver.find_element(By.TAG_NAME, 'select')
        ).select_by_value('100')

        parts = [
            {
                'name': row.find_element(
                    By.CLASS_NAME, 'container_name_info'
                ).text.lower().replace('\n', ' '),
                'quality': len(
                    row.find_elements(By.XPATH, './/img[contains(@src, "star.svg")]')
                ),
                'supplier': shop_names[shop_no]
            } for row in self.driver.find_elements(By.XPATH, './/tbody/tr')
        ]

        keys = {
            i.split('=')[0]: i.split('=')[1]
            for i in self.execute_script(
                'return $("#part_database_ajax_frm").serialize()'
            ).split('&')
        }.keys()

        keys = list(filter(lambda key: 'partSupplierHasPartID' in key, keys))

        keys = [key[key.rindex('_') + 1:] for key in keys]

        data = dict(zip(keys, parts))

        self.driver.refresh()

        return data

    def execute_script(self, script: str) -> Any:
        return self.driver.execute_script(script)

    def quit(self, timeout: float=0) -> None:
        sleep(timeout)

        self.driver.quit()
        sys.exit()
