import KHS, LJH, Min, OST
from functools import wraps
import errno
import os
import signal

class TimeoutError(Exception):
    pass

def timeout(seconds=10, error_message=os.strerror(errno.ETIME)):
    def decorator(func):
        def _handle_timeout(signum, frame):
            raise TimeoutError(error_message)

        def wrapper(*args, **kwargs):
            signal.signal(signal.SIGALRM, _handle_timeout)
            signal.setitimer(signal.ITIMER_REAL,seconds) #used timer instead of alarm
            try:
                result = func(*args, **kwargs)
            finally:
                signal.alarm(0)
            return result
        return wraps(func)(wrapper)
    return decorator


class Scheduler :
    """
        말만 스케줄러이고 실제로는 동기 방식임.
        상식적으로 이렇게 비효율적인 스케줄러를 구현하는 것이 말이 안됨.
    """
    def __init__(self) :    
        self.INIT = 0
        self.RUNNING = 1
        self.FAILED = -1
        
        self.RUN_INDEX = 0
        self.crawler_list = [LJH.visit_onion, Min.visit_onion, OST.visit_onion, KHS.visit_onion]    
        self.crawler_length = self.crawler_list.__len__()
        self.crewler_status = [self.INIT, self.INIT, self.INIT, self.INIT, self.INIT]
        
    @timeout(20)
    def run(self, url : str) :
        # 대충.. 무슨 의미가 있는지..
        self.crawler_list[self.RUN_INDEX]
        self.RUN_INDEX = (self.RUN_INDEX + 1) % (self.crawler_length)
        
        self.crewler_status[self.RUN_INDEX] = self.RUNNING
        
        print("%d 번 스케줄러 차례" % (self.RUN_INDEX))
        
        if(self.RUN_INDEX == 3) :
            self.crawler_list[self.RUN_INDEX]([url], 1, "")
        elif(self.RUN_INDEX == 2) :
            self.crawler_list[self.RUN_INDEX]([url], 1, 2, [url])
        else :
            self.crawler_list[self.RUN_INDEX](url)
        
        
        
        self.crewler_status[self.RUN_INDEX] = self.INIT
        

    
import requests
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
            
            
    for url in processed_onions : 
        scheduler.run(url)
        
   