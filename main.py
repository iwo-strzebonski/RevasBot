import os
import sys
import yaml

from typing import Tuple
from revas_selenium import Revas_Selenium

def main() -> Tuple[str, str, int]:
    path = os.getcwd()
    
    try:
        os.mkdir('temp')
        os.mkdir('download')
    except:
        for f in os.listdir(os.path.join(os.getcwd(), 'temp')):
            os.remove(os.path.join(os.getcwd(), 'temp', f))
        for f in os.listdir(os.path.join(os.getcwd(), 'download')):
            os.remove(os.path.join(os.getcwd(), 'download', f))

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
    USR_NAME, PASSWD, GAME_ID = main()

    revas_selenium = Revas_Selenium(USR_NAME, PASSWD, GAME_ID)

    url = revas_selenium.login()
    offer_count = revas_selenium.get_offer_count(url)
    id = 0
    i = 0

    print(url)
    print(offer_count)

    while i < offer_count:
        f = revas_selenium.get_xlsx(url, id)

        if 'DB_SERVICE_0_NOT_FOUND' not in os.listdir(os.path.join(os.getcwd(), 'temp'))[0]:
            os.rename(
                os.path.join(os.getcwd(), 'temp', f),
                os.path.join(os.getcwd(), 'download', f)
            )
            print(f'{id}: {f}')
            i += 1
        else:
            os.remove(os.path.join(os.getcwd(), 'temp', f)) 

        id += 1
        
    # revas_selenium.quit(2)
