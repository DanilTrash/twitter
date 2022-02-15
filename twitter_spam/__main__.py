from faker import Faker
import string
from random import choice
from selenium.webdriver import Chrome


def main():
    faker = Faker()
    for _ in range(1):
        profile = faker.first_name_female().lower()
        print(
            profile + ''.join([choice(string.digits + string.ascii_letters) for _ in range(5)]) + '\t' + ''.join([choice(string.digits + string.ascii_letters) for _ in range(12)])
        )


if __name__ == '__main__':
    main()
