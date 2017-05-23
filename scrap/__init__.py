#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2017 Rafi Kurnia Putra
# Licensed under the MIT - https://opensource.org/licenses/MIT

"""
scrap - Created by Rafi Kurnia Putra <rafi.kurnia.putra@gmail.com> on 23/05/2017
"""
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent


class Scrap(object):
    """
    Scrap facebook user's posts and comments
    """

    def __init__(self, facebook_user_url):
        self.facebook_user_url = facebook_user_url

    def scrap(self):
        """
        Start scrapping on the user page
        :return: list of contents
        """

        ua = UserAgent()
        header = {'User-Agent': ua.chrome}
        r = requests.get(self.facebook_user_url, headers=header)

        if r.status_code == 200:
            soup = BeautifulSoup(r.content, "html.parser")
            return soup.prettify()[0:1000]
        else:
            return []
