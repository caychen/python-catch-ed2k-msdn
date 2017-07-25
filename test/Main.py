#! /usr/bin/env python3
# -*- coding: utf-8 -*-

'''
@file: test.main

@email: 412425870@qq.com

@author: Cay

@pythonVersion: Python3.5

@function: 

@version: 
'''
from spider.Spider import Spider
import time

if __name__ == '__main__':
    spider = Spider('http://msdn.itellyou.cn')
    print('开始爬取msdn itellyou上的ed2k链接...')
    start = time.time()
    spider.craw_home()
        
    end = time.time()
    print('总共用时:',end - start, 's')