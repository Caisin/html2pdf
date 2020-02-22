#!/usr/bin/python3.6
# -*- coding: UTF-8 -*

import logging
import re

from bs4 import BeautifulSoup

from caisin.Crawler import Crawler, html_template
from caisin.Render import Render


class GitBookCrawler(Crawler):
    """
    GitBook导出的
    """

    def __init__(self, name, start_url, out_path, del_html=False):
        super().__init__(name, start_url, out_path, del_html)
        self.render = Render()

    def request(self, url, **kwargs):
        print(url)
        return self.render.get_html(url)

    def parse_menu(self, response):
        """
        解析目录结构,获取所有URL目录列表
        :param response 爬虫返回的response对象
        :return: url生成器
        """
        soup = BeautifulSoup(response, "html.parser")
        menu_tag = soup.find("ul", class_="summary")
        for a in menu_tag.find_all("a"):
            url = a.get("href")
            if not url.startswith("http"):
                url = "/".join([self.domain, self.path, url])  # 补全为全路径
            yield url

    def parse_body(self, response):
        """
        解析正文
        :param response: 爬虫返回的response对象
        :return: 返回处理后的html文本
        """
        try:
            # print(response)
            soup = BeautifulSoup(response, 'html.parser')
            body = soup.find("section", class_="normal markdown-section")
            # 加入标题, 居中显示
            # try:
            #     title = body.find('h1').get_id()
            # except:
            #     title = body.find('h4').get_id()
            # center_tag = soup.new_tag("center")
            # title_tag = soup.new_tag('h1')
            # title_tag.string = title
            # center_tag.insert(1, title_tag)
            # body.insert(1, center_tag)

            html = str(body)
            # body中的img标签的src相对路径的改成绝对路径
            pattern = "(<img .*? src=\")(.*?)(\")"

            def func(m):
                if not m.group(2).startswith("http"):
                    rtn = "".join([m.group(1), self.domain, self.path, '/', m.group(2), m.group(3)])
                    return rtn.replace("../", "")
                else:
                    return "".join([m.group(1), m.group(2), m.group(3)])

            html = re.compile(pattern).sub(func, html)
            html = html_template.format(content=html, start_url=self.start_url)
            html = html.encode("utf-8")
            return html
        except Exception as e:
            logging.error("解析错误", exc_info=True)


if __name__ == '__main__':
    html_template = """
<!DOCTYPE HTML>
<html lang="zh-hans" >
    <head>
        <meta charset="UTF-8">
        <meta content="text/html; charset=utf-8" http-equiv="Content-Type">
        <meta http-equiv="X-UA-Compatible" content="IE=edge" />
        <meta name="description" content="">
        <meta charset="UTF-8">
        <link rel="stylesheet" href="{start_url}/gitbook/style.css">
        <link rel="stylesheet" href="{start_url}/gitbook/gitbook-plugin-katex/katex.min.css">
        <link rel="stylesheet" href="{start_url}/gitbook/gitbook-plugin-highlight/website.css">
        <link rel="stylesheet" href="{start_url}/gitbook/gitbook-plugin-fontsettings/website.css">
        <meta name="HandheldFriendly" content="true"/>
        <meta name="viewport" content="width=device-width, initial-scale=1, user-scalable=no">
        <meta name="apple-mobile-web-app-capable" content="yes">
        <meta name="apple-mobile-web-app-status-bar-style" content="black">
        <link rel="apple-touch-icon-precomposed" sizes="152x152" href="{start_url}/gitbook/images/apple-touch-icon-precomposed-152.png">
        <link rel="shortcut icon" href="{start_url}/gitbook/images/favicon.ico" type="image/x-icon">
        <style>
            .markdown-section pre>code {
                white-space: pre-wrap;
                word-wrap: break-word;
            }
        </style>
</head>
<body style="font-size: xx-large;padding:50px 10px">
{content}
</body>
</html>
"""
    out_path = "E:/code/Python/html2pdf/out"
    urls = {
        'Go语言圣经（中文版）': 'http://localhost/gitbook',
        # 'Go语言高级编程': 'https://chai2010.cn/advanced-go-programming-book',
        # 'Go2编程指南': 'https://chai2010.cn/go2-book',
        # 'golang': 'https://book.eddycjy.com/golang',
    }
    for item in urls:
        crawler = GitBookCrawler(item, urls[item], out_path)
        # crawler.run()
        crawler.html_to_pdf()
