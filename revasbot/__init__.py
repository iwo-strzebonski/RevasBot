__author__ = 'iwo-strzebonski'
__license__ = 'WTFLP'
__version__ = '2.1.0'

import os
import shutil

from revasbot.revas_core import RevasCore
from revasbot.revas_cache import RevasCache
from revasbot.selenium.revas_selenium import RevasSelenium
from revasbot.selenium.revas_scrapper import RevasScrapper
from revasbot.revas_shopper import RevasShopper

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

def init_dirs(game_changed: bool) -> bool:
    try:
        shutil.rmtree('analysis')
    except FileNotFoundError:
        pass

    try:
        os.mkdir('shop')
    except FileExistsError:
        pass

    os.mkdir('analysis')

    if not game_changed and \
        os.path.exists('download/hr_employment') and len(os.listdir('download/hr_employment')) and \
        os.path.exists('download/offer') and len(os.listdir('download/offer')) == 15 and \
        os.path.exists('download/suppliers') and len(os.listdir('download/suppliers')) == 6:

        try:
            shutil.rmtree('download/finance_bank')
            os.mkdir('download/finance_bank')
        except FileNotFoundError:
            pass

        try:
            shutil.rmtree('download/schedule')
            os.mkdir('download/schedule')
        except FileNotFoundError:
            pass

        try:
            shutil.rmtree('download/scores')
            os.mkdir('download/scores')
        except FileNotFoundError:
            pass

        return True

    try:
        shutil.rmtree('download')
    except FileNotFoundError:
        pass

    os.mkdir('download')
    os.mkdir('download/offer')
    os.mkdir('download/suppliers')
    os.mkdir('download/finance_bank')
    os.mkdir('download/hr_employment')
    os.mkdir('download/schedule')
    os.mkdir('download/scores')

    return False

def init_scrapper(revas_scrapper: RevasScrapper, game_name: str) -> None:
    if os.path.exists(f'cache/{game_name}.yml'):
        revas_scrapper.smart_scrap_xlsx()
    else:
        if not os.path.exists('cache'):
            os.mkdir('cache')

        revas_scrapper.scrap_xlsxs()

def setup():
    '''Starts the RevasBot
    '''
    clear_xlsx()

    user_name, password, last_game_name = RevasCache.config_loader()

    revas_selenium = RevasSelenium(user_name, password)
    revas_selenium.login()

    downloads_valid = init_dirs(last_game_name != revas_selenium.game_name)

    revas_scrapper = RevasScrapper(revas_selenium)
    revas_shopper = RevasShopper(revas_selenium.execute_script)

    ########
    # You can skip download now!
    scrap_data = input('Do you want to download data from Revas (you can skip if you already downloaded them)? [Y/n]: ')
    if scrap_data not in { 'n', 'N' }:  # 'Y' or 'y' or ''
        revas_selenium.get_schedule()
        revas_scrapper.scrap_finance_bank()
        revas_scrapper.scrap_scores()
        revas_scrapper.scrap_products()

        if not downloads_valid:
            init_scrapper(revas_scrapper, revas_selenium.game_name)
    ########

    ########
    # Used to buy resources
    buy_resources = input('Do you want to buy resources from a CSV file? [Y/n]: ')
    if buy_resources not in { 'n', 'N' }:  # 'Y' or 'y' or ''
        # revas_shopper.buy_resources([{ 'id': '244', 'amount': '1' }])
        revas_shopper.buy_resources_from_file(revas_selenium.game_name)
    ########

    revas_selenium.quit()
