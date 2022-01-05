import requests
from pandas import DataFrame
from bs4 import BeautifulSoup
import re
from datetime import datetime
import os

code_str = "samsung%20electronic"
def get_url_list(code_str):
    news_url = 'https://www.koreatimes.co.kr/www2/common/search.asp?kwd=' + code_str
    req = requests.get(news_url.format(query))
    soup = BeautifulSoup(req.text, 'html.parser')
    ranks = soup.find_all('div', {'class': 'list_article_headline HD'})
    print(ranks)
    return
get_url_list(code_str)