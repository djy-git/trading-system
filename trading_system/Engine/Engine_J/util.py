import requests
from pandas import DataFrame
from bs4 import BeautifulSoup
import re
from datetime import datetime
import os

from transformers import BertTokenizer
from transformers import BertForSequenceClassification, AdamW, BertConfig
from transformers import get_linear_schedule_with_warmup
from keras.preprocessing.sequence import pad_sequences

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

def get_new(news_url):
    req = requests.get(news_url)
    soup = BeautifulSoup(req.text, 'html.parser')
    news = soup.find_all('div', {'class': 'view_mid_div'})
    return

# 작업에 따른 문장 데이터 생성 및 토큰화 작업
def get_tokenize(sentence, method='CLS'):
    '''
    BERT는 형태소분석으로 토큰을 분리하지 않는다고함.
    WordPiece라는 통계적인 방식을 사용하는데, 한 단어내에서 자주 나오는 글자들을 붙여서 하나의 토큰으로 만든다고함.(아마 이걸 sub-word 임베딩이라고 부르나??)
    (매우 중요한듯!) 언어에 상관없이 토큰을 생성할 수 있다는 장점이 있고, 신조어 같이 사전에 없는 단어를 처리하기도 좋다고함.
    '''
    sent = None

    # 작업에 따른 문장 전처리
    if method=='CLS':
         sent = "[CLS] " + sentence + " [SEP]"

    # pre-train된 토큰화 모델을 불러온다.
    tokenizer = BertTokenizer.from_pretrained('bert-base-multilingual-cased', do_lower_case=False) #truncation=True, padding=True

    # 문장에서 글자에 대한 토큰화 수행
    tokenized_texts = tokenizer.tokenize(sent)
    return tokenized_texts

def get_embedding_token(tokenized_text, MAX_LEN = 128):
    # pre-train된 토큰화 모델을 불러온다.
    # Q : 이전에 위에서 토크나이즈를 수행한 결과를 가진 토큰 객체를 사용해야 하는가? 여기서 새로 정의해서 수행해도 되는가?
    tokenizer = BertTokenizer.from_pretrained('bert-base-multilingual-cased', do_lower_case=False)  # truncation=True, padding=True

    # 토큰을 숫자 인덱스로 변환
    input_id = tokenizer.convert_tokens_to_ids(tokenized_text)

    #성능에 영향을 미칠 수 있는 요인
    # 문장을 MAX_LEN 길이에 맞게 자르고, 모자란 부분을 패딩 0으로 채움 -> 이부분이 필요한가? Bert는 길이에 종속 안되지 않나?
    #input_id = pad_sequences(input_id, maxlen=MAX_LEN, dtype="long", truncating="post", padding="post")

    # 어텐션 마스크 초기화 -> 이것도 일단은 생략!
    return input_id


def train_model():
    # 모델의 작업에 따라 수행되는 모델의 이름이 다른듯? 여기서는 분류를 사용하기 때문에 BertForSequenceClassification 사용.
    # 미리 훈련된 모델을 이용
    '''
    fine-tuning에서 모델을 불러와서 학습을 시키면 된다는데, layer 고정 없이 어떻게 진행하는지 알 필요가 있다
    '''
    model = BertForSequenceClassification.from_pretrained("bert-base-multilingual-cased", num_labels=2)

    '''
    데이터 훈련 구간
    '''

    return input_id

'''
test 구간
'''

code_str_list = ["samsung%20electronic"]
for code_str in code_str_list:
    url_list, subject_list = get_url_list(code_str)
    totken_txt = get_tokenize(subject_list[0])
    print(totken_txt)
    totken_embedding = get_embedding_token(totken_txt)
    print(totken_embedding)
'''
test 구간 해제
'''
