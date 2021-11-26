import os

from revasbot.revas_pandas import RevasPandas
from revasbot.revas_selenium import RevasSelenium

class RevasScrapper(RevasSelenium):
    def __init__(self, usr_name: str, passwd: str, game_id: str) -> None:
        super().__init__(usr_name, passwd, game_id)

        self.id_names = {
            'offer': 'serviceID',
            'suppliers': 'partSupplierID',
            'finance_bank': 'bankID'        # bankID = 1
        }

        self.offer_tabs = [
            'tool_tab',
            'emploees_tab',
            'parts_tab'
        ]

        self.special_pages = {
            'hr_employment': 'hire',
            'hr_training': 'decisions'
        }

        self.revas_pandas = RevasPandas

    def scrap_offer_info(self, item_id: int) -> int:
        i = 0

        for tab in self.offer_tabs:
            spreadsheet = self.get_xlsx(self.id_names['offer'], item_id, 'offer', tab)

            if 'NOT_FOUND' not in spreadsheet:
                self.revas_pandas.xlsx_to_csv(
                    os.path.join(os.getcwd(), 'temp', spreadsheet),
                    os.path.join(
                        os.getcwd(),
                        'download',
                        'offer',
                        tab,
                        spreadsheet.replace('.xlsx', '.csv')
                    )
                )

                if self.offer_tabs.index(tab) == 2:
                    i = 1

            os.remove(os.path.join(os.getcwd(), 'temp', spreadsheet))

            if 'NOT_FOUND' in spreadsheet:
                return 0

        return i

    def scrap_xlsxs(self) -> None:
        for id_key, id_name in self.id_names.items():
            i = 0

            if id_key == 'finance_bank':
                count = 1
                item_id = 1
            else:
                item_id = 0
                count = self.get_data_count(id_key)

            while i < count:
                if id_key == 'offer':
                    i += self.scrap_offer_info(item_id)
                else:
                    spreadsheet = self.get_xlsx(id_name, item_id, id_key)

                    if 'NOT_FOUND' not in spreadsheet:
                        self.revas_pandas.xlsx_to_csv(
                            os.path.join(os.getcwd(), 'temp', spreadsheet),
                            os.path.join(
                                os.getcwd(),
                                'download',
                                id_key,
                                spreadsheet.replace('.xlsx', '.csv')
                            )
                        )

                        i += 1

                    os.remove(os.path.join(os.getcwd(), 'temp', spreadsheet))

                item_id += 1

        self.driver.get(self.url)
