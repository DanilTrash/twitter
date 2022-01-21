from configparser import ConfigParser
from time import sleep

from onlinesimru import GetUser, GetNumbers
from onlinesimru.Extentions import RequestException
from logger import logger

LOG = logger('online_sim')


class OnlineSim:
    __onlineSim_token = '76d8377e27690ecbe2153174c22104eb'
    tzid = None

    def __init__(self, country, service):
        self.service = service
        self.country = country
        self.sim = GetNumbers(self.__onlineSim_token)
        self.user = GetUser(self.__onlineSim_token)

    def get_balance(self):
        value = self.user.balance()["balance"]
        LOG.info(value)
        return value

    def get_numbers(self):
        value = self.sim.state()
        LOG.info(value)
        return value

    def get_number(self):
        self.tzid = self.sim.get(self.service, self.country)
        value = self.get_state()
        return value

    def get_sms(self):
        value = self.sim.wait_code(self.tzid, 1)
        LOG.info(value)
        return value

    def get_state(self):
        value = self.sim.stateOne(self.tzid)
        LOG.info(value)
        return value

    def tariffs1(self):
        value = self.sim.tariffs()
        LOG.info(value)
        return value


if __name__ == '__main__':
    online_sim = OnlineSim(country='380', service='twitter')
    online_sim.get_number()
