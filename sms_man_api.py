import json
from time import sleep

import requests

from logger import logger


LOG = logger('sms_man')
URL = 'http://api.sms-man.ru/control'


class SmsMan:
    smsman_token = '7jum0G6_tqXLCIZoAbMo8luIh6HW2IgQ'
    request_id = None

    def __init__(self, country_id, application_id):
        self.country_id = country_id
        self.application_id = application_id

    # def countries(self):
    #     data = {
    #         '$api_key': smsman_token,
    #     }
    #     return requests.get(f'http://api.sms-man.ru/stubs/handler_api.php?action=getCountries', data=data)

    def get_balance(self):
        result = requests.get(f'{URL}/get-balance?token={self.smsman_token}')
        LOG.info(result.content)
        return result

    def get_limits(self):
        result = requests.get(
            f'http://api.sms-man.ru/stubs/handler_api.php?action=getPrices&api_key={self.smsman_token}'
            f'&country={self.country_id}')
        LOG.info(result.content)
        return result

    def get_number(self) -> str:
        req = requests.get(
            f'http://api.sms-man.ru/stubs/handler_api.php?action=getNumber&'
            f'api_key={self.smsman_token}&'
            f'service={self.application_id}&'
            f'country={self.country_id}'
        )
        LOG.info(req.content)
        _, self.request_id, number = req.content.decode().split(':')
        return number

    def get_sms(self):
        req = requests.get(
            f'{URL}/get-sms?token={self.smsman_token}&request_id={self.request_id}'
        )
        LOG.info(req.content)
        return req

    def post_status(self, status):
        result = requests.get(
            f'{URL}/set-status?token={self.smsman_token}&request_id={self.request_id}&status={status}'
        )
        LOG.info(result.content)
        return result

    def get_countries(self):
        result = requests.get(
            f'http://api.sms-man.ru/stubs/handler_api.php?action=getCountries&api_key={self.smsman_token}')
        LOG.info(result.content)
        return result

    def get_applications(self):
        result = requests.get(f'{URL}/applications?token={self.smsman_token}')
        LOG.info(result.content)
        return result


if __name__ == '__main__':
    smsman = SmsMan(1, 'tw')
    print(smsman.get_limits().json().get('tw'))
