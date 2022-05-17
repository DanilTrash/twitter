from worker import Twitter


class Spam:
    def __init__(self, account: dict):
        self.account_data = account


def main():
    account = {
        'username': 'NJohnson3382',
        'password': 'NR4QKDG44p0z',
        'phone': '380953953573'
    }
    spam = Spam(account)


if __name__ == '__main__':
    main()
