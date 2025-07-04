import os
import sys
import urllib.request
from bs4 import BeautifulSoup
from urllib.request import urlopen
import time

client_id = "Og48dwj0wUikSb5v3DxL"
client_secret = "CfNUwk0ByN"
search_word = input("검색어 입력: ")

def gen_search_url(api_node, search_text, start_num, disp_num):
    base = 'https://openapi.naver.com/v1/search'
    node = '/' + api_node +'.json'
    param_query = '?query=' + urllib.parse.quote(search_text)
    param_start = '&start=' + str(start_num)
    param_disp = '&display=' + str(disp_num)

    return base + node + param_query + param_start + param_disp

import json
import datetime
from urllib.request import Request

def get_result_onpage(url):
    request = urllib.request.Request(url)
    request.add_header("X-Naver-Client-Id", client_id)
    request.add_header("X-Naver-Client-Secret", client_secret)
    response = urllib.request.urlopen(request)
    print('[%s] Url Request Success' % datetime.datetime.now())

    return json.loads(response.read().decode('utf-8'))

import pandas as pd

def delete_tag(input_str):
    input_str = input_str.replace('<b>', '')
    input_str = input_str.replace('</b>', '')
    return input_str

def get_fields(json_data):
    title = [delete_tag(each['title']) for each in json_data['items']]
    image = [each['image'] for each in json_data['items']]
    link = [each['link'] for each in json_data['items']]
    lprice = [each['lprice'] for each in json_data['items']]
    brand = [each['brand'] for each in json_data['items']]
    category = [each['category4'] for each in json_data['items']]

    result_pd = pd.DataFrame({
        'title': title,
        'image' : image,
        'link': link,
        'lprice': lprice,
        'brand': brand,
        'category': category
    }, columns=['image', 'title', 'brand', 'lprice', 'category', 'link'])

    return result_pd

result_mol = []

for n in range(1, 300, 100):
    url = gen_search_url('shop', search_word, n, 100)
    json_result = get_result_onpage(url)
    pd_result = get_fields(json_result)

    result_mol.append(pd_result)

result_mol = pd.concat(result_mol)

result_mol.reset_index(drop=True, inplace=True)
result_mol['lprice'] = result_mol['lprice'].astype('float')

lt = time.localtime()

with pd.ExcelWriter(f'./{lt.tm_year}.{lt.tm_mon}.{lt.tm_mday}_네이버쇼핑_{search_word}_상품정보.xlsx', engine='xlsxwriter') as writer:
    result_mol.to_excel(writer, sheet_name='Sheet1')

    workbook = writer.book
    worksheet = writer.sheets['Sheet1']

	# 셀 너비 지정
    worksheet.set_column('A:A', 4)
    worksheet.set_column('B:B', 10)
    worksheet.set_column('C:C', 60)
    worksheet.set_column('D:D', 10)
    worksheet.set_column('E:E', 10)
    worksheet.set_column('F:F', 10)
    worksheet.set_column('G:G', 50)

    worksheet.conditional_format('E2:E301', {'type': '3_color_scale'})