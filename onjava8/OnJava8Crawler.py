#!/usr/bin/python3.6
# -*- coding: UTF-8 -*

import logging
import re

from bs4 import BeautifulSoup

from caisin.Crawler import Crawler, html_template
from caisin.Render import Render


class OnJava8Crawler(Crawler):
    """
    廖雪峰Python3教程
    """

    def __init__(self, name, start_url, out_path, del_html=False):
        super().__init__(name, start_url, out_path, del_html)
        self.render = Render()
        self.head = ''

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
        self.head = soup.find("head")
        menu_tag = soup.find("div", class_="sidebar-nav")
        for li in menu_tag.find_all("li"):
            url = li.find_all("a")[1].get("href")
            if not url.startswith("http"):
                url = "/".join([self.domain + '/onjava8', url])  # 补全为全路径
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
            body = soup.find("article", id="main", class_="markdown-section")
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
                    rtn = "".join([m.group(1), self.domain, m.group(2), m.group(3)])
                    return rtn
                else:
                    return "".join([m.group(1), m.group(2), m.group(3)])

            html = re.compile(pattern).sub(func, html)
            html = html_template.format(content=html, head=self.head)
            html = html.encode("utf-8")
            return html
        except Exception as e:
            logging.error("解析错误", exc_info=True)


if __name__ == '__main__':
    html_template = """
<!DOCTYPE html>
<html lang="en">
{head}
<body style="font-size: xx-large;padding:50px 10px">
{content}
</body>
</html>
"""
    out_path = "E:/code/Python/html2pdf/out"
    urls = {
        'java编程思想第五版': 'https://lingcoder.gitee.io/onjava8/#/sidebar',
    }
    for item in urls:
        crawler = OnJava8Crawler(item, urls[item], out_path)
        # crawler.run()
        crawler.html_to_pdf()
