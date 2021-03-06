import sqlite3
from time import sleep

from loguru import logger

from data import GeneratedTwitter
from services import OnlineSimService
from twitter_spam.worker import Twitter


class Registration:

    def __init__(self, page_id: str = None):
        self.db_path = f'data_{page_id}.sqlite'

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
        for multilogin_id in multilogin_ids:
            tzid = service.get_phone('twitter', 212)
            if not tzid:
                print(tzid)
                continue
            if tzid.get('response') == 'WARNING_LOW_BALANCE':
                print(tzid)
                sleep(10)
                continue
            gen_account = GeneratedTwitter('ar_AA')
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
