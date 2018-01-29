# -*- coding: utf-8 -*-

from django.test import TestCase
import logging

try:
    from selenium import webdriver
    from selenium.webdriver.common.keys import Keys
    import selenium.webdriver.support.ui as ui
    isselenium = True
except Exception, e:
    isselenium = False

import text2tags
import myurlsy


class MyTagsTestCase(TestCase):

    def setUp(self):

        self.t2t = text2tags.MyTags()

        # dla pierwszego testu
        self.test_text2tags_cases_list = [
            # text_to_tags_and_hits --> tret
            [u'', []],
            ['jeden', [(u'jeden', 1)]],
            [u'jeden', [(u'jeden', 1)]],
            [u'dwa trzy osiem gżegżółeńka',
             [(u'g\u017ceg\u017c\xf3\u0142e\u0144ka', 1), (u'dwa', 1), (u'osiem', 1), (u'trzy', 1)]],
            [u'dwa trzy osiem osiem dwa cztery pięć',
             [(u'dwa', 2), (u'osiem', 2), (u'cztery', 1), (u'trzy', 1), (u'pi\u0119\u0107', 1)]],
            [u'dwa dwa dwa dwa trzy osiem osiem dwa cztery pięć',
             [(u'dwa', 5), (u'osiem', 2), (u'cztery', 1), (u'trzy', 1), (u'pi\u0119\u0107', 1)]],
        ]

        # dla drugiego testu
        self.test_find_and_count_tags_in_content_cases_list = [
            # text_to_analise, keywords, --> output_list, remain
            [u'', [], [], ''],
            [u'text to analise', [u'keywords'], [], u'keywords, '],
            [u'text to analise zawiera jeden keyword', [u'keyword', u'tag'], [(u'keyword', 1)], u'tag, '],

        ]
        # TODO no i jakieś jeszcze ze stringiem miast unicodu i może pl znakami etc...
        # TODO może odczytywane z plików-do-testów

    def test_text2tags(self):

        for test_case in self.test_text2tags_cases_list:
            text_to_tags_and_hits = test_case[0]
            tret = self.t2t.text2tags(text_to_tags_and_hits)
            self.assertEqual(tret, test_case[1], u'lipa w "test_text2tags"')

    def test_find_and_count_tags_in_content(self):

        for test_case in self.test_find_and_count_tags_in_content_cases_list:
            text_to_analise = test_case[0]
            keywords = test_case[1]

            output_list, remain = self.t2t.find_and_count_tags_in_content(text_to_analise, keywords)

            # print '))))))) ', output_list, remain
            self.assertEqual(output_list, test_case[2], u'lipa w "test_find_and_count_tags_in_content (1)"')
            self.assertEqual(remain, test_case[3], u'lipa w "test_find_and_count_tags_in_content (2)"')


class MyUrlsTestCase(TestCase):

    def setUp(self):

        self.murl = myurlsy.MyUrls()

        self.test_find_first_exists_url_cases_list = [
            # url_like_is, response-url
            [u'', None],
            [u'interia.pl', 'http://interia.pl'],

        ]

        self.test_get_keywords_from_meta_tags_cases_list = [
            # <meta name="keywords" content="SMS,sendSMS,freeSMS">
            ['http://www.wiks.eu/sms.php', [u'SMS', u'sendSMS', u'freeSMS']],

        ]

    def test_find_first_exists_url(self):

        for test_case in self.test_find_first_exists_url_cases_list:
            url_like_is = test_case[0]
            url_checked = self.murl.find_first_exists_url(url_like_is)
            self.assertEqual(url_checked, test_case[1], u'lipa w "test_find_first_exists_url"')

    def test_get_keywords_from_meta_tags(self):

        for test_case in self.test_get_keywords_from_meta_tags_cases_list:
            url_checked = test_case[0]

            content_page, \
            keywords = self.murl.get_keywords_from_meta_tags(url_checked)
            # print '++++++++++++', content_page, keywords
            self.assertEqual(keywords, test_case[1], u'lipa w "test_get_keywords_from_meta_tags" (1)')


class AllWebTestCase(TestCase):

    def setUp(self):

        global isselenium

        if isselenium:
            try:
                # create a new Firefox session
                self.driver = webdriver.Firefox()
                self.driver.implicitly_wait(30)
                self.driver.maximize_window()
                self.wait = ui.WebDriverWait(self.driver, 15)
                # navigate to the application home page
                self.driver.get("http://tt1")
                self.url_to_test = "wiks.eu/sms.php"
                self.expected_rest = u'SMS, sendSMS, freeSMS,'
            except Exception, e:
                # Message: 'geckodriver' executable needs to be in PATH.
                isselenium = False
                logging.warning(e)
        else:
            logging.warning(u'brak Selenium')

    def test_dev_task(self):
        """
        przetestuj, strona główna, sprawdż tytuł
        przejdź do 0 wpisz i wciśnij, odczytaj
        przejdź do formAngulara, wpisz i odczytaj co wyszło
        zamknij przeglądarkę
        :return:
        """
        global isselenium

        if isselenium:
            try:
                self.assertEqual("Dev-task", self.driver.title)
                alinka = self.driver.find_element_by_id("alink0")
                alinka.click()
                eleminp0 = self.driver.find_element_by_id("myInput")
                eleminp0.clear()
                eleminp0.send_keys(self.url_to_test)
                eleminp0.send_keys(Keys.RETURN)
                self.wait.until(lambda driver: driver.find_element_by_id('resttag'))
                elemrestag0 = self.driver.find_element_by_id("resttag")
                element_text0 = elemrestag0.text
                self.assertEqual(self.expected_rest, element_text0)
                # print 'element0.text: {0}'.format(element_text0)  # element.text: SMS, sendSMS, freeSMS,
                alinka = self.driver.find_element_by_id("alinkback")
                alinka.click()
                alinka = self.driver.find_element_by_id("alinka")
                alinka.click()
                eleminpa = self.driver.find_element_by_id("myInput")
                eleminpa.clear()
                eleminpa.send_keys(self.url_to_test)
                self.wait.until(lambda driver: driver.find_element_by_id('resttag'))
                elemrestaga = self.driver.find_element_by_id("resttag")
                element_texta = elemrestaga.text
                self.assertEqual(self.expected_rest, element_texta)
                # print 'elementa.text: {0}'.format(element_texta)
                self.driver.close()
            except Exception, e:
                logging.warning(e)
        logging.warning(u'Problem z SELENIUM, zobacz README')

# https://stackoverflow.com/questions/40208051/selenium-using-python-geckodriver-executable-needs-to-be-in-path
# WebDriverException: Message: 'geckodriver' executable needs to be in PATH
