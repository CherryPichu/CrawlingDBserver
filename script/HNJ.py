import graphviz
graphviz.version()
import pydot
import requests
from bs4 import BeautifulSoup
import json
import time

class Graph :
    def __init__(self) :
        self.graph = {}
        
    def addEdge(self, u, v) :
        if u not in self.graph :
            self.graph[u] = []
        self.graph[u].append(v)
    
    def printGraph(self) :
        for u in self.graph :
            print(u, end=" : ")
            for v in self.graph[u] :
                print(v, end=" ")
            print()

graph = Graph()
proxies = {
     'http' : "socks5h://uskawjdu.iptime.org:9052",
     'https' : "socks5h://uskawjdu.iptime.org:9052"
}         

visitedList = set()
def visit_onion(onion_link, depth : int):
    onion_link = onion_link.replace("#", "")
    onion_link = onion_link.replace("../", "/")
    
    if(depth == 0) :
        return
    
    print(onion_link)
    if visitedList.__contains__(onion_link) :
        print("visited : " + onion_link )
        return
    visitedList.add(onion_link)
    try :
        response = requests.get(onion_link, proxies=proxies, timeout=15)
        response.close()
    except :
        print("error : " + onion_link)
        return
    
    
    soup = BeautifulSoup(response.text, "html.parser")
    title = soup.title.__str__().replace("<title>", "").replace("</title>", "")
    
    atags = soup.find_all("a")
    hrefs = []
    for a in atags :
        href = a.get("href")
        if href != None :
            hrefs.append(href)
    # print(hrefs)
    for href in hrefs :
        href = href.replace("#", "")
        
        if "http://" in href or "https://" in href :
            graph.addEdge(onion_link, href)
            visit_onion(href, depth - 1)
            continue
        
        if href in onion_link :
            continue
        
        if href[0] == "/" :
            href = onion_link + href
        else :
            href = onion_link + "/" + href
            
  
            
        graph.addEdge(onion_link, href)
        visit_onion(href, depth - 1)
        
            
        


onion_link = "http://4t4ki52bkw46s6zfxnnlcnzrqjv4zdp5kwmqeqtouwbixuxp5kfcxyad.onion"
visit_onion(onion_link, 3)


dot = pydot.Dot( graph_type="digraph", rankdir="LR")

# 그래프 생성
for (u, vList) in graph.graph.items() :
    if u == "http://4t4ki52bkw46s6zfxnnlcnzrqjv4zdp5kwmqeqtouwbixuxp5kfcxyad.onion" :
        pydot.Node(u, fillcolor='#FF0000')
    else : 
        pydot.Node(u)
    for v in vList :
        edge = pydot.Edge(u, v, arrowhead='vee')
        dot.add_edge(edge)
dot.write_png('darkWeb.png')


