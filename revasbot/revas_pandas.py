import pandas as pd

class RevasPandas:
    # def __init__():
    #     pass

    @classmethod
    def xlsx_to_csv(cls, sheet_from: str, sheet_to: str):
        data = pd.read_excel(sheet_from, header=2)
        data.to_csv(sheet_to, index=False)

        print(pd.DataFrame(pd.read_csv(sheet_to)))

