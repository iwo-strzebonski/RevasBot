import os
import sys
import yaml

from time import sleep

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def loadConfig():
    PATH = os.getcwd()

    try:
        with open(f'{PATH}/config.yml', 'r', encoding='utf-8') as file:
            config = yaml.load(file, Loader=yaml.FullLoader)
    except FileNotFoundError:
        usr_name = input('Type your Revas account username: ')
        passwd = input('Type your Revas account password: ')
        game_id = input('Type your Revas game ID: ')

        with open(f'{PATH}/config.yml', 'w', encoding='utf-8') as file:
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

class RevasSelenium(object):
    def __init__(self, usr_name: str, passwd: str, game_id: int):
        self.browser = webdriver.Firefox()
        self.browser.get('https://gry.revas.pl/')

        self.usr_name = usr_name
        self.passwd = passwd
        self.game_id = game_id

    def login(self):
        self.browser.find_element_by_id('logEmail').send_keys(self.usr_name)
        self.browser.find_element_by_id('logPassword').send_keys(self.passwd + Keys.RETURN)

        enter_game = WebDriverWait(self.browser, 1).until(
            EC.presence_of_element_located((By.ID, f'join_btn_{self.game_id}')))
        enter_game.click()

        return 0

    def quit(self, timeout: float = 0):
        sleep(timeout)
        self.browser.quit()


if __name__ == '__main__':
    USR_NAME, PASSWD, GAME_ID = loadConfig()
    revasSelenium = RevasSelenium(USR_NAME, PASSWD, GAME_ID)
    revasSelenium.login()
    # revasSelenium.quit(2)
