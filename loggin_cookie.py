"""
@Project   : weiboSpider
@Module    : loggin_cookie.py
@Author    : Deco [deco@cubee.com]
@Created   : 7/5/18 11:06 AM
@Desc      : 
"""
import sys
import traceback
import logging

import dryscrape
import requests
from lxml import etree


class NetTour:
    cookie = {"Cookie": "your cookie"}  # 将your cookie替换成自己的cookie

    def __init__(self, user_id):
        self.user_id = user_id
        self.username = ''
        self.dryscrape_session = dryscrape.Session()

    def get_username_static_cookie(self):
        try:
            url = "https://weibo.cn/{}/info".format(self.user_id)
            # url = "https://weibo.cn/%d/info" % self.user_id
            user_agent = ('Mozilla/5.0 (X11; Linux x86_64; rv:12.0) ' 
                          'Gecko/20100101 Firefox/12.0',)
            default_request_headers = {
                'Accept': 'text/html,application/xhtml+xml,application/xml;'
                          'q=0.9,*/*;q=0.8',
                'User-Agent': user_agent,
                'Connection': 'Keep-Alive',
                'Accept-Encoding': 'gzip, deflate',
                'Accept-Language': 'en-US,*',
            }
            html = requests.get(url, cookies=self.cookie,
                                headers=default_request_headers).content
            # session = requests.Session()
            # custom_user_agent = ('Mozilla/5.0 (X11; Linux x86_64; rv:12.0) '
            #                      'Gecko/20100101 Firefox/12.0'),
            # session.headers.update({'User-Agent': custom_user_agent})
            # html = session.get(url, cookies=self.cookie).content
            selector = etree.HTML(html)
            username = selector.xpath("//title/text()")[0]
            self.username = username[:-3]
            print("User name: " + self.username)
        except Exception as e:
            print("Error: ", e)
            traceback.print_exc()

    def get_username_dynamic_cookie(self):
        try:
            url = "https://weibo.cn/{}/info".format(self.user_id)
            user_agent = ('Mozilla/5.0 (X11; Linux x86_64; rv:12.0) ' 
                          'Gecko/20100101 Firefox/12.0',)
            default_request_headers = {
                'Accept': 'text/html,application/xhtml+xml,application/xml;'
                          'q=0.9,*/*;q=0.8',
                'User-Agent': user_agent,
                'Connection': 'Keep-Alive',
                'Accept-Encoding': 'gzip, deflate',
                'Accept-Language': 'en-US,*',
            }

            # start xvfb to support headless scraping
            if 'linux' in sys.platform:
                dryscrape.start_xvfb()

            for key, value in default_request_headers.items():
                # seems to be a bug with how webkit-server handles
                # accept-encoding
                if key.lower() != 'accept-encoding':
                    self.dryscrape_session.set_header(key, value)

            self.dryscrape_session = dryscrape.Session(
                base_url=url)

            cookies = {}
            for cookie_string in self.dryscrape_session.cookies():
                if 'domain=zipru.to' in cookie_string:
                    key, value = cookie_string.split(';')[0].split('=')
                    cookies[key] = value
            self.cookie = cookies

            html = requests.get(url, cookies=self.cookie,
                                headers=default_request_headers).content
            selector = etree.HTML(html)
            username = selector.xpath("//title/text()")[0]
            self.username = username[:-3]
            print("User name: " + self.username)
        except Exception:
            logging.exception("message")
