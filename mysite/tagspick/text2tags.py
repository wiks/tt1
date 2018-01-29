# -*- coding: utf-8 -*-

import nltk
import operator
import logging
logger = logging.getLogger('myproject.custom')


class MyTags:
    """
    narzędziałki związane z zamianą textu (np treści strony WEB) na tagi, wraz z ich policzeniem NLTK)
    oraz wyszukaniem w nich konkretnych KEYsów i wypluciu wszystkiego ładnie dla zobrazowania WEBowego
    """

    def __init__(self):

        pass

    @staticmethod
    def text2tags(text_to_tags_and_hits):
        """
        analizuj text na tagi, sortuj wynik według ilości wystąpień
        :param text_to_tags_and_hits:
        :return:
        """
        tokens = [t for t in text_to_tags_and_hits.split()]
        new_tokens = []
        for token in tokens:
            ntoken = unicode(token.lower())  #.replace(',', '').replace('.', '').replace(':', ''))
            new_tokens.append(ntoken)
        freq = nltk.FreqDist(new_tokens)
        # logger.debug(u'-------> %s', freq)
        # -------> <FreqDist with 1549 samples and 2182 outcomes>
        sorted_x = sorted(freq.items(), key=operator.itemgetter(1), reverse=True)
        # logger.debug(u'-------> %s', sorted_x)
        # -------> [(u'na', 41), (u'=', 36), (u'w', 33), (u'z', 33), (u'nie', 25), (u'pogoda', 22), (u'i', 21), ...
        return sorted_x

    def find_and_count_tags_in_content(self, text_to_analise, keywords):
        """
        wyszukaj podane tagi w treści, zlicz ilość wystąpień i analizuj
        utwórz: listę z posortowanymi tagami i ilością ich wystąpień w treści strony
        oraz string-unicode - pozostałe TAGi które nie występują w treści strony
        :param text_to_analise:
        :param keywords:
        :return:
        # output_list -------> [(u'pogoda', 22), (u'gry', 6), (u'kobieta', 3), (u'sport', 3), ...] ,
        # remain -------> portal, hub, www, tematyczny, horyzontalny, wertykalny, wyszukiwarka, katalog, internet,
        # bezpłatne, darmowe, konta, e-mail, strony, czat, wirtualne, kartki, wirtualna, reklama, marketing, informacje,
        # wiadomosci, turystyka, komputery, rozrywka, prognoza, program TV, WAP, RMF FM,
        """
        allwords_list = self.text2tags(text_to_analise)
        output_list = []
        remain_list = keywords
        for one in allwords_list:
            if one[0] in keywords:
                output_list.append(one)
                remain_list.remove(one[0])
        remain = u''
        if remain_list:
            for one in remain_list:
                remain += unicode(one) + u', '
        # logger.debug(u'output_list -------> %s , remain -------> %s', output_list, remain)
        return output_list, remain
