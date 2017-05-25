#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2017 Rafi Kurnia Putra
# Licensed under the MIT - https://opensource.org/licenses/MIT

"""
scrap - Created by Rafi Kurnia Putra <rafi.kurnia.putra@gmail.com> on 23/05/2017
"""

import re
import time

from bs4 import BeautifulSoup
from selenium import webdriver

import conf


class Scrap(object):
    """
    Scrap facebook user's posts and comments
    """

    def __init__(self):
        self.driver = webdriver.Chrome("/mnt/Data/Ubuntu/Downloads/chromedriver")
        self.driver.get("https://www.facebook.com")
        time.sleep(3)

        username = self.driver.find_element_by_id("email")
        username.send_keys(conf.EMAIL)
        time.sleep(2)

        password = self.driver.find_element_by_id("pass")
        password.send_keys(conf.PASSWORDS)
        time.sleep(2)

        login = self.driver.find_element_by_id("loginbutton")
        login.click()
        time.sleep(5)

    def scrap(self, facebook_user_url):
        """
        Start scrapping on the user page
        :return: list of contents
        """

        final_url = "https://m.facebook.com/" + facebook_user_url
        self.driver.get(final_url)
        time.sleep(3)

        last_height = self.driver.execute_script("return document.body.scrollHeight")
        while True:
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(5)
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

        time.sleep(5)
        contents = self.driver.page_source
        final_contents = BeautifulSoup(contents, "html.parser")

        # posts_comments = filter(lambda x: "\"id\":\"tlFeed\"" in x, final_contents.prettify().splitlines())[0]
        # cleaned = posts_comments \
        #     .replace("\\\\\\/", "/") \
        #     .replace("\\/", "/") \
        #     .replace("\\\"", "\"") \
        #     .replace("\\u003C", "<") \
        #     .replace("&amp;", "&") \
        #     .replace("&quot;", "\"") \
        #     .replace("&#123;", "{") \
        #     .replace("&#125;", "}") \
        #     .replace("\\u0025", "%") \
        #     .replace("&gt;", ">")

        # soup = BeautifulSoup(cleaned, "html.parser")
        all_href = final_contents.find_all('a', href=True)
        html = map(lambda x: str(x).replace("&amp;", "&"), all_href)
        user_data = filter(lambda x: len(re.findall(r"<a href=\"/(?:story|photo)(.*?)>", x)) > 0, html)
        permalink = filter(lambda x: len(re.findall(r"<abbr>(.*?)</abbr>", x)) > 0, user_data)
        url_only = map(lambda x: "https://m.facebook.com" + re.findall(r"\"(.*?)\"", x)[0].replace("\"", ""), permalink)

        new0 = list(enumerate(url_only))
        new1 = map(lambda x: (x[0], x[1].split("&_ft_=")), new0)
        new2 = [(x[0], x[1][1]) for x in new1]

        import pandas
        df = pandas.DataFrame(data=new2, columns=['index', 'keys']).groupby('keys').agg({'index': 'min'})

        selected_url = sorted([item for sublist in df.values.tolist() for item in sublist])

        final_url = [item[1] for item in new0 if item[0] in selected_url]

        return final_contents, final_url, self.driver

    # get a title from each post
    # title = driver.find_element_by_xpath("//div[contains(@class, '_5rgt _5nk5')]").text

    # get the comments from each post
    # b = driver.find_elements_by_xpath("//div[contains(@class, '_14ye')]")
    # comments = [item.text for item in b]

    # get a title of life events
    # events = driver.find_element_by_xpath("//div[contains(@class, '_52je _52jb _52jj _5isp')]").text

    # if event or title not found it will raise NoSuchElementException


