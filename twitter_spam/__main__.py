import sqlite3

import requests
from loguru import logger
from selenium.webdriver import Remote

from twitter_spam.data import GeneratedAccount


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


def main_arabic():
    page_id = '103266452'
    con = sqlite3.connect(f'../data_{page_id}.sqlite')
    # query = '''
    # create table if not exists data (
    #     id integer primary key,
    #     multilogin_id text,
    #     proxy text,
    #     phone text,
    #     username text,
    #     password text
    # )'''
    # con.execute(query)
    # con.commit()
    # for proxy in open('../proxies.txt').read().splitlines():
    #     split_ = (':'.join(proxy.split(':')[:2]),)
    #     con.execute('insert into data (proxy) values (?)', split_)
    #     con.commit()
    service = OnlineSimService()
    multilogin_ids = con.execute('select multilogin_id from data where username is NULL')
    for multilogin_id in multilogin_ids:
        gen_account = GeneratedAccount()
        print(gen_account)
        browser = Browser(multilogin_id[0])
        phone_number = service.get_phone()
        browser


if __name__ == '__main__':
    main_arabic()
