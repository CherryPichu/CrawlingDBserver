import requests, re, pydot, sys, time, json

from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag
from nltk.corpus import stopwords
from urllib.parse import urlparse, urlsplit
from bs4 import BeautifulSoup

UNIQUENAME = "KHS"
MAIN_DEPTH = -1
# global MAIN_DEPTH
from urllib.parse import urlparse, urlsplit
def is_image_url(url):
    # 이미지 파일 확장자 목록
    image_extensions = ['.gif', '.jpg', '.jpeg', '.png', '.bmp', '.tiff']
    # URL에서 경로 부분을 분리
    path = urlsplit(url).path
    # 경로의 마지막 부분이 이미지 확장자 중 하나와 일치하는지 확인
    return any(path.endswith(ext) for ext in image_extensions)
               
whole_pages = set()
graph = pydot.Dot("relation", graph_type = "digraph", rankdir="LR")

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
    # print(NN)
    return NN

def visit_onion(onion_urls, depth, referer):
    if depth == 0:
        return
    
    new_links = []  # 새 링크 저장
    proxies = {
        'http' : "socks5h://uskawjdu.iptime.org:9051",
        'https' : "socks5h://uskawjdu.iptime.org:9051"
    }
    headers = {
        "Content-Type": "application/json"
    }

    for onion_url in onion_urls:
        if onion_url in whole_pages:
            continue  # 이미 방문한 URL은 스킵

        data = {
            "name" : UNIQUENAME,
            "origin_url": onion_url,
            "parameter": urlparse(onion_url).query,
            "title": "",
            "url": urlparse(onion_url).scheme + '://' + urlparse(onion_url).netloc + urlparse(onion_url).path,
            "domain": urlparse(onion_url).netloc,
            "HTML": "",
            "referer":referer,
            "wordlist": []
        }
        
        response = None
        try:
            if not onion_url.startswith(('http://', 'https://')):
                onion_url = 'http://' + onion_url
                
            if is_image_url(onion_url) :
                continue
            
            response = requests.get(onion_url, headers=headers, proxies=proxies, allow_redirects=True)
            response.encoding = response.apparent_encoding  # 인코딩 명시적 설정
            response.close()
            
            if re.match("4\\d{2}", str(response.status_code)):
                onion_url = str(onion_url).replace("http://", "https://")
                response = requests.get(onion_url, headers=headers, proxies=proxies, allow_redirects=True)
                response.encoding = response.apparent_encoding  # 인코딩 명시적 설정
                response.close()
            if re.match("4\\d{2}", str(response.status_code)):
                continue
            time.sleep(1)
        except requests.RequestException as e:
            print(f"{onion_url}에서 에러 발생: {e}")
            data = {
                "name" : UNIQUENAME,
                "origin_url": onion_url,
                "parameter": "",
                "title": "null",
                "url": onion_url,
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
        
        if re.match("2\\d{2}", str(response.status_code)):
            soup = BeautifulSoup(response.content, "html.parser")
            
            if soup.title is not None:
                title = str(soup.title)
                data['title'] = title
            
            data['HTML'] = response.text

            text_nodes = soup.find_all(text=True)
            cleaned_texts = [re.sub(r'\s+', ' ', text).strip() for text in text_nodes if text.strip()]
            NNs = get_NNs(cleaned_texts)
            data['wordlist'] = json.dumps(NNs)


            for a in soup.find_all("a"):
                href = a.get("href")
                
                if href is None or str(href).startswith("#") or str(href).startswith("javascript:") or len(href) == 0:
                    continue

                if href.startswith("//"):
                    href = "http:"+ href
                elif href.startswith("/"):
                    href = urljoin(onion_url, href)
            
                new_links.append(href)  # 새로운 링크 추가
            
            try:
                response = requests.post("http://uskawjdu.iptime.org:8001/postData", json=data)
                response.close()
            except Exception as e:
                print(f"requests 에러 발생: {e}, http://uskawjdu.iptime.org:8001/postData")

            whole_pages.add(onion_url)  # URL 방문 기록

            if referer != "":
                # graph.add_edge(pydot.Edge(referer, onion_url))
                print(f"PNG Updated: {referer} -> {onion_url}")
                # graph.write_png("relation.png")
        else:
            print(onion_url, response.status_code, response.headers)

    depth -= 1  # 재귀 깊이 감소
    if len(new_links) > 0:
        new_links = list(new_links)
        visit_onion(new_links, depth, referer)

def main():
    
    getUrl = "http://uskawjdu.iptime.org:8001/getUrl?name=%s" %(UNIQUENAME)
    try:
        response = requests.get(getUrl)
        response.close()
    except requests.RequestException as e:
        print(f"requests 에러 발생: {e}")
        print("==================================================")
    arg= response.json()["url"]
    depth= response.json()["Depth"]
    MAIN_DEPTH = depth
        
    if len(sys.argv) >= 0:
        # arg = sys.argv[1]
        visit_onion([arg], depth, "")
        # graph.write_png("relation.png")
    else:
        print("인자가 제공되지 않았습니다.")

if __name__ == "__main__":
    main()