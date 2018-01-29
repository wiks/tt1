# -*- coding: utf-8 -*-
import os
import sys
from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.http import HttpResponse
import requests
import urllib
import json

import myurlsy
import text2tags
import misc

import logging
logger = logging.getLogger('myproject.custom')


def index(request):
    """
    strona główna, opis i linki do dwóch rozwiązań
    :param request:
    :return:
    """
    return render(request, 'index.html', locals())


def index0(request):
    """
    generuje stronkę dla zwykłego BUTTONem formularza
    :param request:
    :return:
    """
    requirements = misc.req_as_dict()
    inpurl = request.POST.get("url", None)
    url_get_base = request.build_absolute_uri(reverse('testurl'))
    button_label = u'analizuj to szybciutko!'
    if inpurl:
        data = {'url': inpurl}
        url_get = url_get_base + '?' + urllib.urlencode(data)
        logger.debug(u'ask: %s', url_get)
        response = requests.get(url_get)
        content = json.loads(response.content)
        if content:
            logger.debug(u'answer: %s', response.content)
            url_checked = content['url_checked']
            mismath_url = content['mismath_url']
            len_keywords = content['len_keywords']
            output_list = content['output_list']
            remain = content['remain']
        else:
            logger.debug(u'answer: NONE')
    return render(request, 'index0.html', locals())


def indexa(request):
    """
    generuję stronkę dla Angular'a
    :param request:
    :return:
    """
    requirements = misc.req_as_dict()
    requirements.append("Angular==1.6.4")
    testurl = request.build_absolute_uri(reverse('testurl'))
    url_get_base = request.build_absolute_uri(reverse('testurl'))
    # logger.debug(u'testurl ------> %s', testurl)
    return render(request, 'indexa.html', locals())


def testurl(request):
    """
    odpowiadacz dla zwykłego requesta i dla Angular'a
    http://localhost:8000/testurl?url=interia.pl
    http://tt1/testurl?url=interia.pl
    :param request:
    :return:
    {
    "len_keywords": 39, <-- ilość znalezionych w nim TAGów
    "url_checked": "http://interia.pl", <-- adres dopasowany i analizowany
    "output_list": <-- występujące w treści tagi i ilości ich wystąpień
    [["pogoda", 22], ["gry", 6], ["kobieta", 3], ["sport", 3],
    ["biznes", 3], ["encyklopedia", 1], ["poczta", 1], ["czateria", 1], ["internet", 1], ["fm", 1], ["motoryzacja", 1],
    ["informacje", 1]]
    "remain": <-- jako string - pozostałe tagi z KEYWORDS, rozdzielone przecinkami
    "portal, hub, www, tematyczny, horyzontalny, wertykalny, wyszukiwarka, katalog,
    bezp\u0142atne, darmowe, konta, e-mail, strony, czat, wirtualne, kartki, wirtualna, reklama, marketing, wiadomosci,
    turystyka, komputery, rozrywka, prognoza, program TV, WAP, RMF FM, ",
    "mismath_url": true, <-- gdy url sprawdzany różni się od tego wpisanego
    }
    """
    inpurl = request.POST.get('url', '')
    if not inpurl:
        inpurl = request.GET.get('url', '')
    logger.debug(inpurl)
    retd = {}  # pre-output
    murl = myurlsy.MyUrls()
    url_checked = murl.find_first_exists_url(inpurl)
    if url_checked:
        t2t = text2tags.MyTags()
        mismath_url = url_checked != inpurl
        content_page, \
        keywords = murl.get_keywords_from_meta_tags(url_checked)
        # logger.debug(u'--> keywords: %s', keywords)
        count_keywords = 0
        if keywords:
            count_keywords = len(keywords)
        output_list, \
        remain_key_ustring = t2t.find_and_count_tags_in_content(content_page,
                                                                keywords)
        retd = {
            'url_checked': url_checked,
            'mismath_url': mismath_url,
            'len_keywords': count_keywords,
            'output_list': output_list,
            'remain': remain_key_ustring,
        }
    ret = json.dumps(retd)
    logger.debug('==DICT-for-RESP==========> %s', ret)
    return HttpResponse(ret)


def page_problem(request):

    # main_url = u'http://tt1'
    main_url = request.build_absolute_uri(reverse('main'))
    # logger.debug(u'main_url %s', main_url)
    return render(request, 'pproblem.html', locals())
