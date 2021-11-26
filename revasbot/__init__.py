__authors__ = ['iwo-strzebonski', 'raphaelsanti-source']
__license__ = 'WTFLP'
__version__ = '1.0.0'

import os
import shutil

from revasbot.revas_core import RevasCore
from revasbot.revas_scrapper import RevasScrapper


def setup():
    try:
        shutil.rmtree('temp')
        shutil.rmtree('download')
    except FileNotFoundError:
        pass

    os.mkdir('temp')
    os.mkdir('download')
    os.mkdir('download/offer')
    os.mkdir('download/offer/emploees_tab')
    os.mkdir('download/offer/parts_tab')
    os.mkdir('download/offer/tool_tab')
    os.mkdir('download/suppliers')
    os.mkdir('download/finance_bank')

    revas_core = RevasCore()
    user_name, password, game_id = revas_core.config_loader()

    revas_scrapper = RevasScrapper(user_name, password, game_id)
    revas_scrapper.login()

    revas_scrapper.scrap_xlsxs()

    # revas_scrapper.quit(2)
