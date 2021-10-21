from typing import Tuple

import os
import sys
import yaml

class SelebotCore:
    def __init__(self) -> None:
        self.path = os.getcwd()

    def config_loader(self) -> Tuple[str, str, int]:
        try:
            with open(f'{self.path}/config.yml', 'r', encoding='utf-8') as conf_file:
                config = yaml.load(conf_file, Loader=yaml.FullLoader)
        except FileNotFoundError:
            usr_name = input('Type your Revas account username: ')
            passwd = input('Type your Revas account password: ')
            game_id = input('Type your Revas game ID: ')

            with open(f'{self.path}/config.yml', 'w', encoding='utf-8') as conf_file:
                yaml.dump({
                    'USER': usr_name,
                    'PASSWD': passwd,
                    'GAME_ID': game_id
                }, conf_file)

                conf_file.close()

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

        return config['USER'], config['PASSWD'], config['GAME_ID']
