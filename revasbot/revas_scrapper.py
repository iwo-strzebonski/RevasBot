import os

from revasbot.revas_console import RevasConsole as console
from revasbot.revas_core import RevasCore
from revasbot.revas_selenium import RevasSelenium
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
            'finance_bank': {
                'id': 'bankID',
                'action': 'finance-bank'
            },
            'hr_employment': {
                'id': 'positionID',
                'action': 'employes'
            }
        }

        self.revas_selenium = revas_selenium

    def smart_scrap_xlsx(self, game_name: str) -> None:
        config = RevasCore.cache_loader(game_name)

        for key, id_list in config.items():
            page_info = self.special_pages[key]

            for item_id in id_list.keys():
                item_data = (
                    page_info['id'],
                    item_id,
                    key,
                    page_info['action']
                )

                spreadsheet = self.revas_selenium.get_xlsx(item_data)

                os.rename(
                    os.path.join(RevasCore.home_path(), spreadsheet),
                    os.path.join(
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

            if key in ['finance_bank', 'hr_employment']:
                item_id = 1
            else:
                count = self.revas_selenium.get_data_count(key)

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

                    os.rename(
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

        RevasCore.cache_saver(game_name, cache_data)
        self.revas_selenium.driver.back()

    def scrap_scores(self) -> None:
        if self.revas_selenium.round_no > 2:
            scores = self.revas_selenium.get_scores()
            RevasPandas.dict_to_csv(
                scores,
                f'download/scores/scores_round_{self.revas_selenium.round_no}.xlsx'
            )
            # https://restauracja.revas.pl/ajax.php?mod=sale&tab=results
        else:
            console.warn('Wyniki dostępne od rundy 3')
