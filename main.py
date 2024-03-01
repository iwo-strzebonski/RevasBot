'''
Bot written in Python 3
To be used with Revas simulations

Uses Selenium 4 and Tensorflow 2

Authors:
 * iwo-strzebonski
 * raphaelsanti-core

Licensed under WTFPL
'''

import revasbot
from revasbot.revas_console import RevasConsole as console

if __name__ == '__main__':
    console.info(revasbot.__author__)
    console.info(revasbot.__version__)
    console.info(revasbot.__license__)
    revasbot.setup()
