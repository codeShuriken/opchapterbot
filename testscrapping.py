from bs4 import BeautifulSoup
from urllib.parse import urlparse

import requests
import bs4

url = 'http://onepiece.wikia.com/wiki/Chapter_863'

r = requests.get(url)
soup = BeautifulSoup(r.content, 'html.parser')

table = soup.find_all('div',attrs={"mw-content-ltr mw-content-text"})
for x in table:
    i = 0
    cover_page_mark = 0
    short_summary_mark = 0
    long_summary_mark = 0

    cover_page = ''
    short_summary = ''

    for el in x.find_all(['h2', 'p']):
        if el.name == 'h2':
            if "Cover Page" in el.get_text() and el.name == 'h2':
                cover_page_mark = i
            if "Short Summary" in el.get_text() and el.name == 'h2':
                short_summary_mark = i
            if "Long Summary" in el.get_text() and el.name == 'h2':
                long_summary_mark = i
        i += 1

    i = 0
    for el in x.find_all(['h2', 'p']):
        if el.name == 'p':
            if cover_page_mark < i < short_summary_mark:
                cover_page += el.get_text()
            if short_summary_mark < i < long_summary_mark:
                short_summary += el.get_text()
        i += 1
        
print (cover_page)
print (short_summary)
