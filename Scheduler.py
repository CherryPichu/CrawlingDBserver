import KHS, LJH, Min, OST
from functools import wraps
import errno
import os
import signal
import time
from datetime import datetime
from Unit import Unit
import requests

"""
    일단 새로운 접속이 생기면, ProccessID 생성
"""
class Scheduler :
    def __init__(self) :    
        self.__Units : list[Unit] = []
        self.id_index = 0
        
    def newUnit(self, url : str, name : str) :
        unit = Unit(self.id_index + 1, name )
        self.id_index += 1
        self.__Units.append(unit)
        
        return self.id_index
        
    def findByUnit(self, id : int) :
        id_list = list()
        for unit  in self.__Units :
            id_list.append( unit.getUnitId() )


if __name__ == "__main__":
    scheduler = Scheduler()
    processed_onions = []

    
    # 파일을 읽기 모드로 열기
    with open("./onions.txt", 'r') as file:
        # 각 줄을 순회하며 처리
        
        for line in file:
            # strip() 메소드로 양쪽 공백 제거
            stripped_line = line.strip()
            
            # "http://"를 앞에 붙여서 결과 리스트에 추가
            processed_onions.append(f"http://{stripped_line}")
            
    processed_onions = processed_onions[665:]
            
   
    for url in processed_onions : 
        time.sleep(3)
        
        with open("./log.txt", "at+") as f :
            f.write(url + "\n")
        
        try :
            scheduler.run(url)
        except :
            with open("./bug.txt", "at+") as f :
                f.write(url + "\n")
            continue
        
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