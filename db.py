import sqlite3

""" 테이블 정보
    NAME : HTML_FILES
        id integer primary key autoincrement, \
        origin_url varchar(50) not null \
        parameter varchar(50) not null \
        title varchar(50) not null, \
        url varchar(50) not null, \
        HTML TEXT, \
        isCrawling boolean not null)" \
"""

"""
    ref : https://gist.github.com/xeoncross/494947640a7dcfe8d91496988a5bf325
"""

DB_TABLE_NAME = "HTML_FILES"
class DBConn :
    def __new__(cls, *args, **kwargs) :
        """ 싱글톤 패턴 """
        if not hasattr(cls, "_instace") :
            cls._instace = super().__new__(cls)
        return cls._instace
    def __init__(self, dbName : str = "db.db" ) :
        self.conn = sqlite3.connect("./db/" + dbName)
        
    ## db
    """
        db.close()
    """
    def __del__(self) :
        pass
        # if self.conn != None : 
            # self.conn.close()
    
    ## get
    def query(self, sql : str, parameter : tuple = tuple()) -> bool :
        cursor = self.conn.cursor()
        cursor.execute(sql, parameter)
        self.conn.commit()
        # try :
        #     cursor = self.conn.cursor()
        #     cursor.execute(sql, parameter)
        #     self.conn.commit()
        # except :
        #     print("db.query error")
        return cursor
    
    def insert(self, sql : str, parameter : list) :
        cursor = self.conn.cursor()
        cursor.execute(sql, parameter)
        id = cursor.lastrowid # 뭔지 모르겠음
        self.conn.commit() # 반영
        cursor.close()
        
        return id
    
    def update(self, sql : str, parameter : list) :
        cursor = self.query(sql, parameter)
        rowcount = cursor.rowcount
        self.conn.commit()
        cursor.close()
        return rowcount
    
    
    def fetch(self, sql : str, parameter : list) :
        rows = []
        cursor = self.query(sql, parameter)
        if cursor.with_rows :
            rows = cursor.fetchall()
        cursor.close()
        return rows
    
    def fetchone(self, sql : str, parameter : list):
        row = None
        cursor = self.query(sql, parameter)
        if cursor.with_rows:
            row = cursor.fetchone()
        cursor.close()
        return row
    
class HtmlFileManager :
    def __init__(self, dbName : str = "db.db" ) :
        self.DB_TABLE_NAME = "HTML_FILES"
        self.dbcon = DBConn(dbName)
        self.OFFSET_ID = 0
        self.OFFSET_origin_url = 1
        self.OFFSET_origin_parameter = 2
        self.OFFSET_parameter = 3
        self.OFFSET_title = 4
        self.OFFSET_URL = 5
        self.OFFSET_HTML = 6
        self.OFFSET_ISCRAWLING = 7
        
        self.createTable()
        
        
    def __new__(cls, *args, **kwargs) :
        """ 
        싱글톤 패턴
        ref : https://wikidocs.net/69361 
        """
        if not hasattr(cls, "_instace") :
            cls._instace = super().__new__(cls)
        return cls._instace
    
    def __del__(self) :
        pass
    
    def getLastOneSelect(self) -> list :
        # result = list()
        sql = "select * from %s ORDER BY id DESC LIMIT 1" % (self.DB_TABLE_NAME)
        cursor = self.dbcon.query(sql, ())
        result = cursor.fetchone()
        
        return result
    
    def createTable(self) -> bool :
        sql = "CREATE TABLE if not exists %s ( \
            id integer primary key autoincrement, \
            origin_url varchar(50) not null, \
            parameter varchar(50) not null, \
            title varchar(50) not null, \
            url varchar(50) not null, \
            domain varchar(50) not null,  \
            HTML TEXT, \
            isCrawling boolean not null)" \
            % (self.DB_TABLE_NAME)
            
        self.dbcon.query(sql , ())
        
    def insertIntoTable(self, origin_url: str, parameter: str, title : str, 
                        url : str, domain : str, html : str, is_crawling : bool) -> bool  :
        # 만약 같은 url 이 is_craling = True 상태면 insert 를 하지 않음
        if self.getIsCrawlingUrl(url) :
            print("중복된 url")
            # return False
        
        sql = "INSERT INTO %s (origin_url, parameter, title, url, domain,  HTML, isCrawling) values (?, ?, ?, ?, ?, ?, ?)" % (self.DB_TABLE_NAME)
        cursor = self.dbcon.query(sql, (origin_url, parameter, title, url, domain, html, is_crawling))

        if cursor.rowcount != 0 :
            return True
        
        
    
    def dropTable(self) -> None :
        r = input("Are you sure that you drop a %s talbe? Y or N : ".format(self.DB_TABLE_NAME))
        if (r.upper() in "YES") != True :
            return
        
        sql = "DROP TABLE if exists %s" % (self.DB_TABLE_NAME)
        self.dbcon.query(sql)
        
        print("successful")
        
    
    def getLastAllSelect(self, number : int) -> list :
        """
        
        Parameters : 
            number (int) : 인자의 갯수만큼 가장 높은 ID 값 순으로 Select 해서 반환.
        
        Return :
            list : 반환 목록
        """
        sql = "select * from %s ORDER BY id DESC LIMIT %d" % (self.DB_TABLE_NAME, number)
        cursor = self.dbcon.query(sql, ())
        result = cursor.fetchall()
        
        return result
    
    def getIsCrawlingUrl(self, url :str) -> True:
        url = url.strip()
        sql = "select * from %s WHERE url = ? ORDER BY id DESC" % (self.DB_TABLE_NAME)
        cursor = self.dbcon.query(sql, (url, ))
        result = cursor.fetchall()
        
        return bool( sum([i[self.OFFSET_ISCRAWLING] for i in result]) ) 
    
    def getIsCrawlingTitle(self, title : str) -> True: # Not test
        title = title.strip()
        sql = "select * from %s WHERE Title = ? ORDER BY id DESC" % (self.DB_TABLE_NAME)
        cursor = self.dbcon.query(sql, (title, ))
        result = cursor.fetchall()
        
        return bool( sum([i[self.OFFSET_ISCRAWLING] for i in result]) ) 

    # def set(self) :


## ====== TEST CODE ======
if __name__ =="__main__" :
    
    dbhtml = HtmlFileManager()
    dbhtml.dropTable()
    dbhtml.createTable()
    
    dbhtml.insertIntoTable("origin_url", "parameter", "title", "naver.com2","domain", "html",  True)
    dbhtml.insertIntoTable("origin_url2", "parameter2", "title2", "url","domain", "html",  True)
    # print( dbhtml.getLastOneSelect() )
    
    print( dbhtml.getLastAllSelect(10) )
    # print(dbhtml.getIsCrawlingUrl("naver.com"))

    
    
    
    ## DB 생성
    
    # DB 삭제
    # sql = "Drop table if exists ?"
    # cursor = dbconn.query(sql, [DB_TABLE_NAME])
    
    # DB 조회
    # sql = "SELECT TABLE"
    