from db import UrlManager

if __name__ == "__main__":
    processed_onions = []

    urldb = UrlManager()
    # 파일을 읽기 모드로 열기
    with open("./onions.txt", 'r') as file:
        # 각 줄을 순회하며 처리
        
        for line in file:
            # strip() 메소드로 양쪽 공백 제거
            stripped_line = line.strip()
            
            
            # "http://"를 앞에 붙여서 결과 리스트에 추가
            urldb.insertIntoTable(f"http://{stripped_line}", False)
            
    
    
    