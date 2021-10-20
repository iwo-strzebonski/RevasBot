import os
import sys
import yaml

from typing import Tuple
from revas_selenium import RevasSelenium

def loadConfig() -> Tuple[str, str, int]:
    path = os.getcwd()

    try:
        with open(f'{path}/config.yml', 'r', encoding='utf-8') as file:
            config = yaml.load(file, Loader=yaml.FullLoader)
    except FileNotFoundError:
        usr_name = input('Type your Revas account username: ')
        passwd = input('Type your Revas account password: ')
        game_id = input('Type your Revas game ID: ')

        with open(f'{path}/config.yml', 'w', encoding='utf-8') as file:
            yaml.dump({
                'USER': usr_name,
                'PASSWD': passwd,
                'GAME_ID': game_id
            }, file)

            file.close()

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


if __name__ == '__main__':
    USR_NAME, PASSWD, GAME_ID = loadConfig()
    revasSelenium = RevasSelenium(USR_NAME, PASSWD, GAME_ID)
    revasSelenium.login()
    # revasSelenium.quit(2)
