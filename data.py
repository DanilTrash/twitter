import string
from dataclasses import dataclass
from random import choice

from faker import Faker

with open(r'C:\Users\KIEV-COP-4\Desktop\twitter\key_words.txt') as file:
    key_words = file.read().splitlines()


class GoogleSheetsUrl:

    def __init__(self, table_id: str, page_id: str):
        self.db_url = f'https://docs.google.com/spreadsheets/d/{table_id}/export?format=csv&id={table_id}&gid={page_id}'

    def __repr__(self) -> str:
        return self.__str__()

    def __str__(self):
        return self.db_url


def generate_password() -> str:
    value = ''.join((choice(string.digits + string.ascii_letters) for _ in range(12)))
    return value


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
    first_name: str
    last_name: str
    password: str
    username: str


class GeneratedTwitter(Account):

    def __init__(self, locale='en_US'):
        self.password: str = generate_password()
        self.first_name: str = Faker(locale).first_name_female().lower()
        self.username: str = generate_username()


class GeneratedFacebook(Account):

    def __init__(self, locale='en_US'):
        self.first_name = Faker(locale).first_name_female()
        self.last_name = Faker(locale).last_name_female()
        self.password = generate_password()

    def __repr__(self):
        return f'GeneratedFacebook(first_name={self.first_name}, last_name={self.last_name}, password={self.password})'
