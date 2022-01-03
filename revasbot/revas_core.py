from typing import Tuple

import os
import sys
import platform
import yaml

from selenium.webdriver.common.by import By

from revasbot.revas_console import RevasConsole as console

class RevasCore:
    # def __init__(self) -> None:
    #     pass

    @classmethod
    def config_loader(cls) -> Tuple[str, str]:
        try:
            with open('config.yml', 'r', encoding='utf-8') as conf_file:
                config = yaml.load(conf_file, Loader=yaml.FullLoader)

        except FileNotFoundError:
            usr_name = console.input('Type your Revas account username: ')
            passwd = console.getpass('Type your Revas account password: ')

            while any(i == '' for i in [usr_name, passwd]):
                console.warn('Please provide user data!')
                usr_name = console.input('Type your Revas account username: ')
                passwd = console.getpass('Type your Revas account password: ')

            with open('config.yml', 'w', encoding='utf-8') as conf_file:
                yaml.dump({
                    'USER': usr_name,
                    'PASSWD': passwd
                }, conf_file)

            console.debug('No config.yml found, creating a new one...')
            config = {
                'USER': usr_name,
                'PASSWD': passwd,
            }

        if any(config[key] is None for key in config):
            console.error('Please provide user data!')
            sys.exit()

        return (
            str(config['USER']),
            str(config['PASSWD'])
        )

    @classmethod
    def cache_loader(cls, file_name: str) -> dict[str, dict[str, int]]:
        with open(os.path.join('cache', file_name + '.yml'), 'r', encoding='utf-8') as cached_file:
            config = yaml.load(cached_file, Loader=yaml.FullLoader)

        return config

    @classmethod
    def cache_saver(cls, file_name: str, data: dict[str, dict[str, int]]) -> None:
        with open(os.path.join('cache', file_name + '.yml'), 'w', encoding='utf-8') as cached_file:
            yaml.dump(data, cached_file)

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
    def choose_game(cls, games: list[dict[str, str]]) -> str:
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

        console.debug(games[game_number - 1]['game_id'])
        return games[game_number - 1]['game_id']

    @classmethod
    def home_path(cls) -> str:
        if platform.system() == 'Windows':
            import winreg

            key = winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                r'Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders'
            )

            directory, _qtype = winreg.QueryValueEx(key, '{374DE290-123F-4565-9164-39C4925E467B}')

            return directory

        return os.path.expanduser('~/Downloads')
