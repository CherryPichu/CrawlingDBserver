import requests, time, re, json, nltk
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag
from nltk.corpus import stopwords
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup

visited_url = set()

def visit_onion(onion_link, depth, max_depth, parent_link):
    if depth > max_depth:
        return
    
    proxies = {
        'http' : "socks5h://uskawjdu.iptime.org:9050",
        'https' : "socks5h://uskawjdu.iptime.org:9050"
    }
    
    a_link = []
    parent_urls = onion_link

    for child_url in parent_urls:
        if child_url in visited_url:
            #print(f"visitied url passed: {child_url}")
            continue
        
        try:
            response = requests.get(child_url, proxies=proxies, verify=False)
            response.close()
        except Exception as e:
            print(f"requests1 에러 발생: {e}")
            continue
        
        # 404일시 프로토콜 변경해서 한번 더 리퀘스트
        if re.match("4\\d{2}", str(response.status_code)):
            try:
                child_url = str(child_url).replace("http://", "https://")
                response = requests.get(child_url, proxies=proxies)
                response.close()
            except Exception as e:
                print(f"requests2 에러 발생: {e}")
                continue
        
        # a 태그 처리
        if re.match("2\\d{2}", str(response.status_code)):
            soup = BeautifulSoup(response.content, "html.parser")
            title = soup.title
            if title is None:
                title = ""
            else:
                title = title.text

            for a in soup.findAll("a"):
                href = a.get("href")

                if href is None or href.startswith("#") or href.startswith("javascript:") or len(href) == 0:
                    continue

                if href.startswith("//"):
                    href = "http:"+ href
                elif href.startswith("/"):
                    href = urljoin(child_url, href)
                    
                parsed_href = urlparse(href)
                if parsed_href.scheme == " " or parsed_href.netloc == "":
                    print("Not a valid URL:", href)
                    continue

                a_link.append(href)

            # 명사(noun)
            # 자연어 처리
            NN = []
            stop_words = set(stopwords.words("english"))
            for word in soup.get_text().replace("\t", "").replace("\xa0", " ").split("\n"):
                word = word.lower()
                tokens = word_tokenize(word)

                for token in tokens:
                    if token in stop_words:
                        continue
                    tagged_word = pos_tag([token])
                    word, pos = tagged_word[0]
                    if pos.startswith("NN") and len(word) < 20:
                        NN.append(word)
            #print(NN)
            
            parsed_url = urlparse(child_url)
            domain = parsed_url.netloc
            query = parsed_url.query

            data = {
                "origin_url": parent_link[0],
                "parameter": query,
                "title": title,
                "url": child_url,
                "domain": domain,
                "HTML": response.text,
                "wordlist" : json.dumps(NN),
                "isCrawling": True
            }
            
            
            try:
                response = requests.post("http://uskawjdu.iptime.org:8001/postData", json=data)
                response.close()
            except Exception as e:
                print(f"requests 에러 발생: {e}, http://uskawjdu.iptime.org:8001/postData")

            print(f"depth: {depth}, url: {child_url}, title: {title}")
            print("==================================================")

            visited_url.add(child_url)

    visit_onion(a_link, depth+1, max_depth, parent_link)
    time.sleep(1)


# def main():
#     nltk.download('punkt')
#     nltk.download('stopwords')
#     nltk.download('averaged_perceptron_tagger')
#     with open("C:\\Users\\ost09\\OneDrive\\바탕 화면\\다크웹 크롤러\\onions\\onions.txt", "rb") as f:
#         data = f.read()
#     for onion_link in data.decode("utf-8").split('\n'):
#         onion_link = "http://" + onion_link.replace("\n", "").replace(" ", "").replace("\r", "")
#         visit_onion([onion_link], 0, 1, onion_link)
#         visited_url.clear()


# if __name__ == "__main__":
    # try:
    #     main()
    #     print("all work done")
    # except KeyboardInterrupt:
    #     print("abort")
    
    
def main():
    url = "http://yq5jjvr7drkjrelzhut7kgclfuro65jjlivyzfmxiq2kyv5lickrl4qd.onion/"
    visit_onion([url],1, 2, [url])
    
    
if __name__ == "__main__":
    # nltk.download('averaged_perceptron_tagger')
    main()