import sqlite3
from random import choice
from time import sleep
from typing import NoReturn

from loguru import logger
from selenium.webdriver.common.keys import Keys

from browser import Driver
from data import GeneratedAccount, Account
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
        sleep(3)  # fixme
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


class Registration:

    def __init__(self, page_id: str = None):
        self.db_path = f'../data_{page_id}.sqlite'

    @staticmethod
    def generate_accounts(amount: int = 1):
        for _ in range(amount):
            gen_acc = GeneratedAccount()
            yield gen_acc

    def create_db(self):
        query = '''
            create table if not exists data (
                id integer primary key,
                multilogin_id text,
                proxy text,
                phone text,
                username text,
                password text
            )'''
        self.execute(query)

    def execute(self, *args):
        with sqlite3.connect(self.db_path) as con:
            con.execute(*args)
            con.commit()

    def __call__(self, *args, **kwargs):
        service = OnlineSimService('a518d7a9d5ea34b9d72aab65f059d6c3', '45.135.176.221:49111')
        with sqlite3.connect(self.db_path) as con:
            multilogin_ids = con.execute(
                'select multilogin_id from data where username is NULL and multilogin_id is not NULL').fetchall()
        generated_accounts = self.generate_accounts(len(multilogin_ids))
        for multilogin_id in multilogin_ids:
            tzid = service.get_phone('twitter', 212)
            if not tzid:
                print(tzid)
                continue
            if tzid.get('response') == 'WARNING_LOW_BALANCE':
                print(tzid)
                sleep(10)
                continue
            gen_account = next(generated_accounts)
            print(gen_account)
            phone_number = service.get_operation(tzid.get('tzid'))
            ##################

            ##################
            browser = Twitter(multilogin_id[0])
            try:
                browser.reg_page()
                browser.fill_input_fields(account=gen_account, phone=phone_number['number'])
                browser.second_page()
                browser.third_page()
                code = None

                ####################
                c = 0
                while code is None and c < 30:
                    code = service.get_operation(tzid.get('tzid')).get('msg')
                    print(code)
                    sleep(1)
                    c += 1
                ####################

                if code:
                    print(phone_number)
                    browser.verification_page(code)
                    browser.fill_password(gen_account.password)
                    browser.skip_photo_input()
                    browser.skip_about_input()
                    browser.username_field(gen_account.username)
                    browser.driver.refresh()
                    browser.driver.get('https://twitter.com/home')
                    result_data = (gen_account.username, gen_account.password, phone_number['number'], *multilogin_id)
                    self.execute(
                        'update data set username = ?, password = ?, phone = ? where multilogin_id = ?',
                        result_data
                    )
                    sleep(5)
            except Exception as error:
                logger.exception(error)
            finally:
                del browser
                sleep(1)
            ########################


if __name__ == '__main__':
    registration = Registration('1112505379')
    registration.create_db()
    while True:
        registration()
