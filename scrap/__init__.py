#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2017 Rafi Kurnia Putra
# Licensed under the MIT - https://opensource.org/licenses/MIT

"""
scrap - Created by Rafi Kurnia Putra <rafi.kurnia.putra@gmail.com> on 23/05/2017
"""

import urllib

from bs4 import BeautifulSoup


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

        r = urllib.urlopen(self.facebook_user_url).read()
        soup = BeautifulSoup(r)
        return soup.prettify()[0:1000]
