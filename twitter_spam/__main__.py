import sqlite3
from random import choice
from time import sleep

import requests
from loguru import logger
from selenium.webdriver import Remote
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from twitter_spam.services import OnlineSimService
from twitter_spam.data import GeneratedAccount, Account


class Browser:
    driver = None

    def __init__(self, multilogin_id: str):
        while self.driver is None:
            mla_url = 'http://127.0.0.1:35000/api/v1/profile/start?automation=true&profileId=' + multilogin_id
            resp = requests.get(mla_url).json()
            if resp['status'] == 'OK':
                value = resp['value']
                self.driver = Remote(command_executor=value, desired_capabilities={'acceptSslCerts': True})
            else:
                logger.error('profile status: {} {}'.format(resp['status'], resp['message']))
                sleep(4)

    def reg_page(self):
        url = 'https://twitter.com/i/flow/signup'
        self.driver.get(url)
        return

    def fill_input_fields(self, account: Account, phone: str):
        name_xpath = '//input[@name="name"]'
        phone_xpath = '//input[@name="phone_number"]'
        name_el = WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((By.XPATH, name_xpath)))
        phone_el = WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((By.XPATH, phone_xpath)))
        name_el.send_keys(account.first_name)
        phone_el.send_keys(phone)
        month_xpath = f'//*[@id="SELECTOR_1"]/option[@value="{str(choice(range(1, 13)))}"]'
        day_xpath = f'//*[@id="SELECTOR_2"]/option[@value="{str(choice(range(1, 30)))}"]'
        year_xpath = f'//*[@id="SELECTOR_3"]/option[@value="{str(choice(range(1997, 2002)))}"]'
        db_xpaths = [month_xpath, day_xpath, year_xpath]
        for selector in db_xpaths:
            selected_el = WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((By.XPATH, selector)))
            selected_el.click()
        submitbtn_xpath = '//*[@id="layers"]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[2]/div'
        sumbit_btn_el = WebDriverWait(self.driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, submitbtn_xpath)))
        sumbit_btn_el.click()
        return True

    def next_page(self):
        next_2_button_xpath = '//*/div[2]/div[2]/div[2]/div'
        element = WebDriverWait(self.driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, next_2_button_xpath))
        )
        element.click()

    def third_page(self):
        pass

    def __del__(self):
        self.driver.quit()


def add_proxy(con):
    for proxy in open('../proxies.txt').read().splitlines():
        split_ = (':'.join(proxy.split(':')[:2]),)
        con.execute('insert into data (proxy) values (?)', split_)
        con.commit()


def create_table(con):
    query = '''
    create table if not exists data (
        id integer primary key,
        multilogin_id text,
        proxy text,
        phone text,
        username text,
        password text
    )'''
    con.execute(query)
    con.commit()


class Registration:
    def __init__(self):
        page_id = '103266452'
        con = sqlite3.connect(f'../data_{page_id}.sqlite')
        # create_table(con)
        # add_proxy(con)
        multilogin_ids = con.execute('select multilogin_id from data where username is NULL')
        service = OnlineSimService('a518d7a9d5ea34b9d72aab65f059d6c3')
        for multilogin_id in multilogin_ids:

            gen_account = GeneratedAccount()
            print(gen_account)

            browser = Browser(multilogin_id[0])
            tzid = service.get_phone('twitter', 380)['tzid']
            phone_number = service.get_operation(tzid)['number']
            browser.reg_page()
            browser.fill_input_fields(account=gen_account, phone=phone_number)
            browser.next_page()
            for _ in range(15):
                code = service.get_operation(tzid)
                print(code)
                sleep(1)
            del browser


if __name__ == '__main__':
    Registration()
