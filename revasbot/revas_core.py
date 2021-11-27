from typing import Tuple
from getpass import getpass

import os
import sys
import yaml


class RevasCore:
    # def __init__(self) -> None:
    #     pass

    @classmethod
    def config_loader(cls) -> Tuple[str, str, str]:
        try:
            with open('config.yml', 'r', encoding='utf-8') as conf_file:
                config = yaml.load(conf_file, Loader=yaml.FullLoader)

        except FileNotFoundError:
            usr_name = input('Type your Revas account username: ')
            passwd = getpass('Type your Revas account password: ')
            game_id = input('Type your Revas game ID: ')

            with open('config.yml', 'w', encoding='utf-8') as conf_file:
                yaml.dump({
                    'USER': usr_name,
                    'PASSWD': passwd,
                    'GAME_ID': game_id
                }, conf_file)

            if any(i == '' for i in [usr_name, passwd, game_id]):
                print('Please provide user data!')
                sys.exit()

            print('No config.yml found, creating a new one...')
            config = {
                'USER': usr_name,
                'PASSWD': passwd,
                'GAME_ID': game_id
            }

        if any(config[key] is None for key in config):
            print('Please provide user data!')
            sys.exit()

        return (
            str(config['USER']),
            str(config['PASSWD']),
            str(config['GAME_ID'])
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
