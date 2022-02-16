import sqlite3
from time import sleep

import requests
from loguru import logger
from selenium.webdriver import Remote
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from twitter_spam.data import GeneratedAccount, Account


class OnlineSimService:
    api_key = ''

    def get_phone(self, service: str = 'twitter', country_code: str = '971'):
        return None

    def get_message(self, tzid):
        return None


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
        name_el = WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((By.XPATH, name_xpath)))
        name_el.send_keys(account.first_name)

    def registration(self, *args, **kwargs):
        self.reg_page()
        self.fill_input_fields(*args, **kwargs)


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
        create_table(con)
        # add_proxy(con)
        service = OnlineSimService()
        multilogin_ids = con.execute('select multilogin_id from data where username is NULL')
        for multilogin_id in multilogin_ids:
            gen_account = GeneratedAccount()
            print(gen_account)
            browser = Browser(multilogin_id[0])
            phone_number = service.get_phone()
            browser.registration(account=gen_account, phone=phone_number)


if __name__ == '__main__':
    Registration()
