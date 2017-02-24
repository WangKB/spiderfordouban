import json
import urllib.request
import urllib.error
from time import sleep

from lxml import etree


def get_html(url):
    sleep(2)
    html = urllib.request.urlopen(url).read()
    return etree.HTML(html.lower().decode('utf-8'))


def get_json(url):
    r = urllib.request.urlopen(url)
    data = json.loads(r.read().decode(r.info().get_param('charset') or 'utf-8'))
    return data
