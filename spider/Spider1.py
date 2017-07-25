#! /usr/bin/env python3
# -*- coding: utf-8 -*-

'''
@file: spider.spider

@email: 412425870@qq.com

@author: Cay

@pythonVersion: Python3.5

@function: 

@version: 
'''

import requests
from bs4 import BeautifulSoup
import json
from entity import Product
from urllib.parse import urljoin

class Spider:
    #_url = 'http://msdn.itellyou.cn'
    _count = 1
#     _menuid = []
    _menuname = []
    _products_detail_id = []
    _header = {'Use-Agent':'Mozilla/5.0 (Windows NT 6.1; rv:47.0) Gecko/20100101 Firefox/47.0',
               'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
               }
    
    def __init__(self,url=None):
        self.session = requests.session()
        self._url = url
        self._header['Referer'] = url
        self._header['Host'] = url[url.find('msdn'):]
#         print(self._header['Host'])
        self._index_url = urljoin(url,'Category/Index')
        self._lang_url = urljoin(url,'Category/GetLang')
        self._list_url = urljoin(url,'Category/GetList')
        self._product_url = urljoin(url,'Category/GetProduct')
        
    
    def get_response_text(self, url=None, data=None):
        if data == None:
            return self.session.get(url).text
        else:
            return self.session.post(url, data, headers=self._header).text
        
    @classmethod        
    def parser(cls, text, tagElement, attrs=None):
        soup = BeautifulSoup(text, 'html.parser')
        return soup.find_all(tagElement, attrs)
    
    def craw_home(self):#login the home
        response_text = self.get_response_text(self._url)
#         soup = BeautifulSoup(response_text,'html.parser')
#         menus = soup.find_all('a',attrs={'data-loadmenu':'true'})
        menus = Spider.parser(response_text,'a', attrs={'data-loadmenu':'true'})
        if len(menus) > 0:
            for menu in menus:
    #             self._menuid.append(menu['data-menuid'])
                #self._menuname.append(menu.get_text())]
                print('当前左侧菜单为:', menu.get_text())
                self.craw_index(menu['data-menuid'])
            
#         self.craw_index('fcf12b78-0662-4dd4-9a82-72040db91c9e')
    
    def craw_index(self, menu_id):   
        products = json.loads(self.get_response_text(self._index_url, data={'id':menu_id}))
        if len(products) > 0:
            for product in products:
                print('当前产品名称为:',product['name'])
                self.craw_lang(product['id'])
            
    def craw_lang(self, product_id):
        langs = json.loads(self.get_response_text(self._lang_url, {'id':product_id}))['result']
        if len(langs) > 0:
            for lang in langs:
                print('当前语言为:',lang['lang'])
                self.craw_list(product_id, lang['id'])
        else:
            print('没有数据...')
            
    def craw_list(self, product_id, lang_id):
        products_list = json.loads(self.get_response_text(self._list_url, data={'id':product_id,'lang':lang_id,'filter':'true'}))['result']
        if len(products_list) > 0:
            for product in products_list:
    #             self._products_detail_id.append(product)
                self.craw_products(product['id'])
        
    def craw_products(self, product_detail_id):
        obj = json.loads(self.get_response_text(self._product_url, data={'id':product_detail_id}))['result']
        product = Product.Product(FileName = obj['FileName'],DownLoad = obj['DownLoad'],PostDateString = obj['PostDateString'],SHA1 = obj['SHA1'],size = obj['size'])
#         print(obj['result'])
        print(self._count, ":", product)
        self._count += 1