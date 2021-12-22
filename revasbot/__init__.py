__authors__ = ['iwo-strzebonski', 'raphaelsanti-source']
__license__ = 'WTFLP'
__version__ = '1.0.0'

import os
import shutil

from revasbot.revas_core import RevasCore
from revasbot.revas_scrapper import RevasScrapper


def setup():
    try:
        shutil.rmtree('download')
    except FileNotFoundError:
        pass

    os.mkdir('download')
    os.mkdir('download/offer')
    os.mkdir('download/suppliers')
    os.mkdir('download/finance_bank')
    os.mkdir('download/hr_employment')

    revas_core = RevasCore()
    user_name, password, game_id = revas_core.config_loader()

    revas_scrapper = RevasScrapper(user_name, password, game_id)
    revas_scrapper.login()

    game_name = revas_scrapper.game_name

    if os.path.exists(os.path.join('cache', game_name + '.yml')):
        revas_scrapper.smart_scrap_xlsx(game_name)
    else:
        if not os.path.exists('cache'):
            os.mkdir('cache')

        revas_scrapper.scrap_xlsxs(game_name)

    revas_scrapper.quit()
