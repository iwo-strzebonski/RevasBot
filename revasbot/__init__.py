__authors__ = ['iwo-strzebonski']
__license__ = 'WTFLP'
__version__ = '2.0.2'

import os
import shutil

from revasbot.revas_core import RevasCore
from revasbot.revas_scrapper import RevasScrapper

def clear_xlsx() -> None:
    download_path = os.path.expanduser('~/Downloads')

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

    user_name, password = RevasCore.config_loader()

    revas_scrapper = RevasScrapper(user_name, password)
    revas_scrapper.login()

    game_name = revas_scrapper.game_name

    if os.path.exists(os.path.join('cache', game_name + '.yml')):
        revas_scrapper.smart_scrap_xlsx(game_name)
    else:
        if not os.path.exists('cache'):
            os.mkdir('cache')

        revas_scrapper.scrap_xlsxs(game_name)

    revas_scrapper.quit()
