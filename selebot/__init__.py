__authors__ = ['iwo-strzebonski', 'raphaelsanti-source']
__license__ = 'WTFLP'
__version__ = '1.0.0'

import os
import shutil


from selebot.selebot_core import SelebotCore
from selebot.revas_selenium import RevasSelenium

def setup():
    try:
        shutil.rmtree('temp')
        shutil.rmtree('download')
    except FileNotFoundError:
        pass

    os.mkdir('temp')
    os.mkdir('download')
    os.mkdir('download/offer')
    os.mkdir('download/suppliers')

    selebot_core = SelebotCore()
    user_name, password, game_id = selebot_core.config_loader()

    revas_selenium = RevasSelenium(user_name, password, game_id)

    url = revas_selenium.login()
    revas_selenium.scrap_xlsxs()

    print(url)
    # revas_selenium.quit(2)
