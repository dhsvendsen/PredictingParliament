# -*- coding: UTF-8 -*-

from lxml import html
import requests

page = requests.get('http://www.ft.dk/samling/20141/lovforslag/L4/index.htm')
tree = html.fromstring(page.text)

title = tree.xpath('//*[@id="menuSkip"]/h1[1]/text()')
forslagsstiller = tree.xpath('//*[@id="menuSkip"]/p[1]/a/text()')
ministeromraade = tree.xpath('//*[@id="menuSkip"]/p[4]/text()')
resume = tree.xpath('//*[@id="menuSkip"]/p[5]/text()')

print ministeromraade