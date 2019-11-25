#!/usr/bin/python3.6
# -*- coding: UTF-8 -*
from __future__ import unicode_literals

import logging
import os

import time

from urllib.parse import urlparse

import pdfkit
import requests

html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
</head>
<body>
{content}
</body>
</html>
"""

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/70.0.3538.110 Safari/537.36 "
}

options = {
    'page-size': 'Letter',
    'margin-top': '0.75in',
    'margin-right': '0.75in',
    'margin-bottom': '0.75in',
    'margin-left': '0.75in',
    'encoding': "UTF-8",
    'custom-header': [
        ('Accept-Encoding', 'gzip')
    ],
    'cookie': [
        ('cookie-name1', 'cookie-value1'),
        ('cookie-name2', 'cookie-value2'),
    ],
    'outline-depth': 10,
}


class Crawler(object):
    """
    爬虫基类，所有爬虫都应该继承此类
    """
    name = None

    def __init__(self, name, start_url, out_path, del_html=False):
        """
        初始化
        :param name: 将要被保存为PDF的文件名称
        :param start_url: 爬虫入口URL
        """
        self.del_html = del_html
        self.name = name
        self.out_path = out_path
        self.start_url = start_url
        self.domain = '{uri.scheme}://{uri.netloc}'.format(uri=urlparse(self.start_url))

    @staticmethod
    def request(url, **kwargs):
        """
        网络请求,返回response对象
        :return:
        """
        response = requests.get(url=url, headers=headers, **kwargs)
        return response

    def parse_menu(self, response):
        """
        从response中解析出所有目录的URL链接
        """
        raise NotImplementedError

    def parse_body(self, response):
        """
        解析正文,由子类实现
        :param response: 爬虫返回的response对象
        :return: 返回经过处理的html正文文本
        """
        raise NotImplementedError

    def run(self):
        start = time.time()
        items = []
        out_dir = "/".join([self.out_path, self.name])
        html_path = "/".join([out_dir, "html"])
        if not os.path.exists(html_path):
            os.makedirs(html_path)
        for index, url in enumerate(self.parse_menu(self.request(self.start_url))):
            html = self.parse_body(self.request(url))
            f_name = "/".join([html_path, str(index) + ".html"])
            with open(f_name, 'wb') as f:
                f.write(html)
                f.flush()
            items.append(f_name)

        try:
            pdfkit.from_file(items, out_dir + "/" + self.name + ".pdf", options=options)
        except:
            logging.error("转PDF错误!", exc_info=True)
        if self.del_html:
            for html in items:
                os.remove(html)
        total_time = time.time() - start
        print(u"总共耗时：%f 秒" % total_time)
