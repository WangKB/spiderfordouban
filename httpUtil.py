import json

from time import sleep
from requests import get
from lxml import etree


def get_html(url, proxies=None):
    # proxies = {
    #     'http': 'http://77.73.66.26:8080',
    #     'https': 'http://77.73.66.26:8080'
    # }
    sleep(2)
    headers = {
        'User-Agent':
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
            'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
    }
    response = get(url,  headers=headers, proxies=proxies)
    html = response.content
    return etree.HTML(html.decode('utf-8'))


def get_json(url):
    r = get(url)
    data = json.loads(r.read().decode(r.info().get_param('charset') or 'utf-8'))
    return data


def get_tail(html, text):
    if len(html.xpath(text)) > 0:
        return html.xpath(text)[0].tail
    return None


def get_inner_text(html, text):
    if len(html.xpath(text)) > 0:
        return str(html.xpath(text)[0])
    return None


def get_attr(html, text):
    if len(html.xpath(text)) > 0:
        return str(html.xpath(text)[0])
    return None


def bea_celebrity_info(info):
    if info is not None:
        return info.replace(":", "").strip()
    return None
