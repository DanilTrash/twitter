import string
from dataclasses import dataclass
from random import choice

from faker import Faker

with open(r'key_words.txt') as file:
    key_words = file.read().splitlines()


class GeneratedData:

    @staticmethod
    def generate_password() -> str:
        value = ''.join((choice(string.digits + string.ascii_letters) for _ in range(12)))
        return value

    @staticmethod
    def generate_username() -> str:
        while True:
            key_word = choice(key_words)
            rnd_digits = ''.join([choice(string.digits) for _ in range(2)])
            # rnd_char = ''.join([choice(string.ascii_lowercase) for _ in range(2)])
            first_name_female = Faker().first_name_female().lower()
            random_data = (key_word, first_name_female)
            result = '_'.join(random_data) + rnd_digits
            if len(result) < 16:
                return result


@dataclass
class Account:
    password: str
    first_name: str
    username: str


class GeneratedAccount(Account):

    def __init__(self):
        self.password: str = GeneratedData().generate_password()
        self.first_name: str = Faker('ar_AA').first_name_female().lower()
        self.username: str = GeneratedData().generate_username()


class GoogleSheetsUrl:

    def __init__(self, table_id: str, page_id: str):
        self.db_url = f'https://docs.google.com/spreadsheets/d/{table_id}/export?format=csv&id={table_id}&gid={page_id}'

    def __repr__(self) -> str:
        return self.__str__()

    def __str__(self):
        return self.db_url
