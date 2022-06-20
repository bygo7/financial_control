# -*- coding: utf-8 -*-
"""
Created on Mon Sep  6 00:11:57 2021

@author: Byeongyong
"""
# 스노우볼 엑셀파일의 수치들을 업데이트 한다.

#1. P(현재가) 업데이트
from tqdm import tqdm
# 가격정보 불러오기 from naver finance
from bs4 import BeautifulSoup
import requests
def get_bs_obj(com_code): # url의 데이터 bs로 가져오기
    url = "https://finance.naver.com/item/main.nhn?code=" + com_code
    result = requests.get(url)
    bs_obj = BeautifulSoup(result.content, "html.parser") #html.parser 로 파이썬에서 쓸 수 있는 형태로 변환
    return bs_obj
def get_price(com_code):
    bs_obj = get_bs_obj(com_code)
    no_today = bs_obj.find("p", {"class":"no_today"})
    try:
        blind_now = no_today.find("span", {"class":"blind"})
        price = blind_now.text
    except AttributeError:
        blind_now = 'NaN'
        price = 'No Data'
    return price

def get_pricelist (corp_code_list):
    # '종목코드' 열의 A가 들어있는 셀중 기업코드만 발췌
    price_list = []
    for elem in tqdm(corp_code_list):
        price_list.append(get_price(elem))
        
    return price_list


import pandas_datareader as pdr
from datetime import datetime
def get_pricelist_yahoo(corp_code_list):
    date = str(datetime.today().year) + '-' + str(datetime.today().month).zfill(2) + '-' + str(datetime.today().day).zfill(2)
    price_list = []
    for elem in tqdm(corp_code_list):
        corp = elem + '.KS'
        try:
            close_price = pdr.get_data_yahoo(corp, start = date, end = date).iloc[0, 3]
        except:
            close_price = 'No Data'
        price_list.append(close_price)
    return price_list

def get_pricelist_yahoo_list(corp_code_list):
    corp_code_list_KS = []
    for elem in corp_code_list:
        corp_code_list_KS.append(elem + '.KS')
    date = str(datetime.today().year) + '-' + str(datetime.today().month).zfill(2) + '-' + str(datetime.today().day).zfill(2)
    df = pdr.get_data_yahoo(corp_code_list_KS, start = date, end = date)
    return df
