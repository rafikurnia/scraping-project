#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2017 Rafi Kurnia Putra
# Licensed under the MIT - https://opensource.org/licenses/MIT

"""
scrap - Created by Rafi Kurnia Putra <rafi.kurnia.putra@gmail.com> on 23/05/2017
"""
import mechanize
from bs4 import BeautifulSoup

import conf


class Scrap(object):
    """
    Scrap facebook user's posts and comments
    """

    def __init__(self):
        self.browser = mechanize.Browser()
        self.browser.set_handle_robots(False)

        # f = open("/mnt/Data/Ubuntu/scrapping-project/scrap/cookie_data")
        # cookie = f.read()
        # f.close()

        # while len(cookie) != 0:
        # self.browser.set_cookie(cookie)
        # cookie = cookie[cookie.find(';') + 1:]


        # import pickle
        #
        # with open('../cookie_data_3.pkl', 'rb') as input:
        #     cookie_data = pickle.load(input)

        # import cookielib
        #
        # cookie_data_2 = cookielib.Cookie(version=0, name='c_user', value="1393754456", expires=1503332297, port=None,
        #                                  port_specified=False, domain='.facebook.com', domain_specified=True,
        #                                  domain_initial_dot=True, path='/', path_specified=True, secure=True,
        #                                  discard=False, comment=None,
        #                                  comment_url=None, rest={}, rfc2109=False)

        cookies = mechanize.CookieJar()
        # cookies.set_cookie(cookies)
        #

        self.browser.set_cookiejar(cookies)

        # print self.browser._ua_handlers['_cookies'].cookiejar
        #
        # exit()

        # self.browser.set_simple_cookie()


        self.browser.addheaders = [("User-agent",
                                    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) "
                                    "Chrome/58.0.3029.96 Safari/537.36")]
        self.browser.set_handle_refresh(False)
        self.browser.open("http://www.facebook.com/login.php")

        # print self.browser._ua_handlers['_cookies'].cookiejar[0]
        #
        # exit()


        self.browser.select_form(nr=0)
        self.browser.form['email'] = conf.EMAIL
        self.browser.form['pass'] = conf.PASSWORDS
        self.browser.submit()

    def scrap(self, facebook_user_url):
        """
        Start scrapping on the user page
        :return: list of contents
        """

        final_url = "https://m.facebook.com/" + facebook_user_url

        self.browser.open(final_url)
        response = self.browser.response()
        contents = response.read()

        final_contents = BeautifulSoup(contents, "html.parser")
        return final_contents, final_contents.prettify(), self.browser


        # fil = filter(lambda x: '"id":"tlFeed"' in x, final_contents.prettify().splitlines())
        # fil = fil[0]
        # cl = fil.replace("\\\\\\/", "/").replace("\\/", "/").replace('\\"', '"').replace("\\u003C", '<').replace(
        #     "&amp;", "&").replace("&quot;", '"').replace("&#123;", "{").replace("&#125;", "}").replace("\\u0025", "%")
        # connt = BeautifulSoup(cl, "html.parser")
        # hrf = connt.find_all('a', href=True)
        # ahrf = map(lambda x: str(x).replace("&amp;", "&"), hrf)
        # import re
        # iseng_boy = filter(lambda x: len(re.findall(r'<a href=\"\/story(.*?)>', x)) > 0, ahrf)
        # iseng_man = filter(lambda x: len(re.findall(r'<abbr>(.*?)</abbr>', x)) > 0, iseng_boy)
        # url_only = map(lambda x: 'https://m.facebook.com' + re.findall(r'\"(.*?)\"', x)[0].replace('"', ''), iseng_man)
