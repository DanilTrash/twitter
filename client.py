from twitter_spam.spam import Registration


def twitter():
    registration = Registration('1112505379')
    registration.create_db()
    while True:
        registration()


