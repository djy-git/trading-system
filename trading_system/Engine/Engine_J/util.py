import numpy as np

from common import *

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
import json
import torch
import random
from torch.utils.data import TensorDataset, DataLoader, RandomSampler, SequentialSampler
from Engine.Engine_Y.util import *


#랜덤시드 고정 -> 추후 이동?
seed_val = 42
random.seed(seed_val)
np.random.seed(seed_val)
torch.manual_seed(seed_val)
torch.cuda.manual_seed_all(seed_val)

'''
!!! 해당 파일은 CPU 기반!!!

GPU 학습시에 torch에서 CUDA 설정이 필요함!!

'''
'''
종목코드, 코드 검색 이름 가져오기
'''
def get_code_code_str():
    with open('code_str_list.json', 'r') as f:
        json_data = json.load(f)
        return list(json_data.keys()), list(json_data.values())
    return None

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

    '''
    ## 기호는 앞 토큰과 이어진다는 표시입니다. 토크나이저는 여러 언어의 데이터를 기반으로 만든 'bert-base-multilingual-cased'를 사용합니다. 그래서 한글도 처리가 가능합니다.
    '''
    # pre-train된 토큰화 모델을 불러온다.
    tokenizer = BertTokenizer.from_pretrained('bert-base-multilingual-cased', do_lower_case=False) #truncation=True, padding=True

    # 문장에서 글자에 대한 토큰화 수행
    tokenized_texts = tokenizer.tokenize(sent)
    return tokenized_texts

def get_embedding_token(tokenized_text):
    # pre-train된 토큰화 모델을 불러온다.
    # Q : 이전에 위에서 토크나이즈를 수행한 결과를 가진 토큰 객체를 사용해야 하는가? 여기서 새로 정의해서 수행해도 되는가?
    tokenizer = BertTokenizer.from_pretrained('bert-base-multilingual-cased', do_lower_case=False)  # truncation=True, padding=True

    # 토큰을 숫자 인덱스로 변환
    input_id = tokenizer.convert_tokens_to_ids(tokenized_text)


    # 어텐션 마스크 초기화 -> 이것도 일단은 생략!
    return input_id

def match_sent_size(sent, MAX_LEN = 32):
    # 성능에 영향을 미칠 수 있는 요인
    # 문장을 MAX_LEN 길이에 맞게 자르고, 모자란 부분을 패딩 0으로 채움 -> 이부분이 필요한가? Bert는 길이에 종속 안되지 않나?
    # Tensor변환 과정에서 입력 모양을 맞춰줘야해서 일단 추가함!
    sent = pad_sequences(sent, maxlen=MAX_LEN, dtype="long", truncating="post", padding="post")
    return sent

# target_code : https://colab.research.google.com/drive/1tIf0Ugdqg4qT7gcxia3tL7und64Rv1dP#scrollTo=muU2kS2GCh4y
def train_model(train_dataloader, epochs= 1):

    # 모델의 작업에 따라 수행되는 모델의 이름이 다른듯? 여기서는 분류를 사용하기 때문에 BertForSequenceClassification 사용.
    # 미리 훈련된 모델을 이용
    '''
    fine-tuning에서 모델을 불러와서 학습을 시키면 된다는데, layer 고정 없이 어떻게 진행하는지 알 필요가 있다
    '''
    model = BertForSequenceClassification.from_pretrained("bert-base-multilingual-cased", num_labels=2)

    '''
    데이터 훈련 구간
    '''
    # 옵티마이저 설정
    optimizer = AdamW(model.parameters(),
                      lr=2e-5,  # 학습률
                      eps=1e-8  # 0으로 나누는 것을 방지하기 위한 epsilon 값
                      )

    # 그래디언트 초기화
    model.zero_grad()

    # 에폭만큼 반복
    for epoch_i in range(0, epochs):

        # 로스 초기화
        total_loss = 0

        # 훈련모드로 변경
        model.train()

        # 데이터로더에서 배치만큼 반복하여 가져옴
        for step, batch in enumerate(train_dataloader):
            # 배치에서 데이터 추출
            b_input_ids, b_labels = batch

            # Forward 수행
            outputs = model(b_input_ids, labels=b_labels)
            print(outputs)
            # 로스 구함
            loss = outputs[0]

            # 총 로스 계산
            total_loss += loss.item()

            # Backward 수행으로 그래디언트 계산
            loss.backward()

            # 그래디언트를 통해 가중치 파라미터 업데이트
            optimizer.step()

            # 그래디언트 초기화
            model.zero_grad()

    return model


def make_data_set(train_inputs, train_labels, batch_size = 1):

    # 파이토치의 DataLoader로 입력, 라벨을 묶어 데이터 설정
    # 학습시 배치 사이즈 만큼 데이터를 가져옴

    #TensorDataset은 Dataset을 상속한 클래스로 학습 데이터 X와 레이블 Y를 묶어 놓는 컨테이너이다.
    train_data = TensorDataset(train_inputs, train_labels)
    train_sampler = RandomSampler(train_data)

    # TensorDataset을 DataLoader에 전달하면 for 루프에서 데이터의 일부분만 간단히 추출할 수 있게 된다.
    train_dataloader = DataLoader(train_data, sampler=train_sampler, batch_size=batch_size)

    return train_dataloader

def get_label(code, number):
    today = datetime.today()
    yesterday = today - timedelta(days=1)
    price = download_price(code, yesterday.strftime("%Y%m%d"), today.strftime("%Y%m%d"))
    print(price)
    if price['close'].values[1]>price['close'].values[0]:
        label = [1 for i in range(number)]
    else:
        label = [0 for i in range(number)]

    return label

'''
test 구간
'''


# Data_X = np.array([])
# Data_Y = np.array([])
#
# code_list, code_str_list = get_code_code_str()
# for code_ind in range(len(code_str_list)):
#     code_str = code_str_list[code_ind]
#     code = code_list[code_ind]
#     print("test!!")
#     print(code)
#     url_list, subject_list = get_url_list(code_str)
#
#     totken_txts = [get_tokenize(subject) for subject in subject_list]
#
#     totken_embeddings = [get_embedding_token(totken_txt) for totken_txt in totken_txts]
#     totken_embeddings = match_sent_size(totken_embeddings)
#
#     labels = get_label(code, len(subject_list))
#     labels = np.array(labels)
#     if len(Data_X)==0:
#         Data_X = totken_embeddings
#         Data_Y = labels
#     else:
#         Data_X = np.append(Data_X, totken_embeddings, axis=0)
#         Data_Y = np.append(Data_Y, labels, axis=0)
#     print(Data_X)
#     print(Data_Y)
#
# Data_X = torch.tensor(Data_X)
# Data_Y = torch.tensor(Data_Y)
# Data_Y = Data_Y.type(torch.LongTensor)
#
# train_dataloader = make_data_set(Data_X, Data_Y)
# model = train_model(train_dataloader)
# print('end_test')


# code_str_list = ["samsung%20electronic"]
# for code_str in code_str_list:
#     url_list, subject_list = get_url_list(code_str)
#     totken_txt = get_tokenize(subject_list[0])
#     print(totken_txt)
#     totken_embedding = get_embedding_token(totken_txt)
#     print(totken_embedding)
'''
test 구간 해제
'''
