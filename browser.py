from time import sleep
from typing import Optional

import requests
from loguru import logger
from selenium.webdriver import Remote
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


class Driver:
    driver = None

    def __init__(self, multilogin_id: str) -> None:
        options = Options()
        options.add_argument('--headless')
        while self.driver is None:
            url = 'http://127.0.0.1:35000/api/v1/profile/start'
            params = {'automation': 'true', 'profileId': multilogin_id}
            resp = requests.get(url, params=params).json()
            if resp['status'] == 'OK':
                value = resp['value']
                self.driver = Remote(command_executor=value, options=options)
            else:
                logger.error('{} {}'.format(resp['status'], resp['message']))
                print('waiting for 30')
                sleep(10)

    def wait_for_element_to_click(self, xpath, timeout: int = 10) -> Optional[WebElement]:
        element = WebDriverWait(self.driver, timeout).until(
            EC.element_to_be_clickable((By.XPATH, xpath))
        )
        return element
