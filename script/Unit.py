from enum import Enum
from datetime import datetime

"""
    상태를 가지고 있어야지 일단
    현재 url
    그리고 크롤링
    
"""
class Unit :
    def __init__(self, unitName : str) :
        
        self.STOP : int= 0
        self.RUNNING : int= 1
        self.BUG : int= 2
    
        self.name = unitName
        self.__url = ""
        self.__dbIndex = -1
        self.__state = self.STOP
        self.craeteAt = datetime.now()

    def getState(self) :
        return self.__state
    
        

    def getUrlRow(self) -> list :
        """
        [0] : dbIndex
        [1] : name
        """
        return [self.__dbIndex,  self.__url]
        
    def activate(self, dbIndex : int, url : str) :
        self.__state = self.RUNNING
        self.__url = url
        self.__dbIndex = dbIndex
    
    def terminate(self) :
        self.__state = self.STOP
        self.__url = ""
        self.__dbIndex = -1
        
    def __str__(self) :
        result = "Unit Name : %d \nstate : %s \nurl : %s" \
            % (self.name, self.__state, self.__url)
            
        return result

            
    # def __del__(self) :
        # self.

