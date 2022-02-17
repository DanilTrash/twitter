import sqlite3
from random import choice
from time import sleep
from typing import NoReturn

import requests
from loguru import logger

from twitter_spam.browser import Browser
from twitter_spam.data import GeneratedAccount, Account
from twitter_spam.services import OnlineSimService





class Registration:

    def __init__(self, page_id: str = None):
        self.db_path = f'../data_{page_id}.sqlite'

    def generate_accounts(self, amount: int = 1) -> Account:
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
        service = OnlineSimService('a518d7a9d5ea34b9d72aab65f059d6c3')
        with sqlite3.connect(self.db_path) as con:
            multilogin_ids = con.execute('select multilogin_id from data where username is NULL').fetchall()
        generated_accounts = self.generate_accounts(len(multilogin_ids))
        for multilogin_id in multilogin_ids:
            tzid = service.get_phone('twitter', 380)
            if tzid.get('response') == 'WARNING_LOW_BALANCE':
                print(tzid)
                sleep(10)
                continue
            gen_account = next(generated_accounts)
            print(gen_account)
            phone_number = service.get_operation(tzid.get('tzid'))
            ##################

            ##################
            browser = Browser(multilogin_id[0])
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
                    result_data = (gen_account.username, gen_account.password, phone_number['number'], *multilogin_id)
                    self.execute(
                        'update data set username = ?, password = ?, phone = ? where multilogin_id = ?',
                        result_data
                    )
            except Exception as error:
                logger.exception(error)
            finally:
                del browser
            ########################


if __name__ == '__main__':
    registration = Registration('635278386')
    registration.create_db()
    while True:
        registration()
