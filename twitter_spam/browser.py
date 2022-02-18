from random import choice
from time import sleep
from typing import NoReturn

import requests
from loguru import logger
from selenium.webdriver import Remote
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from twitter_spam.data import Account


class Browser:
    driver = None

    def __init__(self, multilogin_id: str):
        while self.driver is None:
            url = 'http://127.0.0.1:35000/api/v1/profile/start'
            params = {'automation': 'true', 'profileId': multilogin_id}
            resp = requests.get(url, params=params).json()
            if resp['status'] == 'OK':
                value = resp['value']
                self.driver = Remote(command_executor=value)
            else:
                logger.error('{} {}'.format(resp['status'], resp['message']))
                print('waiting for 30')
                sleep(10)

    def reg_page(self):
        url = 'https://twitter.com/i/flow/signup'
        self.driver.get(url)
        return

    def wait_for_element_to_click(self, xpath, timeout: int = 5):
        element = WebDriverWait(self.driver, timeout).until(
            EC.element_to_be_clickable((By.XPATH, xpath))
        )
        return element

    def fill_input_fields(self, account: Account, phone: str) -> NoReturn:
        name_xpath = '//input[@name="name"]'
        phone_xpath = '//input[@name="phone_number"]'
        name_el = self.wait_for_element_to_click(name_xpath)
        phone_el = self.wait_for_element_to_click(phone_xpath)
        name_el.send_keys(account.first_name)
        phone_el.send_keys(phone)
        month_xpath = f'//*[@id="SELECTOR_1"]/option[@value="{str(choice(range(1, 13)))}"]'
        day_xpath = f'//*[@id="SELECTOR_2"]/option[@value="{str(choice(range(1, 30)))}"]'
        year_xpath = f'//*[@id="SELECTOR_3"]/option[@value="{str(choice(range(1997, 2002)))}"]'
        db_xpaths = [month_xpath, day_xpath, year_xpath]
        for selector in db_xpaths:
            selected_el = self.wait_for_element_to_click(selector)
            selected_el.click()
        sleep(1)
        submit_btn_xpath = '//*[@id="layers"]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[2]/div'
        sumbit_btn_el = self.wait_for_element_to_click(submit_btn_xpath)
        sumbit_btn_el.click()
        return True

    def second_page(self) -> NoReturn:
        sleep(1)
        next_2_button_xpath = '//*/div[2]/div[2]/div[2]/div'
        element = self.wait_for_element_to_click(next_2_button_xpath)
        element.click()

    def third_page(self):
        sleep(1)
        next_3_botton_xpath = '//div[6]/div'
        element = self.wait_for_element_to_click(next_3_botton_xpath)
        element.click()
        sleep(1)
        submit_phone_xpath = '//*[@id="layers"]/div[3]/div/div/div/div/div/div[2]/div[2]/div[2]/div[1]/div'
        element = self.wait_for_element_to_click(submit_phone_xpath)
        element.click()

    def verification_page(self, code: str) -> NoReturn:
        verification_xpath = '//input[@name="verfication_code"]'
        element = self.wait_for_element_to_click(verification_xpath)
        element.send_keys(code)
        sleep(1)
        submit_btn_xpath = '//div[2]/div[2]/div[2]/div/div'
        element = self.wait_for_element_to_click(submit_btn_xpath)
        element.click()

    def fill_password(self, password: str):
        password_xpath = '//input[@name="password"]'
        element = self.wait_for_element_to_click(password_xpath)
        element.send_keys(password)
        sleep(1)
        submit_btn_xpath = '//div[2]/div[2]/div[2]/div/div/div'
        element = self.wait_for_element_to_click(submit_btn_xpath)
        element.click()

    def skip_photo_input(self):
        sleep(1)
        xpath = '//div[2]/div/div/span'
        element = self.wait_for_element_to_click(xpath)
        element.click()

    def skip_about_input(self):
        sleep(1)
        xpath = '//div[2]/div[2]/div[2]/div/div/span'
        element = self.wait_for_element_to_click(xpath)
        element.click()

    def username_field(self, username: str):
        username_xpath = '//input[@name="username"]'
        element = self.wait_for_element_to_click(username_xpath)
        element.clear()
        element.send_keys(username)
        sleep(1)
        submit_xpath = '//div[2]/div[2]/div[2]/div/div'
        element = self.wait_for_element_to_click(submit_xpath)
        element.click()

    def __del__(self):
        self.driver.close()
