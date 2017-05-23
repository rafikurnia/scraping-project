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

        f = open("/mnt/Data/Ubuntu/scrapping-project/scrap/cookie_data")
        cookie = f.read()
        f.close()


        # while len(cookie) != 0:
        # self.browser.set_cookie(cookie)
            # cookie = cookie[cookie.find(';') + 1:]

        cookies = mechanize.CookieJar()
        self.browser.set_cookiejar(cookies)

        self.browser.addheaders = [("User-agent",
                                    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) "
                                    "Chrome/58.0.3029.96 Safari/537.36")]
        self.browser.set_handle_refresh(False)
        self.browser.open("http://www.facebook.com/login.php")
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
