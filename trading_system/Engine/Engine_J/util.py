import requests
from pandas import DataFrame
from bs4 import BeautifulSoup
import re
from datetime import datetime
import os



'''
원하는 종목과 관련된 기사 url 크롤링
'''
def get_url_list(code_str):
    news_url = 'https://www.koreatimes.co.kr/www2/common/search.asp?kwd=' + code_str
    req = requests.get(news_url)

    soup = BeautifulSoup(req.text, 'html.parser')
    news_list = soup.find_all('div', {'class': 'list_article_headline HD'})
    url_list = []
    subject_list = []
    for news in news_list:
        url_list.append(news.find('a', href=True)['href'])
        subject_list.append(str(news.text).replace('\n',''))
    return url_list, subject_list


'''
각 기사 url로 부터 내용 크롤링 -> 일단 제목으로 먼지 처리 하는거 먼저 연습하자!
'''
def get_new(news_url):
    req = requests.get(news_url)
    soup = BeautifulSoup(req.text, 'html.parser')
    news = soup.find_all('div', {'class': 'view_mid_div'})
    return

'''
test 구간
'''

code_str_list = ["samsung%20electronic"]
for code_str in code_str_list:
    url_list, subject_list = get_url_list(code_str)
'''
test 구간 해제
'''
