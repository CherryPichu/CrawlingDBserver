import sqlite3
from bs4 import BeautifulSoup
import requests


con = sqlite3.connect("./db/sdev2-1.db")

cursor = con.cursor()
cursor.execute("create table relationship(src Text, src_title Text, dst Text_title Text)")

response = requests.get("https://www.naver.com")
response.close()
soup = BeautifulSoup(response.content, "html.parser")

for a in soup.find_all("a") :
    href = a["href"]
    # print(a["href"])
    print(href)
    if len(href) < 2 or href.startswitch("#") :
        continue
    




con.close()


