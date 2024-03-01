import os
import shutil

from revasbot.revas_console import RevasConsole as console
from revasbot.revas_core import RevasCore
from revasbot.revas_cache import RevasCache
from revasbot.selenium.revas_selenium import RevasSelenium
from revasbot.revas_pandas import RevasPandas

class RevasScrapper:
    def __init__(self, revas_selenium: RevasSelenium) -> None:
        self.special_pages = {
            'offer': {
                'id': 'serviceID',
                'action': 'offer'
            },
            'suppliers': {
                'id': 'partSupplierID',
                'action': 'suppliers'
            },
            # 'finance_bank': {
            #     'id': 'bankID',
            #     'action': 'finance-bank'
            # },
            'hr_employment': {
                'id': 'positionID',
                'action': 'employes'
            }
        }

        self.revas_selenium = revas_selenium

    def smart_scrap_xlsx(self) -> None:
        config = RevasCache.cache_loader(
            self.revas_selenium.game_name
        )

        for key, id_list in config.items():
            if not key in self.special_pages:
                continue

            page_info = self.special_pages[key]

            for item_id in id_list.keys():
                item_data = (
                    page_info['id'],
                    item_id,
                    key,
                    page_info['action']
                )

                spreadsheet = self.revas_selenium.get_xlsx(item_data)

                shutil.move(
                    os.path.join(RevasCore.home_path(), spreadsheet),
                    os.path.join(
                        'download',
                        key,
                        spreadsheet
                    )
                )

    def scrap_xlsxs(self) -> None:
        cache_data = {}

        for key, value in self.special_pages.items():
            cache_data[key] = {}

            item_id = 0
            count = 1

            i = 0

            if key == 'hr_employment':
                item_id = 1
            else:
                count = self.revas_selenium.get_data_count(key)
                count = 6 if not count else count

            while i < count:
                item_data = (
                    value['id'],
                    str(item_id),
                    key,
                    value['action']
                )

                spreadsheet = self.revas_selenium.get_xlsx(item_data)

                if 'NOT_FOUND' not in spreadsheet:
                    cache_data[key][item_id] = spreadsheet
                    console.debug(str(item_id) + ': ' + spreadsheet)

                    shutil.move(
                        os.path.join(RevasCore.home_path(), spreadsheet),
                        os.path.join(
                            'download',
                            key,
                            spreadsheet
                        )
                    )

                    i += 1
                else:
                    os.remove(os.path.join(RevasCore.home_path(), spreadsheet))

                item_id += 1

        RevasCache.cache_saver(
            self.revas_selenium.game_name, cache_data
        )
        self.revas_selenium.driver.back()

    def scrap_finance_bank(self):
        item_data = (
            'bankID',
            '1',
            'finance_bank',
            'finance-bank'
        )

        spreadsheet = self.revas_selenium.get_xlsx(item_data)

        shutil.move(
            os.path.join(RevasCore.home_path(), spreadsheet),
            os.path.join(
                'download',
                'finance_bank',
                spreadsheet
            )
        )

    def scrap_scores(self) -> None:
        if self.revas_selenium.round_no > 2:
            scores = self.revas_selenium.get_scores()
            RevasPandas.dict_to_xlsx(
                scores, 'download/scores/sales.xlsx'
            )
        else:
            console.warn('Wyniki dostępne od rundy 3')

    def scrap_products(self) -> None:
        count = self.revas_selenium.get_data_count('suppliers')

        # HACK: Since recently, you need to maximize the window to get the list of products
        self.revas_selenium.driver.maximize_window()

        if count:
            data = {
                key: value for d in [
                    self.revas_selenium.get_products(i) for i in range(count)
                ] for key, value in d.items()
            }

            RevasCache.update_cache(
                self.revas_selenium.game_name, 'resources', data
            )

            # 'parts_table_length': '100'
        else:
            console.warn('Lista dostawców jest niedostępna, nie można pobrać listy produktów')

        # self.revas_selenium.driver.back()
