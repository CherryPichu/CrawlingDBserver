import requests, time, re, json, nltk, pydot, os
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag
from nltk.corpus import stopwords
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
UNIQUENAME = "OST"

# global MAIN_DEPTH
from urllib.parse import urlparse, urlsplit
def is_image_url(url):
    # 이미지 파일 확장자 목록
    image_extensions = ['.gif', '.jpg', '.jpeg', '.png', '.bmp', '.tiff']
    # URL에서 경로 부분을 분리
    path = urlsplit(url).path
    # 경로의 마지막 부분이 이미지 확장자 중 하나와 일치하는지 확인
    return any(path.endswith(ext) for ext in image_extensions)

os.environ["PATH"] += os.pathsep + "C:\\Program Files\\Graphviz\\bin\\"

visited_url = set()
graph = pydot.Dot(graph_type = "digraph", rankdir="LR")

def requests_(url, headers=None, proxies=None):
    response = None
    # print(url)
    try:
        response = requests.get(url, headers=headers, proxies=proxies)
        response.close()
    except requests.RequestException as e:
        print(f"requests 에러 발생: {e}")
        print("==================================================")

    return response


def get_links_title(html, url):
    links = []
    soup = BeautifulSoup(html, "html.parser")
    title = ""

    if soup.title is not None:
        title = soup.title.text

    for a in soup.find_all("a"):
        href = a.get("href")
        
        if href is None or str(href).startswith("#") or str(href).startswith("javascript:") or len(href) == 0:
            continue

        if href.startswith("//"):
            href = "http:"+ href
        elif href.startswith("/"):
            href = urljoin(url, href)
                    
        # parsed_href = urlparse(href)
        # if parsed_href.scheme == " " or parsed_href.netloc == "":
        #     print("Not a valid URL:", href)
        #     continue
        links.append(href)

    return soup, title, links


def get_NNs(texts):
    # 명사(noun)
    # 자연어 처리
    NN = []
    stop_words = set(stopwords.words("english"))
    for word in texts:
        word = word.lower()
        tokens = word_tokenize(word)

        for token in tokens:
            if token in stop_words:
                continue
            tagged_word = pos_tag([token])
            word, pos = tagged_word[0]
            if pos.startswith("NN") and len(word) < 20 and len(word) > 2:
                NN.append(word)
    print(NN)
    return NN


def visit_onion(onion_link, depth, max_depth, origin_url, parent_link=None):
    if depth > max_depth:
        return
    print(onion_link)
    # print("=============== debug ===============")
    a_link = None
    child_url = None
    referer = parent_link
    proxies = {
        'http' : "socks5h://uskawjdu.iptime.org:9050",
        'https' : "socks5h://uskawjdu.iptime.org:9050"
    }

    if not isinstance(onion_link, list):
        onion_link = [onion_link]
        
    for child_url in onion_link:
        child_url = child_url

        if child_url in visited_url:
            #print(f"visitied url passed: {child_url}")
            continue
        if is_image_url(child_url) :
                continue
        response = requests_(child_url, proxies=proxies)
        if  depth != 0 and  response is None:
            continue
        
        if depth == 0 and  response is None :
            print("응답없음")
            data = {
                "name" : UNIQUENAME,
                "origin_url": child_url,
                "parameter": "",
                "title": "null",
                "url": child_url,
                "domain": "",
                "HTML": "",
                "wordlist" : "[]",
                "referer" : ""
            }
            try:
                response = requests.post("http://uskawjdu.iptime.org:8001/postData", json=data)
                response.close()
            except Exception as e:
                print(f"requests 에러 발생: {e}, http://uskawjdu.iptime.org:8001/postData")
            continue
            

        # 404일시 프로토콜 변경해서 한번 더 리퀘스트
        if re.match("4\\d{2}", str(response.status_code)):
            print("change protocol and request one more")
            child_url = str(child_url).replace("http://", "https://")
            response = requests_(child_url, proxies=proxies)
            if response is None:
                print("changed protocol but not connected")
                continue

        if re.match("2\\d{2}", str(response.status_code)):
            soup, title, href = get_links_title(response.content, child_url)
            a_link = href

            texts = soup.get_text().replace("\t", "").replace("\xa0", " ").split("\n")
            NNs = get_NNs(texts)

            # print(f"depth: {depth}, url: {child_url}, title: {title}, referer: {referer}")
            print("==================================================")
            
            parsed_url = urlparse(child_url)
            domain = parsed_url.netloc
            query = parsed_url.query

            if referer == None :
                referer = ""
                
            data = {
                "name" : UNIQUENAME,
                "origin_url": origin_url,
                "parameter": query,
                "title": title,
                "url": child_url,
                "domain": domain,
                "HTML": response.text,
                "wordlist" : json.dumps(NNs),
                "referer" : referer
            }
            # print(data)

            try:
                response = requests.post("http://uskawjdu.iptime.org:8001/postData", json=data)
                response.close()
            except Exception as e:
                print("error url : ", child_url)
                print(f"requests 에러 발생: {e}, http://uskawjdu.iptime.org:8001/postData")

            visited_url.add(child_url)

            if referer is not None:
                graph.add_edge(pydot.Edge(referer, child_url))

    visit_onion(a_link, depth+1, max_depth, origin_url=origin_url, parent_link=child_url)
    time.sleep(1)


def main():
    nltk.download('punkt')
    nltk.download('stopwords')
    nltk.download('averaged_perceptron_tagger')
    
    server_path = "http://uskawjdu.iptime.org:8001/getUrl?name=%s" %(UNIQUENAME)
    origin_url = requests_(server_path)
    if origin_url is None:
        return
    origin_url_json = origin_url.json()
    visit_onion(origin_url_json["url"], 0, origin_url_json["Depth"], origin_url=origin_url_json["url"])


if __name__ == "__main__":
    try:
        main()
        print("all work done")
    except KeyboardInterrupt:
        print("abort")