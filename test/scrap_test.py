#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2017 Rafi Kurnia Putra
# Licensed under the MIT - https://opensource.org/licenses/MIT

"""
scrap_test.py - Created by Rafi Kurnia Putra <rafi.kurnia.putra@gmail.com> on 23/05/2017
"""

from __future__ import print_function

from scrap import Scraper


def main():
    """
    Scraper Functional Test
    """

    json_output = Scraper.scrap("bentar.dwika")
    print(json_output)


main()
