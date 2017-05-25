#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2017 Rafi Kurnia Putra
# Licensed under the MIT - https://opensource.org/licenses/MIT

"""
Package scrap - Created by Rafi Kurnia Putra <rafi.kurnia.putra@gmail.com> on 23/05/2017
"""

import json
import re
import time

from bs4 import BeautifulSoup
from pandas import DataFrame
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import Chrome

import conf  # contains email and password for a facebook account


class Scraper(object):
    """
    Scrap facebook user's posts and life events with comments
    
    usage : Scraper.scrap(facebook_user_url)
    example : Scraper.scrap("rafikurniasanusi")
    """

    def __init__(self):
        """
        Initiate webdriver and login into your facebook account
        """

        self.driver = Chrome(conf.WEBDRIVER)
        self.driver.get("https://www.facebook.com")
        time.sleep(3)  # wait for the page is properly opened

        self.driver.find_element_by_id("email").send_keys(conf.EMAIL)
        self.driver.find_element_by_id("pass").send_keys(conf.PASSWORDS)
        self.driver.find_element_by_id("loginbutton").click()
        time.sleep(5)  # wait for the page is properly opened

    @classmethod
    def scrap(cls, facebook_user_url):
        """
        Scrap facebook user's posts and life events with comments
        
        :param facebook_user_url: user's profile url (example: "rafikurniasanusi") 
        :return: user's posts since his/her facebook profile was created in json format 
        """

        this = cls()  # create an instance of class

        final_url = "https://m.facebook.com/" + facebook_user_url  # mobile page is simpler than desktop page
        this.driver.get(final_url)  # create request to user's facebook profile page
        time.sleep(5)  # wait for the page is properly opened

        user_name = this.driver.title  # get user's full name

        # scroll down the page until the beginning of time when user's facebook account was created
        last_height = this.driver.execute_script("return document.body.scrollHeight")  # get current page's height
        while True:
            this.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")  # scroll down
            time.sleep(5)  # wait for the page is properly loaded

            new_height = this.driver.execute_script("return document.body.scrollHeight")  # update current page's height
            if new_height == last_height:  # stopping condition, stop when the page's height was not changed
                break
            else:
                last_height = new_height  # update value

        contents = this.driver.page_source  # get page's html data

        final_contents = BeautifulSoup(contents, "html.parser")  # format the data
        all_href = final_contents.find_all('a', href=True)  # find link to each post
        html = map(lambda html_data: str(html_data).replace("&amp;", "&"), all_href)  # change ampersand character
        user_data = filter(lambda s: len(re.findall(r"<a href=\"/(?:story|photo)(.*?)>", s)) > 0, html)  # story & photo
        permalink = filter(lambda link: len(re.findall(r"<abbr>(.*?)</abbr>", link)) > 0, user_data)  # contains date
        url_only = map(lambda u: "https://m.facebook.com" + re.findall(r"\"(.*?)\"", u)[0].replace("\"", ""), permalink)

        url_with_index = list(enumerate(url_only))  # labeling each url wih index
        temp = map(lambda x: (x[0], x[1].split("&_ft_=")), url_with_index)  # split data from user id
        data = [(element[0], element[1][1]) for element in temp]  # select index and data only
        df = DataFrame(data=data, columns=["index", "keys"]).groupby("keys").agg({"index": "min"})  # remove duplicate

        selected_url = sorted([item for sublist in df.values.tolist() for item in sublist])  # duplicate free url
        final_url = [item[1] for item in url_with_index if item[0] in selected_url]  # remove index

        # open each link to the post and capture posts and life events with the comments
        posts = []  # empty container for user's posts
        for url in final_url:
            this.driver.get(url)  # open the post
            time.sleep(5)  # wait for the page is properly opened

            # get comments
            comments_element = this.driver.find_elements_by_xpath("//div[contains(@class, '_14ye')]")
            if isinstance(comments_element, list):
                if len(comments_element) > 0:
                    comments = [item.text.encode("utf-8").strip() for item in comments_element]
                else:
                    comments = []
            else:
                comments = []

            # get post or life event
            try:
                # finding post's caption
                caption = this.driver.find_element_by_xpath(
                    "//div[contains(@class, '_5rgt _5nk5')]"
                ).text
            except NoSuchElementException:
                try:
                    # if there was no post caption, find for life event caption
                    caption = this.driver.find_element_by_xpath(
                        "//div[contains(@class, '_52je _52jb _52jj _5isp')]"
                    ).text
                except NoSuchElementException:
                    # the posts did not have a caption
                    caption = ""
            caption = caption.encode("utf-8").strip()  # clean the text

            post = {"caption": caption, "comments": comments}  # change into dictionary
            posts.append(post)  # add to post container

        # save json data to json file
        json_output = {user_name: {"posts": posts}}
        with open(user_name + ".json", "w") as outfile:
            json.dump(json_output, outfile, indent=4)

        # gracefully shutdown the webdriver
        this.driver.close()
        this.driver.quit()

        return json.dumps(json_output, indent=4)
