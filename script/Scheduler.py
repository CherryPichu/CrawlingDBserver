from functools import wraps
import errno
import os
import signal
import time
from datetime import datetime
import requests
from script.Unit import Unit
from db import UrlManager,  HtmlFileManager

"""
    일단 새로운 접속이 생기면, ProccessID 생성
"""
class Scheduler:
    def __init__(self):
        self.units : dict = {}

    def createUnit(self, name : str) -> bool:
        unit = Unit(name)
        if(name in self.units.keys()) :
            return False
        self.units[name] = unit
        
        return True
        

    def getUnitbyName(self, name: str) -> Unit:
        if(name in self.units.keys()) :
            return self.units[name]
        return None


    def getOnionUrl(self, name : str) -> str:
        unit = self.getUnitbyName(name)
        if unit == None :
            return ""
        
        url_manager = UrlManager()
        dbIndex, target_url = url_manager.getOnionUrl(unit.getUrlRow()[0])
        unit.activate(dbIndex, target_url)
        
        return target_url

    def postHtmlRow(self, name: str, origin_url: str, parameter: str, title: str,
                             url: str, domain: str, html_content: str, word_list: list, referer:str) -> bool:
        unit = self.getUnitbyName(name)
        if unit == None :
            return False
        
        html_manager = HtmlFileManager()
        success = html_manager.insertIntoTable(origin_url, parameter, title, 
                                url, domain, html_content, word_list, referer)

        if success:
            url_manager = UrlManager()
            dbIndex, url = unit.getUrlRow()
            url_manager.updateById(dbIndex, isCrawling=True)
            unit.terminate()
            
        url_manager = UrlManager()
        url_manager.updateOwnership(unit.getUrlRow()[0], False)
            
        return success

if __name__ == "__main__":
    scheduler = Scheduler()
    # scheduler.create_unit("Example Unit")
        
"""
    스케줄러를 만들 때
    100만개 url 를 병행으로 작동하게 만들어줘야함.
    pop(1) 을 통해서 중복되지 않은 url 을 반환하는 클래스를 만든다.
    가장 오래된 url은 업데이트 갱신해야하는 것도 만들어야함.
    
    db 를 애용해서 스케줄러를 구성해야함.
    스케줄러 DB 클래스, 중복되지 않은 url을 반환하는 클래스
    각각을 만들어야함.
    지랄 맞다 진짜
    
    크롤러는 단어 명사만 뽑아야한다.
"""