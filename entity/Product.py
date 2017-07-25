#! /usr/bin/env python3
# -*- coding: utf-8 -*-

'''
@file: entity.Product

@email: 412425870@qq.com

@author: Cay

@pythonVersion: Python3.5

@function: 

@version: 
'''

class Product:
    def __init__(self, **kwarg):
#         self._FileName = FileName
#         self._DownLoad = DownLoad
#         self._PostDateString = PostDateString
#         self._SHA1 = SHA1
#         self._size = size
        for key in kwarg:
            setattr(self, key, kwarg[key])
         
        
    @property
    def FileName(self):
        return self._FileName
    
    @FileName.setter
    def FileName(self, value):
        self._FileName = value
        
    @property
    def DownLoad(self):
        return self._DownLoad
    
    @DownLoad.setter
    def DownLoad(self, value):
        self._DownLoad = value
        
    @property
    def PostDateString(self):
        return self._PostDateString
    
    @PostDateString.setter
    def PostDateString(self, value):
        self._PostDateString = value
        
    @property
    def SHA1(self):
        return self._SHA1
    
    @SHA1.setter
    def SHA1(self, value):
        self._SHA1 = value
        
    @property
    def size(self):
        return self._size
    
    @size.setter
    def size(self, value):
        self._size = value
    
    def __str__(self):
        return "[FileName: " + self.FileName + ",DownLoad: " + self.DownLoad + ",PostDateString: " + self.PostDateString + ",SHA1: " + self.SHA1 + ",size: " + self.size + "]"
    
    __repr__ = __str__