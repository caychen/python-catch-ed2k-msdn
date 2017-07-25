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
from threading import Thread, Lock

threads = []
g_Count = 1
lock = Lock()

def get_response_text(session, url=None, data=None, headers=None):
    if data == None:
        return session.get(url).text
    else:
        return session.post(url, data, headers=headers).text
    

class MenuSpider(Thread):
    def __init__(self, session, headers, url, menu_id):
        super().__init__()
        self._url = url
        self._session = session
        self._headers = headers
        self._menu_id = menu_id
        
        self._index_url = urljoin(url, 'Category/Index')
        self._lang_url = urljoin(url, 'Category/GetLang')
        self._list_url = urljoin(url, 'Category/GetList')
        self._product_url = urljoin(url, 'Category/GetProduct')
    
    def craw_index(self, menu_id):   
        products = json.loads(get_response_text(self._session, self._index_url, data={'id':menu_id}, headers=self._headers))
        if len(products) > 0:
            for product in products:
               # print('当前产品名称为:',product['name'])
               self.craw_lang(product['id'])
            
    def craw_lang(self, product_id):
        langs = json.loads(get_response_text(self._session, self._lang_url, {'id':product_id}, headers=self._headers))['result']
        if len(langs) > 0:
            for lang in langs:
                # print('当前语言为:',lang['lang'])
                self.craw_list(product_id, lang['id'])
#         else:
#             print('没有数据...')
            
    def craw_list(self, product_id, lang_id):
        products_list = json.loads(get_response_text(self._session, self._list_url, data={'id':product_id, 'lang':lang_id, 'filter':'true'}, headers=self._headers))['result']
        if len(products_list) > 0:
            for product in products_list:
    #             self._products_detail_id.append(product)
                self.craw_products(product['id'])
        
    def craw_products(self, product_detail_id):
        obj = json.loads(get_response_text(self._session, self._product_url, data={'id':product_detail_id}, headers=self._headers))['result']
        product = Product.Product(FileName=obj['FileName'], DownLoad=obj['DownLoad'], PostDateString=obj['PostDateString'], SHA1=obj['SHA1'], size=obj['size'])
#         print(obj['result'])
        global g_Count
        lock.acquire()
        print(g_Count, ":", product)
        g_Count += 1
        lock.release()
    
    def run(self):
        self.craw_index(self._menu_id)
        pass


class Spider:
    _header = {'Use-Agent':'Mozilla/5.0 (Windows NT 6.1; rv:47.0) Gecko/20100101 Firefox/47.0',
               'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
               }
    
    def __init__(self, url=None):
        self.session = requests.session()
        self._url = url
        self._header['Referer'] = url
        self._header['Host'] = url[url.find('msdn'):]
#         print(self._header['Host'])
       
    
    @classmethod        
    def parser(cls, text, tagElement, attrs=None):
        soup = BeautifulSoup(text, 'html.parser')
        return soup.find_all(tagElement, attrs)
    
    def craw_home(self):  # login the home
        response_text = get_response_text(self.session, self._url, headers=self._header)
#         soup = BeautifulSoup(response_text,'html.parser')
#         menus = soup.find_all('a',attrs={'data-loadmenu':'true'})
        menus = Spider.parser(response_text, 'a', attrs={'data-loadmenu':'true'})
        if len(menus) > 0:
            for menu in menus:
    #             self._menuid.append(menu['data-menuid'])
                # self._menuname.append(menu.get_text())]
#                 print('当前左侧菜单为:', menu.get_text())
                th = MenuSpider(self.session, self._header, self._url, menu['data-menuid'])
                threads.append(th)
                th.start() 
                
        for th in threads:
            th.join()