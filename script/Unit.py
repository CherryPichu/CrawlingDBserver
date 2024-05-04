from enum import Enum
from datetime import datetime

"""
    상태를 가지고 있어야지 일단
    현재 url
    그리고 크롤링
    
"""
class Unit :
    STOP = 0
    RUNNING = 1
    BUG = 2
    
    def __init__(self, id : int, unitName : str) :
        self.__processId = id
        self.name = unitName
        self.__url = ""
        self.__state = self.STOP
        self.craeteAt = datetime.now()
        
    # def setState(self, state) :
    #     if(state == self.STOP) :
    #         self.__state = self.STOP
    #     elif(state == self.RUNNING) :
    #         self.__state = self.RUNNING
    #     elif(state == self.BUG) :
    #         self.__state = self.BUG
            
    def getState(self) :
        return self.__state
    
    def getUnitId(self) :
        return self.__processId
        
    def activate(self, url) :
        self.__state = self.RUNNING
        self.__url = url
    
    def terminate(self) :
        self.__state = self.STOP
        
    def __str__(self) :
        result = "Unit ID : %d \nstate : %s \nname : %s\nurl : %s" \
            % (self.processId, self.__state, self.name, self.__url)
            
        return result

            
    # def __del__(self) :
        # self.

