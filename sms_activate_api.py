from configparser import ConfigParser

import requests


class SmsActivate:
    __api_key = '2c7d78A5b57efdc4db82ff46283664AA'
    __base_url = 'https://sms-activate.ru/stubs/handler_api.php'
    request_id = None

    def __init__(self, service, country):
        self.service = service
        self.country = country

    def get_balance(self):
        params = {'api_key': self.__api_key, 'action': 'getBalance'}
        req = requests.get(self.__base_url, params=params)
        return req

    def get_number(self):
        params = {
            'api_key': self.__api_key,
            'action': 'getBalance',
            'service': self.service
        }
        req = requests.get(self.__base_url, params=params)
        return req


def main():
    sms = SmsActivate()
    sms.get_balance()


if __name__ == '__main__':
    main()
