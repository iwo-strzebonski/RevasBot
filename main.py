import os
import sys
import yaml

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

PATH = os.getcwd()

try:
    with open(f'{PATH}/config.yml', 'r', encoding='utf-8') as file:
        CONFIG = yaml.load(file, Loader=yaml.FullLoader)

except FileNotFoundError:
    with open(f'{PATH}/config.yml', 'w', encoding='utf-8') as file:
        yaml.dump({ 'USER': None, 'PASSWD': None, 'GAME_ID': None }, file)
        file.close()

    print('No config.yml found')
    sys.exit()

# print(CONFIG)

USER = CONFIG['USER']
PASSWD = CONFIG['PASSWD']
GAME_ID = CONFIG['GAME_ID']

browser = webdriver.Firefox()
browser.get('https://gry.revas.pl/')

username = browser.find_element_by_id('logEmail')
username.send_keys(USER)
password = browser.find_element_by_id('logPassword')
password.send_keys(PASSWD + Keys.RETURN)

enter_game = WebDriverWait(browser, 10).until(
    EC.presence_of_element_located((By.ID, f'join_btn_{GAME_ID}')))
enter_game.click()

# browser.quit()
