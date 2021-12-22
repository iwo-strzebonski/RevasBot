import os

from revasbot.revas_selenium import RevasSelenium
from revasbot.revas_core import RevasCore
# from revasbot.revas_pandas import RevasPandas

class RevasScrapper(RevasSelenium):
    def __init__(self, usr_name: str, passwd: str, game_id: str) -> None:
        super().__init__(usr_name, passwd, game_id)

        self.special_pages = {
            'offer': {
                'id': 'serviceID',
                'action': 'offer'
            },
            'suppliers': {
                'id': 'partSupplierID',
                'action': 'suppliers'
            },
            'finance_bank': {
                'id': 'bankID',
                'action': 'finance-bank'
            },
            'hr_employment': {
                'id': 'positionID',
                'action': 'employes'
            }
            # 'hr_training': 'decisions'
        }

        self.revas_core = RevasCore
        # self.revas_pandas = RevasPandas

    def smart_scrap_xlsx(self, game_name: str) -> None:
        config = self.revas_core.cache_loader(game_name)

        for key, id_list in config.items():
            page_info = self.special_pages[key]

            for item_id in id_list.keys():
                item_data = (
                    page_info['id'],
                    item_id,
                    key,
                    page_info['action']
                )

                spreadsheet = self.get_xlsx(item_data)

                os.rename(
                    os.path.join(self.download_path, spreadsheet),
                    os.path.join(
                        os.getcwd(),
                        'download',
                        key,
                        spreadsheet
                    )
                )

    def scrap_xlsxs(self, game_name: str) -> None:
        cache_data = {}

        for key, value in self.special_pages.items():
            cache_data[key] = {}

            item_id = 0
            count = 1

            i = 0

            if key == 'finance_bank':
                item_id = 1
            elif key == 'hr_employment':
                item_id = 1
            else:
                count = self.get_data_count(key)

            while i < count:
                item_data = (
                    value['id'],
                    str(item_id),
                    key,
                    value['action']
                )

                spreadsheet = self.get_xlsx(item_data)

                if 'NOT_FOUND' not in spreadsheet:
                    cache_data[key][item_id] = spreadsheet
                    print(str(item_id) + ': ' + spreadsheet)

                    os.rename(
                        os.path.join(self.download_path, spreadsheet),
                        os.path.join(
                            'download',
                            key,
                            spreadsheet
                        )
                    )

                    i += 1
                else:
                    os.remove(os.path.join(self.download_path, spreadsheet))

                item_id += 1

        self.revas_core.cache_saver(game_name, cache_data)
        self.driver.get(self.url)
