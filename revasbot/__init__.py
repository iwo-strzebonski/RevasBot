__authors__ = ['iwo-strzebonski', 'hoxton314']
__license__ = 'WTFLP'
__version__ = '2.0.4'

import os
import shutil

from revasbot.revas_core import RevasCore
from revasbot.revas_selenium import RevasSelenium
from revasbot.revas_scrapper import RevasScrapper

def clear_xlsx() -> None:
    download_path = RevasCore.home_path()

    for down_file in os.listdir(download_path):
        if (
            'Dostawca' in down_file or
            'Wymagania dotyczące usługi' in down_file or
            'Lista pracowników dostępnych na rynku pracy' in down_file or
            'Historia rachunku' in down_file
        ):
            os.remove(os.path.join(download_path, down_file))

def setup():
    try:
        shutil.rmtree('download')
    except FileNotFoundError:
        pass

    clear_xlsx()

    os.mkdir('download')
    os.mkdir('download/offer')
    os.mkdir('download/suppliers')
    os.mkdir('download/finance_bank')
    os.mkdir('download/hr_employment')
    os.mkdir('download/schedule')
    os.mkdir('download/scores')

    user_name, password = RevasCore.config_loader()

    revas_selenium = RevasSelenium(user_name, password)
    revas_selenium.login()

    revas_scrapper = RevasScrapper(revas_selenium)

    game_name = revas_selenium.game_name

    revas_scrapper.scrap_scores()

    if os.path.exists(f'cache/{revas_selenium.game_name}.yml'):
        revas_scrapper.smart_scrap_xlsx(game_name)
    else:
        if not os.path.exists('cache'):
            os.mkdir('cache')

        revas_scrapper.scrap_xlsxs(game_name)

    revas_selenium.quit()
