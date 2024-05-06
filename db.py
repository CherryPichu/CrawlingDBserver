import sqlite3
import json
""" 테이블 정보
    NAME : HTML_FILES
        id integer primary key autoincrement, \
        origin_url varchar(50) not null, \
        parameter varchar(50) not null, \
        title varchar(50) not null, \
        url varchar(50) not null, \
        domain varchar(50) not null,  \
        HTML TEXT, \
        isCrawling boolean not null)" \
"""

"""
    ref : https://gist.github.com/xeoncross/494947640a7dcfe8d91496988a5bf325
"""

DB_TABLE_NAME = "HTML_FILES"
class DBConn :
    def __init__(self, dbName : str = "db.db" ) :
        self.dbName = dbName
        self.conn = sqlite3.connect("./db/" + dbName, timeout=1)
        # self.conn.execute('UPDATE URL SET ownership = FALSE')
        
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

        return cursor
    
    
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
        self.OFFSET_parameter = 2
        self.OFFSET_title = 3
        self.OFFSET_URL = 4
        self.OFFSET_DOMAIN = 5
        self.OFFSET_HTML = 6
        self.OFFSET_wordlist = 7
        self.OFFSET_referer = 8
        self.OFFSET_CREATEAT = 9
        
        
        self.createTable()
        
        
    # def __new__(cls, *args, **kwargs) :
    #     """ 
    #     싱글톤 패턴
    #     ref : https://wikidocs.net/69361 
    #     """
    #     if not hasattr(cls, "_instace") :
    #         cls._instace = super().__new__(cls)
    #     return cls._instace
    
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
            HTML TEXT not null, \
            wordlist TEXT not null, \
            referer varchar(50) not null, \
            createAt datetime DEFAULT CURRENT_TIMESTAMP)" \
            % (self.DB_TABLE_NAME)
            
        self.dbcon.query(sql , ())
        
    def insertIntoTable(self, origin_url: str, parameter: str, title : str, 
                        url : str, domain : str, html : str, wordlist : list, referer : str) -> bool  :
        # 만약 같은 url 이 is_craling = True 상태면 insert 를 하지 않음
        if self.getIsCrawlingUrl(origin_url) :
            print("중복된 url")
            # return False
        
        wordlist = json.dumps(wordlist)
                
        sql = "INSERT INTO %s (origin_url, parameter, title, url, domain,  HTML, wordlist, referer) values (?, ?, ?, ?, ?, ?, ?, ?)" % (self.DB_TABLE_NAME)
        cursor = self.dbcon.query(sql, (origin_url, parameter, title, url, domain, html, wordlist, referer))
        
        if cursor.rowcount != 0 :
            return True
    
    def dropTable(self) -> None :
        r = input("Are you sure that you drop a %s talbe? Y or N : ".format(self.DB_TABLE_NAME))
        if (r.upper() in "YES") != True :
            return
        
        sql = "DROP TABLE if exists %s" % (self.DB_TABLE_NAME)
        self.dbcon.query(sql)
        
        print("successful")
        
    
    def __apply_load(self, wordlist) :
            
            return  
    
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
        
        
        for i in range(len(result)) :
                result[i] = list(result[i])
                result[i][self.OFFSET_wordlist] = json.loads( result[i][self.OFFSET_wordlist] )

        return result
    
    def getIsCrawlingUrl(self, url :str) -> True:
        url = url.strip()
        sql = "select * from %s WHERE origin_url = ? ORDER BY id DESC" % (self.DB_TABLE_NAME)
        cursor = self.dbcon.query(sql, (url, ))
        result = cursor.fetchall()
        
        return bool( len([_ for _ in result]) ) 
    
    # def getIsCrawlingTitle(self, title : str) -> True: # Not test
    #     title = title.strip()
    #     sql = "select * from %s WHERE Title = ? ORDER BY id DESC" % (self.DB_TABLE_NAME)
    #     cursor = self.dbcon.query(sql, (title, ))
    #     result = cursor.fetchall()
        
    #     return bool( sum([i[self.OFFSET_ISCRAWLING] for i in result]) ) 

class UrlManager :
    def __init__(self, dbName : str = "db.db" ) :
        self.DB_TABLE_NAME = "URL"
        self.dbcon = DBConn(dbName)
        self.OFFSET_ID = 0
        self.OFFSET_URL = 1
        self.OFFSET_ISCRAWLING = 2
        self.OFFSET_OWNERSHIP = 3
        self.OFFSET_CREATEAT = 4
        self.OFFSET_UPDATEAT = 5
        
        self.createTable()
        
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
            url varchar(50) not null, \
            isCrawling boolean not null, \
            ownership boolean not null, \
            createAt datetime DEFAULT CURRENT_TIMESTAMP, \
            updateAt datetime DEFAULT CURRENT_TIMESTAMP)" \
            % (self.DB_TABLE_NAME)
            
        self.dbcon.query(sql , ())
        
        check_trigger = "SELECT name FROM sqlite_master WHERE type=\"trigger\" AND \
            name = \"update_updateAt\";"
        isExist = self.dbcon.query(check_trigger).fetchone()
        
        if not isExist :
            update_trigger_query = " \
            CREATE TRIGGER update_updateAt \
            AFTER UPDATE ON %s \
            FOR EACH ROW \
            BEGIN \
                UPDATE %s\
                SET updateAt = DATETIME(\"now\") \
                WHERE id = OLD.id; \
            END; \
            " %(self.DB_TABLE_NAME,self.DB_TABLE_NAME)
            
            self.dbcon.query(update_trigger_query, ())
        

    def insertIntoTable(self, url : str, isCrawling : bool, ownership : bool = False) -> bool  :
        """
         이 함수는 이미 DB에 등록된 URL의 경우 아무런 처리를 하지 않습니다.
         isCrawling 상태를 변경하기 원할경우 updateTable을 이용하세요
        """
        if self.findByUrl(url) != None :
            return False
        sql = "INSERT INTO %s (url, isCrawling, ownership) values (?, ?, ?)" % (self.DB_TABLE_NAME)
        cursor = self.dbcon.query(sql, (url, isCrawling, ownership))
        
        if cursor.rowcount != 0 :
            return True
        return False
    
    def updateByUrl(self, url : str, isCrawling : bool) -> bool :
        if self.findByUrl(url) == None :
            return False
        sql = "UPDATE %s SET isCrawling = ? WHERE url = ?"% (self.DB_TABLE_NAME)
        cursor = self.dbcon.query(sql, (isCrawling, url))
        
        if cursor.rowcount != 0 :
            return True
        return False
    
    def updateById(self, id : str, isCrawling : bool) -> bool :
        if self.findById(id) == None :
            return False
        sql = "UPDATE %s SET isCrawling = ? WHERE id = ?"% (self.DB_TABLE_NAME)
        cursor = self.dbcon.query(sql, (isCrawling, id))

        if cursor.rowcount != 0 :
            return True
        return False
    
    def findByUrl(self, url : str) -> list :
        sql = "select * from %s WHERE url = ? LIMIT 1" % (self.DB_TABLE_NAME)
        cursor = self.dbcon.query(sql, (url, ))
        result = cursor.fetchone()
            
        return result
    
    def findById(self, id : str) -> list :
        sql = "select * from %s WHERE id = ? LIMIT 1" % (self.DB_TABLE_NAME)
        cursor = self.dbcon.query(sql, (id, ))
        result = cursor.fetchone()
            
        return result
    
    def dropTable(self) -> None :
        r = input("Are you sure that you drop a %s talbe? Y or N : ".format(self.DB_TABLE_NAME))
        if (r.upper() in "YES") != True :
            return
        
        sql = "DROP TABLE if exists %s" % (self.DB_TABLE_NAME)
        self.dbcon.query(sql)
        
        print("successful")
        
    def updateOwnership(self, dbIndex : int, ownership : bool) :
        sql = "update %s SET ownership = ? WHERE id = ?" % (self.DB_TABLE_NAME)
        self.dbcon.query(sql, (ownership, dbIndex))
        
    def getOnionUrl(self, dbIndex : int) -> tuple :
        if dbIndex >= 0 : # 이미 점유중인 index 해제
            self.updateOwnership(dbIndex, False)
        
        # 1순위. 크롤링이 되지 않은 URL 을 가져온다. ORDER BY RANDOM() / ORDER BY createAt
        sql = """
            Select * from %s WHERE isCrawling = FALSE AND ownership = FALSE ORDER BY RANDOM() DESC LIMIT 1;
        """% (self.DB_TABLE_NAME)
        cursor = self.dbcon.query(sql, ())
        result = cursor.fetchone()
        
        if result != None :
            ## ownership = True 설정
            self.updateOwnership(result[self.OFFSET_ID], True)
            return result[self.OFFSET_ID], result[self.OFFSET_URL] 
        
        # # # 2순위. UpdateAt 날짜가 가장 늦은 놈을 가져온다.
        sql = """
            Select * from %s ORDER BY updateAt ASC LIMIT 1;
        """% (self.DB_TABLE_NAME)
        cursor = self.dbcon.query(sql, ())
        result = cursor.fetchone()
        
        self.updateOwnership(result[self.OFFSET_ID], True)
        return result[self.OFFSET_ID], result[self.OFFSET_URL] 
        
        
        
        


## ====== TEST CODE ======
if __name__ =="__main__" :
    
    
    dbhtml = HtmlFileManager()
    dbhtml.dropTable()
    # dbhtml.createTable()
    
    # dbhtml.insertIntoTable("origin_url", "parameter", "title", "naver.com2","domain", "html", ["문자열1", "문자열2"] , True)
    # dbhtml.insertIntoTable("origin_url2", "parameter2", "title2", "url","domain", "html",  True)
    # print( dbhtml.getLastOneSelect() )
    
    # print( dbhtml.getLastAllSelect(10) )
    # print(dbhtml.getIsCrawlingUrl("naver.com"))
    
    urldb = UrlManager()
    urldb.dbcon.conn.execute('UPDATE URL SET ownership = FALSE')
    urldb.dbcon.conn.execute('UPDATE URL SET isCrawling = FALSE')
    urldb.dbcon.conn.commit()
    # urldb.dropTable()
    # urldb.insertIntoTable("naver.com4", True)
    # res = urldb.updateTableByUrl("naver.com4", False)
    # print(res)
    
    # print( urldb.getLastOneSelect() )
    # print( urldb.getOnionUrl() )



    
    
    
    ## DB 생성
    
    # DB 삭제
    # sql = "Drop table if exists ?"
    # cursor = dbconn.query(sql, [DB_TABLE_NAME])
    
    # DB 조회
    # sql = "SELECT TABLE"
    