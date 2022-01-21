import os
from time import sleep
from itertools import cycle
from random import choice

from onlinesim_api import OnlineSim
from sms_man_api import SmsMan
from data import Data
from browser import Browser, TwitterRegistration, TwitterSpam
from logger import logger


LOG = logger('client')


class Client:
    def __init__(self):
        LOG.info('Client')
        self.data = Data()
        self.email = cycle(self.data('email').dropna())
        self.password = cycle(self.data('password').dropna())
        self.message = cycle(self.data('message').dropna())
        self.proxy = cycle(self.data('message').dropna())

    @staticmethod
    def random_photo():
        images_dir = r'C:\Users\KIEV-COP-4\Desktop\images'
        photo_path = fr'{images_dir}\{choice(os.listdir(images_dir))}'
        LOG.info(photo_path)
        return photo_path

    def reg_twitter(self):
        LOG.info('reg_twitter')
        service = SmsMan(1, 'tw')
        # service = OnlineSim('380', 'twitter')
        name = next(self.email)
        number = service.get_number()
        with TwitterRegistration() as registration:
            if registration.first_step(number, name):
                registration.second_step()
                registration.third_step()
                sms_code = None
                for _ in range(20):
                    req = service.get_sms().json()
                    sms_code = req.get('sms_code', None)
                registration.four_step(sms_code)
                return

    def spam(self):
        LOG.info('spam')
        with TwitterSpam(r'C:\Users\KIEV-COP-4\AppData\Local\Google\Chrome\User Data', 'Default') as browser:
            browser.spam(next(self.message), self.random_photo())


def main(func='reg'):
    amount = 1
    client = Client()
    while amount > 0:
        if func == 'reg':
            if client.reg_twitter():
                amount -= 1
        if func == 'spam':
            if client.spam():
                amount -= 1


if __name__ == '__main__':
    main()
