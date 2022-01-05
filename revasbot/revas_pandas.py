import pandas as pd

# from revasbot.revas_console import RevasConsole as console

class RevasPandas:
    @classmethod
    def muli_dim_arr_to_csv(cls, data: list[list[str]], path: str) -> None:
        data_frame = pd.DataFrame(data[1:], columns=data[0])
        data_frame.to_csv(path)
        # console.debug(str(data_frame))

    @classmethod
    def dict_to_xlsx(cls, data: dict[str, dict[str, int]], path: str = '') -> None:
        with pd.ExcelWriter(path) as writer:        # pylint: disable=abstract-class-instantiated
            for key, value in data.items():
                data_frame = pd.DataFrame.from_dict(value, orient='index', columns=['count'])
                data_frame.to_excel(writer, sheet_name=key)

            writer.save()

    @classmethod
    def read_csv(cls, path: str) -> dict[str, dict[str, str]]:
        return pd.read_csv(path).to_dict()
