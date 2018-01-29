# -*- coding: utf-8 -*-

from urlparse import urlparse
import urllib2
import bs4
import re
import logging
logger = logging.getLogger('myproject.custom')


class MyUrls:
    """
    narzędziałki związane z adresem URL domyślnym i próbą utworzenia z niego URL
    oraz sprawdzeniem, czy działa
    """

    def __init__(self):

        pass

    @staticmethod
    def _access_input_string_as_url_variants(inpurl):
        """
        ocenia wejściowy string, jako URL, dopasowuje protokuł i ew. WWW,
        zwraca listę wariantów możliwych
        :param inpurl:
        :return:
        """
        url_list_to_check = []
        result = urlparse(inpurl)
        myscheme = result.scheme
        if not myscheme:
            myscheme = [u'', u'http://', u'https://', ]
        if myscheme:
            netloc = inpurl
            if result.netloc:
                netloc = result.netloc + u'' + unicode(result.path)
            if isinstance(myscheme, list):
                for one in myscheme:
                    url_list_to_check.append(unicode(one) + u'' + unicode(netloc))
            else:
                url_list_to_check = [unicode(myscheme) + u'://' + unicode(netloc)]
        return url_list_to_check

    @staticmethod
    def _get_first_from_urls_wariants(url_list_to_check):
        """
        z isty wariantów url, wybiera kolejno, aż napotka pierwszy, który istanieje
        :param url_list_to_check:
        :return:
        """
        url_checked = None
        if url_list_to_check:
            for one in url_list_to_check:
                if not url_checked:
                    try:
                        req = urllib2.Request(one)
                        resp = urllib2.urlopen(req, timeout=2)
                        if resp.code == 200:
                            url_checked = one
                    except Exception, e:
                        # logger.debug(u'errorek przy pobieraniu wariantów [ %s ] : %s', one, e)
                        pass
        return url_checked

    def find_first_exists_url(self, inpurl):
        """
        zmień coś, spróbuj z tego zrobić adres URL
        :param inpurl:
        :return:
        """
        url_list_to_check = self._access_input_string_as_url_variants(inpurl)
        url_checked = self._get_first_from_urls_wariants(url_list_to_check)
        return url_checked

    @staticmethod
    def get_keywords_from_meta_tags(url_checked):
        """
        pod podanym URL pobieram treść i wyszukuję KEYWORDS w HEAD:
        #  <meta name="keywords" content="HTML,CSS,XML,JavaScript">
        :param url_checked:
        :return:
        """
        keywords = []
        content_page = u''
        if url_checked:
            opener = urllib2.build_opener()
            webbrowser_headers = ('User-agent', 'Mozilla/5.0')
            opener.addheaders = [webbrowser_headers]
            respo = opener.open(url_checked)
            page = respo.read()
            soup = bs4.BeautifulSoup(page, "lxml")
            metatags = soup.findAll("meta", attrs={'name':re.compile("^KEYWORDS$", re.I)})
            logger.debug(u'--> metatags: %s', metatags)
            for one in metatags:
                keywords_string = unicode(one.get("content", None))
                keywords += keywords_string.split(',')
            keywords = map(unicode.strip, keywords)
            bd = soup.body.get_text()
            content_page = bd.replace('\n', '').replace('  ', ' ')
        return content_page, keywords
