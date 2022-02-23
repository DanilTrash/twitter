import time
import psycopg2

from data import GeneratedFacebook
from services import OnlineSimService


class Registration:

    def __init__(self, table_name: str):
        # self.table = table_name
        # self.conn = psycopg2.connect(host='192.168.140.222', user='postgres', dbname='facebook')
        # self.curr = self.conn.cursor()
        self()

    def wait_code(self, service, tzid):
        while True:
            phone = service.get_operation(tzid['tzid'])
            print(phone)
            time.sleep(5)

    def __call__(self):
        generated_account = GeneratedFacebook()
        print(generated_account)
        service = OnlineSimService('a518d7a9d5ea34b9d72aab65f059d6c3', '45.135.176.221:49111')
        tzid = service.get_phone('facebook', 7)
        print(tzid)
        if tzid:
            self.wait_code(service, tzid)


def facebook():
    Registration('1333968754')


if __name__ == '__main__':
    facebook()
