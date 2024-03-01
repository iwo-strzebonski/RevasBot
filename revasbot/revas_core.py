import os
import platform

from selenium.webdriver.common.by import By
from revasbot.revas_console import RevasConsole as console

if platform.system() == 'Windows':
    import winreg

class RevasCore:
    @classmethod
    def get_games(cls, driver) -> list[dict[str, str]]:
        table = driver.find_element(By.ID, 'player_games')
        tbody = table.find_elements(By.TAG_NAME, 'tbody')[0]
        rows = tbody.find_elements(By.TAG_NAME, 'tr')
        games = tbody.find_elements(By.CLASS_NAME, 'join_btn')

        return [
            {
                'game_name': row.find_elements(By.TAG_NAME, 'td')[1].text,
                'game_type': row.find_elements(By.TAG_NAME, 'td')[2].text,
                'company_name': row.find_elements(By.TAG_NAME, 'td')[3].text,
                'game_id': games[i].get_attribute('playergameid')
            } for i, row in enumerate(rows)
        ]

    @classmethod
    def choose_game(cls, games: list[dict[str, str]]) -> tuple[str, str]:
        console.header('Choose a game to start:')

        game_number = None
        game_messages = [
            f'{game["game_name"]} ({game["game_type"]}) - {game["company_name"]}'
            for game in games
        ]

        console.list(game_messages)

        while not game_number:
            try:
                game_number = int(input())
            except ValueError:
                game_number = None

        # console.debug(games[game_number - 1]['game_id'])
        return (
            games[game_number - 1]['game_id'],
            games[game_number - 1]['company_name']
        )

    @classmethod
    def home_path(cls) -> str:
        if platform.system() == 'Windows':
            key = winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                r'Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders'
            )

            directory, _qtype = winreg.QueryValueEx(key, '{374DE290-123F-4565-9164-39C4925E467B}')

            return directory

        return os.path.expanduser('~/Downloads')
