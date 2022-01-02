import pandas as pd

from revasbot.revas_console import RevasConsole as console

class RevasPandas:
    # def __init__():
    #     pass

    @classmethod
    def xlsx_to_csv(cls, sheet_from: str, sheet_to: str):
        # console.debug(sheet_from)
        data = pd.read_excel(sheet_from)
        # data = pd.read_excel(sheet_from, header=2)
        data.to_csv(sheet_to, index=True)

        # console.debug(pd.DataFrame(pd.read_csv(sheet_to)))
