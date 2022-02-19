import sys

from selenium.webdriver import Edge, Firefox, Chrome, Safari, Opera
from selenium.webdriver import FirefoxProfile
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.common.exceptions import WebDriverException

from revasbot.revas_console import RevasConsole as console

def get_driver(browser: str = 'edge'):
    '''_summary_

    Args:
        browser (str, optional): _description_. Defaults to 'edge'.

    Returns:
        _type_: _description_
    '''

    driver = None
    caps = None

    if browser == 'firefox':
        caps = DesiredCapabilities().FIREFOX.copy()
    elif browser == 'chrome':
        caps = DesiredCapabilities().CHROME.copy()
    elif browser == 'safari':
        caps = DesiredCapabilities().SAFARI.copy()
    elif browser == 'opera':
        caps = DesiredCapabilities().OPERA.copy()
    else: # defaults to Edge
        caps = DesiredCapabilities().EDGE.copy()

    caps['pageLoadStrategy'] = 'eager'

    if browser == 'firefox':
        ff_prof = FirefoxProfile()

        ff_prof.set_preference(
        'browser.download.manager.showWhenStarting',
        False
        )

        ff_prof.set_preference(
        'browser.helperApps.neverAsk.saveToDisk',
        'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )

        driver = Firefox(firefox_profile=ff_prof, capabilities=caps)
    elif browser == 'chrome':
        driver = Chrome(desired_capabilities=caps)
    elif browser == 'safari':
        driver = Safari(desired_capabilities=caps)
    elif browser == 'opera':
        driver = Opera(desired_capabilities=caps)
    else: # defaults to Edge
        driver = Edge(capabilities=caps)

    driver.set_window_size(800, 600)
    driver.minimize_window()
    # self.driver.maximize_window()

    driver.get('https://gry.revas.pl/')

    return driver

def select_driver():
    browsers = {
        '0': 'Edge',
        '1': 'Firefox',
        '2': 'Chrome',
        '3': 'Safari',
        '4': 'Opera'
    }

    console.header('Select WebDriver:')

    for key, value in browsers.items():
        if key == '0':
            console.ok(f'{key}) {value} [DEFAULT]')
        elif key == '1':
            console.warn(f'{key}) {value} [LEGACY - 4x slower than Edge]')
        else:
            console.error(f'{key}) {value} [UNTESTED]')

    browser = browsers.get(
        console.input('Choose browser engine: '),
        'Edge'
    ).lower()
    
    try:
        driver = get_driver(browser)
    except WebDriverException as e:
        print(e)
        sys.exit()
    else:
        return driver
