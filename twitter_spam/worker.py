import sqlite3
from random import choice
from time import sleep
from typing import NoReturn

from loguru import logger
from selenium.webdriver.common.keys import Keys

from browser import Driver
from data import GeneratedTwitter, Account
from services import OnlineSimService


class Twitter(Driver):
    base_url = 'https://twitter.com'

    def home_page(self) -> NoReturn:
        url = f'{self.base_url}/home'
        self.driver.get(url)

    def reg_page(self) -> NoReturn:
        url = f'{self.base_url}/i/flow/signup'
        self.driver.get(url)

    def fill_input_fields(self, account: Account, phone: str) -> NoReturn:
        name_xpath = '//input[@name="name"]'
        phone_xpath = '//input[@name="phone_number"]'
        reg_button_xpath = '//div/div[5]/div/span'
        try:
            reg_btn_el = self.wait_for_element_to_click(reg_button_xpath)
            reg_btn_el.click()
        except Exception as error:
            logger.error(error)
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
        sleep(3)
        submit_btn_xpath = '//*[@id="layers"]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[2]/div'
        sumbit_btn_el = self.wait_for_element_to_click(submit_btn_xpath)
        sumbit_btn_el.click()
        return True

    def second_page(self) -> NoReturn:
        sleep(1)  # fixme
        next_2_button_xpath = '//*/div[2]/div[2]/div[2]/div'
        element = self.wait_for_element_to_click(next_2_button_xpath)
        element.click()

    def third_page(self) -> NoReturn:
        sleep(1)  # fixme
        next_3_botton_xpath = '//div[6]/div'
        element = self.wait_for_element_to_click(next_3_botton_xpath)
        element.click()
        sleep(1)  # fixme
        submit_phone_xpath = '//*[@id="layers"]/div[3]/div/div/div/div/div/div[2]/div[2]/div[2]/div[1]/div'
        element = self.wait_for_element_to_click(submit_phone_xpath)
        element.click()

    def verification_page(self, code: str) -> NoReturn:
        verification_xpath = '//input[@name="verfication_code"]'
        element = self.wait_for_element_to_click(verification_xpath)
        element.send_keys(code)
        sleep(1)  # fixme
        submit_btn_xpath = '//div[2]/div[2]/div[2]/div/div'
        element = self.wait_for_element_to_click(submit_btn_xpath)
        element.click()

    def fill_password(self, password: str) -> NoReturn:
        password_xpath = '//input[@name="password"]'
        element = self.wait_for_element_to_click(password_xpath)
        element.send_keys(password)
        sleep(1)  # fixme
        submit_btn_xpath = '//div[2]/div[2]/div[2]/div/div/div'
        element = self.wait_for_element_to_click(submit_btn_xpath)
        element.click()

    def skip_photo_input(self) -> NoReturn:
        sleep(1)  # fixme
        xpath = '//div[2]/div/div/span'
        element = self.wait_for_element_to_click(xpath)
        element.click()

    def skip_about_input(self) -> NoReturn:
        sleep(1)  # fixme
        xpath = '//div[2]/div[2]/div[2]/div/div/span'
        element = self.wait_for_element_to_click(xpath)
        element.click()

    def username_field(self, username: str) -> NoReturn:
        username_xpath = '//input[@name="username"]'
        element = self.wait_for_element_to_click(username_xpath)
        element.clear()
        element.send_keys(username)
        sleep(1)  # fixme
        submit_xpath = '//div[2]/div[2]/div[2]/div/div'
        element = self.wait_for_element_to_click(submit_xpath)
        element.click()

    def tweet(self, tweet: str, photo_path: str) -> NoReturn:
        url = 'https://twitter.com/compose/tweet'
        self.driver.get(url)
        self.wait_for_element_to_click('//*/div[@aria-label="Tweet text"]').send_keys(tweet)
        self.wait_for_element_to_click('//*/div[@aria-label="Tweet text"]').send_keys(Keys.ENTER)
        self.wait_for_element_to_click('//*/div[1]/div/div/div/div/div[2]/div[3]/div/div/div[1]/input').send_keys(
            photo_path)
        self.wait_for_element_to_click('//*[@id="layers"]//div/div/span/span[text()="Tweet"]').click()

    def __del__(self):
        self.driver.close()


