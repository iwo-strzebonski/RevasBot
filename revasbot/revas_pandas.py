import pandas as pd

# from revasbot.revas_console import RevasConsole as console

class RevasPandas:
    @classmethod
    def xlsx_to_csv(cls, sheet_from: str, sheet_to: str) -> None:
        # console.debug(sheet_from)
        data_frame = pd.read_excel(sheet_from)
        # data_frame = pd.read_excel(sheet_from, header=2)
        data_frame.to_csv(sheet_to, index=True)

        # console.debug(pd.DataFrame(pd.read_csv(sheet_to)))

    @classmethod
    def muli_dim_arr_to_csv(cls, data: list[list[str]], path: str) -> None:
        data_frame = pd.DataFrame(data[1:], columns=data[0])
        data_frame.to_csv(path)
        # console.debug(str(data_frame))

    @classmethod
    def dict_to_csv(cls, data: dict[str, dict[str, int]], path: str = '') -> None:
        with pd.ExcelWriter(path) as writer:        # pylint: disable=abstract-class-instantiated
            for key, value in data.items():
                data_frame = pd.DataFrame.from_dict(value, orient='index', columns=['count'])
                data_frame.to_excel(writer, sheet_name=key)

            writer.save()
