# -*- coding: utf-8 -*-
import scrapy
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

class GetFreeEbookSpider(scrapy.Spider):
    name = "get_free_ebook"
    allowed_domains = ["packetpub.com"]
    start_urls = ['https://www.packtpub.com/packt/offers/free-learning#']

    scraped_items = {}

    def __init__(self, login, password):
        self.login = login
        self.password = password
        self.driver = webdriver.PhantomJS()
        # self.driver.set_window_size(1920, 1080)
        # self.driver = webdriver.Chrome("/usr/local/bin/chromedriver")
        self.driver.implicitly_wait(5)  # seconds



    def parse(self, response):
        self.driver.get(response.url)
        try:
            WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.XPATH,
                                                '//a[contains(@href,\
                                                "/freelearning-claim")]'))
            )

            book_name = self.driver.find_element_by_xpath('//div[contains(@class,\
                                                          "dotd-title")]/h2').text
            self.scraped_items['ebook'] = book_name

            # click to show login / password form
            button = self.driver.find_element_by_xpath('//a[contains(@href, "/freelearning-claim")]')
            button.click()
            url_book = button.get_attribute("href")

            login_form = self.driver.find_element_by_xpath('//div[contains(@id,\
                                                           "login-form")]/div/div/input')
            login_form.send_keys(self.login)
            pass_form = self.driver.find_element_by_xpath('//div[contains(@id,\
                                                           "login-form")]/div[2]/div/input')
            pass_form.send_keys(self.password)
            login_btn = self.driver.find_element_by_xpath('//div[contains(@id,\
                                                           "login-form")]/div[3]/input')
            login_btn.click()

            try:
                WebDriverWait(self.driver, 30).until(
                    EC.presence_of_element_located((By.XPATH,
                                                    '//a[contains(@href,\
                                                    "/account")]'))
                )
                self.driver.get(url_book)

            except TimeoutException:
                pass


        except TimeoutException:
            self.logger.critical("Nao foi possivel carregar a pagina")
            self.driver.close()

        finally:
            self.driver.close()

        yield self.scraped_items
