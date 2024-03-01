import os
import sys
from typing import Any
import yaml

from revasbot.revas_console import RevasConsole as console

class RevasCache:
    @classmethod
    def config_loader(cls) -> tuple[str, str, str]:
        try:
            with open('config.yml', 'r', encoding='utf-8') as conf_file:
                config = yaml.load(conf_file, Loader=yaml.FullLoader)

        except FileNotFoundError:
            usr_name = console.input('Type your Revas account username: ')
            passwd = console.getpass('Type your Revas account password: ')

            while any(i == '' for i in { usr_name, passwd }):
                console.warn('Please provide user data!')
                usr_name = console.input('Type your Revas account username: ')
                passwd = console.getpass('Type your Revas account password: ')

            with open('config.yml', 'w', encoding='utf-8') as conf_file:
                yaml.dump({
                    'USER': usr_name,
                    'PASSWD': passwd,
                    'last_game_name': ''
                }, conf_file)

            console.debug('No config.yml found, creating a new one...')
            config = {
                'USER': usr_name,
                'PASSWD': passwd,
                'last_game_name': ''
            }

        if any(config[key] is None for key in config):
            console.error('Please provide user data!')
            sys.exit()

        return (
            str(config['USER']),
            str(config['PASSWD']),
            str(config['last_game_name'])
        )

    @classmethod
    def cache_loader(cls, file_name: str) -> dict[str, Any]:
        with open(
            os.path.join('cache', file_name + '.yml'),
            'r', encoding='utf-8'
        ) as cached_file:
            return yaml.load(cached_file, Loader=yaml.FullLoader)

    @classmethod
    def cache_saver(cls, file_name: str, data: dict[str, dict[str, int]]) -> None:
        with open(
            os.path.join('cache', file_name + '.yml'),
            'w', encoding='utf-8'
        ) as cached_file:
            yaml.dump(data, cached_file)

    @classmethod
    def update_cache(cls, file_name: str, key: str, data: dict[str, dict[str, str]]):
        cache = cls.cache_loader(file_name)

        cache[key] = data         # type: ignore

        cls.cache_saver(file_name, cache)

    @classmethod
    def store_game_name(cls, game_name: str):
        with open('config.yml', 'r', encoding='utf-8') as conf_file:
            config = yaml.load(conf_file, Loader=yaml.FullLoader)

        config['last_game_name'] = game_name

        with open('config.yml', 'w', encoding='utf-8') as conf_file:
            yaml.dump(config, conf_file)
