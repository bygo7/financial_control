# -*- coding: utf-8 -*-
"""
Created on Sat Sep 11 19:05:45 2021

@author: Byeongyong
"""
import pandas as pd
import base_datatable
import get_pricelist
import tqdm
from pykrx import stock
import datetime


### Update Base Data of Datatable
# base_datatable.update_data()

# datatable = base_datatable.generate_datatable() # Old Version from DART
needed_data_list = ['환산보통주수(계산)', '순보통주수(계산)', '보통주수', '보통자사주', '잠재주수(?)', '순우선주수', '우선주수', '자산(연도별)', '자기자본(연도별)', '무형자산', '메출액', '매출채권', '채권조정(계산, ?)', '재고자산', '재고조정(계산)', '부채총액', '부채조정(계산)', '조정합계(계산)', '당기순이익(연도별)', 'ROA(연도별, 계산)', 'DY(연도별, 아마 배당?)', '추정BPS(계산)', '수정BPS(계산)', '추정EPS(계산)', '수정EPS(계산)', 'ROE(계산)', '배당성향(계산)', '기준금리(r3, r4)', 'growth rate(g)', 'VALUE(계산)', '주가', '기대수익률(계산)', '기대수익률 10y(계산)', 'PER(계산)', '적정PER(계산)', 'PBR(계산)', '적정PBR(계산)', 'DY(계산)', '자산가치(계산)', '수익가치(계산)', '성장가치(계산)', '성장V/내재V(계산)', ]
needed_data_list_origin = []
for elem in needed_data_list:
    if '계산' in elem:
        pass
    else:
        needed_data_list_origin.append(elem)
# # 1시간 정도 소요.
# price_list = get_pricelist.get_pricelist(corp_code_list)
# datatable['주가'] = price_list

today = datetime.datetime.today()
import exchange_calendars as ecals
XKRX = ecals.get_calendar("XKRX") # 한국 코드
todaystr = str(today.year) + str(today.month).zfill(2) + str(today.day).zfill(2)
while not XKRX.is_session(todaystr): # 개장일인지 확인
    today = today - datetime.timedelta(days = 1)
    todaystr = str(today.year) + str(today.month).zfill(2) + str(today.day).zfill(2)

# datatable = stock.get_market_ohlcv_by_ticker(todaystr, market="ALL")
datatable = stock.get_market_cap_by_ticker(todaystr)
corp_code_list = datatable.index.tolist()

df_temp = stock.get_market_price_change_by_ticker(fromdate = todaystr, todate = todaystr, market = "ALL")
datatable['종목명'] = df_temp['종목명']

datatable = datatable['종목명', '종가', '시가총액']

df2 = stock.get_market_fundamental_by_ticker(todaystr, market="ALL")
