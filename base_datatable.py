# -*- coding: utf-8 -*-
"""
Created on Wed Aug 18 22:49:17 2021

@author: Byeongyong
"""

from urllib.request import urlopen
from io import BytesIO
from zipfile import ZipFile

## Import Corp_Code data zip file from opendart
def update_data():
    url_corpCode = 'https://opendart.fss.or.kr/api/corpCode.xml?crtfc_key=b3d4723c7ae978f43eaefc069da9fefe5040196f'
    with urlopen(url_corpCode) as zipresp:
        with ZipFile(BytesIO(zipresp.read())) as zfile:
            zfile.extractall('corp_code')


# Pre-Downloaded Data...
import xml.etree.ElementTree as ET
tree = ET.parse('./corp_code/CORPCODE.xml')
root = tree.getroot()
# for country in root.iter():
#     print(country.tag, country.text)

def find_corp_num(find_name):
    for country in root.iter("list"):
        if country.findtext("corp_name") == find_name:
            return country.findtext("corp_code")

# import requests
############################################ 개발가이드 > 공시정보 탭 / 쓸모있는 정보가 없음.
# def load_data(**kwargs):
#     crtfc_key = 'b3d4723c7ae978f43eaefc069da9fefe5040196f'
#     try:
#         corp_code = kwargs['corp_code']
#         url = 'https://opendart.fss.or.kr/api/company.json?crtfc_key='+crtfc_key+'&corp_code='+corp_code
#         r = requests.get(url)
#         company_data = r.json()
#         return company_data
#     except KeyError:
#         try:
#             corp_name = kwargs['corp_name']
#             corp_code = find_corp_num(corp_name)
#             print('hi')
#             url = 'https://opendart.fss.or.kr/api/company.json?crtfc_key='+crtfc_key+'&corp_code='+corp_code
#             r = requests.get(url)
#             company_data = r.json()
#             return company_data
#         except KeyError:
#             print('Key Error!')
#         except TypeError:
#             print('There is No company name like', corp_name)

# ##############################################
# def load_data(corp_code):
#     crtfc_key = 'b3d4723c7ae978f43eaefc069da9fefe5040196f'
#     try:
#         url = 'https://opendart.fss.or.kr/api/company.json?crtfc_key='+crtfc_key+'&corp_code='+corp_code
#         r = requests.get(url)
#         company_data = r.json()
#         return company_data
#     except KeyError:
#         print('Key Error!')
###############################################
## List Company Codes from root
def generate_datatable():
    code_list = []
    corp_name_list = []
    stock_code_list = []
    modify_date_list = []
    for x in range(len(root)):
        if root[x][2].text != " ": # 종목코드가 없는 경우 제외 = 상장기업만.
            code_list.append(root[x][0].text)
            corp_name_list.append(root[x][1].text)
            stock_code_list.append(root[x][2].text)
            modify_date_list.append(root[x][3].text)
    # print(len(code_list), len(corp_name_list), len(stock_code_list), len(modify_date_list))
    if not ((len(code_list) == len(corp_name_list)) and (len(stock_code_list) == len(modify_date_list))):
        print("Data Error! Not Valid. Check the data.")
    ### Print Company Names in code_list
    # for elem in code_list[0:10]:
    #     print(load_data(request = 'company', corp_code = elem)['corp_name'])
    
    # from tqdm import tqdm
    
    # company_condition_list = []
    
    # for corp_code_elem in tqdm(code_list):
    #     company_dict = load_data(corp_code = corp_code_elem)
    #     company_condition_list.append(company_dict)
        
    # import pickle
    # with open('company_condition_list.txt', 'wb') as f:
    #     pickle.dump(company_condition_list, f)
    base_dict = {'고유번호':code_list, '정식명칭':corp_name_list, '종목번호':stock_code_list, '최종변경일자':modify_date_list}
    
    import pandas as pd
    pd_data = pd.DataFrame.from_dict(base_dict)
    return pd_data
