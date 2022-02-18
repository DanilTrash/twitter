from abc import ABC, abstractmethod, abstractproperty
from typing import Optional, List

import requests
from loguru import logger


class Service(ABC):
    api_key = None

    def __init__(self, api_key: str):
        self.api_key = api_key

    @abstractmethod
    def get_phone(self, **kwargs) -> Optional[dict]:
        pass

    @abstractmethod
    def get_all_operations(self, **kwargs) -> Optional[dict]:
        pass

    def get_operation(self, *args, **kwargs) -> Optional[dict]:
        pass

    @abstractproperty
    def get_balance(self) -> Optional[dict]:
        pass


class OnlineSimService(Service):
    name = 'OnlineSimApi'
    api_url = 'https://onlinesim.ru/api/'

    def __init__(self, *args, proxy=None):
        super().__init__(*args)
        self.session = requests.Session()

    @property
    def get_balance(self) -> Optional[dict]:
        return_value = None
        method = '/getBalance.php'
        params = {
            'apikey': self.api_key
        }
        try:
            return_value = self.session.get(self.api_url + method, params=params).json()
        except Exception as error:
            logger.info(self.name + '.balance exception')
            logger.error(error)
        finally:
            return return_value

    def get_all_operations(self) -> Optional[List[dict]]:
        return_value = None
        method = '/getState.php'
        params = {
            'apikey': self.api_key
        }
        try:
            return_value = self.session.get(self.api_url + method, params=params).json()
        except Exception as error:
            logger.info(self.name + '.get_state() exception')
            logger.error(error)
        finally:
            return return_value

    def get_phone(self, service: str, country_code: int) -> Optional[dict]:
        phone_number = None
        method = '/getNum.php'
        params = {
            'apikey': self.api_key,
            'service': service,
            'country': country_code
        }
        try:
            phone_number = self.session.get(self.api_url + method, params=params).json()
        except Exception as error:
            logger.info('OnlineSim.get_phone exception')
            logger.error(error)
        finally:
            return phone_number

    def get_operation(self, tzid: int) -> Optional[dict]:
        result = None
        tzid_ = [x for x in self.get_all_operations() if x['tzid'] == tzid]
        if tzid_:
            result = tzid_[0]
        return result


class SmsManService(Service):
    api_url_v1 = 'https://api.sms-man.ru/stubs/handler_api.php'

    api_url_v2 = 'http://api.sms-man.ru/control'
    name = 'SmsMan'
    last_req = None
    request_id = None

    def get_balance(self) -> Optional[dict]:
        pass

    def get_phone(self, **kwargs) -> Optional[dict]:
        pass

    def get_operation(self, *args, **kwargs) -> Optional[dict]:
        pass

    def get_all_operations(self, **kwargs) -> Optional[dict]:
        pass


class SmsActivateService(Service):
    name = 'SmsActivate'

    def get_balance(self) -> Optional[dict]:
        pass

    def get_all_operations(self, **kwargs) -> Optional[dict]:
        pass

    def get_phone(self, **kwargs) -> Optional[dict]:
        pass


def test_onlinesim_get_all_operations():
    service = OnlineSimService('a518d7a9d5ea34b9d72aab65f059d6c3')
    return service.get_all_operations()


def test_onlinesim_get_balance():
    service = OnlineSimService('a518d7a9d5ea34b9d72aab65f059d6c3')
    return service.get_balance


def test_onlinesim_get_phone():
    service = OnlineSimService('a518d7a9d5ea34b9d72aab65f059d6c3')
    return service.get_phone('twitter', 380)


def test_onlinesim_get_operation(tzid: int):
    service = OnlineSimService('a518d7a9d5ea34b9d72aab65f059d6c3')
    return service.get_operation(tzid)
