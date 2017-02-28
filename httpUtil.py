import json

from time import sleep
from requests import get
from lxml import etree


def get_html(url):
    sleep(2)
    html = get(url).content
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
