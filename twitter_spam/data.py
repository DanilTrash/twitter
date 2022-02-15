import string
from random import choice

import pandas as dp
import sqlite3

import pandas as pd
from faker import Faker


class GeneratedAccount:
    username: str
    password: str
    first_name: str

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.first_name = Faker('ar_AA').first_name_female().lower()
        self.password = self.generate_password()
        self.username = self.generate_username()

    def __repr__(self) -> str:
        return str(self)

    def __str__(self) -> str:
        return '\t'.join([self.username, self.password, self.first_name])

    def generate_password(self) -> str:
        value = ''.join([choice(string.digits + string.ascii_letters) for _ in range(12)])
        return value

    def generate_username(self) -> str:
        while True:
            key_word = choice(open(r'..\key_words.txt').read().splitlines())
            rnd_digits = str(choice(range(100)))
            rnd_char = ''.join([choice(string.ascii_lowercase) for _ in range(2)])
            first_name_female = Faker().first_name_female().lower()
            random_data = [key_word, first_name_female+rnd_digits]
            result = '_'.join(random_data)
            if len(result) < 15:
                return result


class GoogleSheetsUrl:

    def __init__(self, table_id: str, page_id: str):
        self.db_url = f'https://docs.google.com/spreadsheets/d/{table_id}/export?format=csv&id={table_id}&gid={page_id}'

    def __repr__(self) -> str:
        return self.__str__()

    def __str__(self):
        return self.db_url
