import os
from time import sleep

from selenium.common.exceptions import TimeoutException
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys

from logger import logger

LOG = logger('browser')


class Browser:
    def __init__(self,
                 user_data_dir: str = None,
                 profile_directory: str = None,
                 proxy: str = None):
        opts = ChromeOptions()
        if proxy:
            opts.add_argument(f'--proxy-server={proxy}')
        if user_data_dir:
            opts.add_argument(f'--user-data-dir={user_data_dir}')
        if profile_directory:
            opts.add_argument(f'--profile-directory={profile_directory}')
        self.driver = Chrome(r'C:\Users\KIEV-COP-4\chromedriver.exe', options=opts)
        LOG.info(opts.arguments)
        self.driver.get('https://twitter.com/home')

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.driver.quit()

    def spam(self, tweet, photo_path):
        LOG.info(tweet)
        url = 'https://twitter.com/compose/tweet'
        self.driver.get(url)
        self.find_element('//*/div[@aria-label="Tweet text"]').send_keys(tweet)
        self.find_element('//*/div[@aria-label="Tweet text"]').send_keys(Keys.ENTER)
        self.find_element('//*/div[1]/div/div/div/div/div[2]/div[3]/div/div/div[1]/input').send_keys(photo_path)
        self.find_element('//*[@id="layers"]//div/div/span/span[text()="Tweet"]').click()
        return True

    def find_element(self, xpath):
        LOG.info(xpath)
        try:
            element = WebDriverWait(self.driver, 10).until(lambda d: self.driver.find_element_by_xpath(xpath),
                                                           f'TimeoutException on finding {xpath}')
            return element
        except TimeoutException as error:
            LOG.error(error)
            return False


class TwitterRegistration(Browser):

    def first_step(self, phone_number: str, name: str):
        name_name = '//*/input[@name="name"]'
        phone_number_name = '//*/input[@name="phone_number"]'
        month_xpath = '//*/select[@id="SELECTOR_1"]'
        day_xpath = '//*/select[@id="SELECTOR_2"]'
        year_xpath = '//*/select[@id="SELECTOR_3"]'
        next_button_xpath = '//*/div[2]/div[@role="button"]'
        URL = 'https://twitter.com/i/flow/signup'
        self.driver.get(URL)
        self.find_element(name_name).send_keys(name)
        self.find_element(phone_number_name).send_keys(phone_number)
        self.find_element(month_xpath).send_keys('декабрь')
        self.find_element(day_xpath).send_keys(1)
        self.find_element(year_xpath).send_keys(1)
        sleep(1)
        self.find_element(next_button_xpath).click()
        return True

    def second_step(self):
        next_2_button_xpath = '//*/div[2]/div[2]/div[2]/div'
        self.find_element(next_2_button_xpath).click()
        return True

    def third_step(self):
        sleep(1)
        next_button = '//*/span/span'
        self.find_element(next_button).click()
        sleep(1)
        confirm_number = '//*/div[2]/div[2]/div[2]/div/span'
        self.find_element(confirm_number).click()
        return True

    def four_step(self, code):  # phone code
        pass

    def fifth_step(self, password):  # password
        pass

    def sixth_step(self):  # photo upload
        pass

    def seventh_step(self):  # about info
        pass

    def eight_step(self):  # wanted categories
        pass

    def final(self):
        pass


class TwitterSpam(Browser):
    URL = 'https://twitter.com/compose/tweet'
