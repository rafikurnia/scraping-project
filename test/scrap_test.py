#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2017 Rafi Kurnia Putra
# Licensed under the MIT - https://opensource.org/licenses/MIT

"""
scrap_test - Created by Rafi Kurnia Putra <rafi.kurnia.putra@gmail.com> on 23/05/2017
"""

from __future__ import print_function

from scrap import Scrap

scrapper = Scrap()
output, pretty, browser = scrapper.scrap("profile.php?id=100000132783800")
