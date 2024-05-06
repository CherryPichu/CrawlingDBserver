import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import json
from datetime import datetime
import hashlib

previous_url = None

def get_url_from_server():
    unique_value = datetime.now().strftime("%Y%m%d%H%M%S%f")
    try:
        response = requests.get("http://uskawjdu.iptime.org:8001/getUrl?name=TEST" + unique_value)
        data = response.json()
        url = data["url"]
        depth = data["Depth"]
        return url, depth, unique_value
    except Exception as e:
        print("Error getting URL from server:", e)
        return None, None, None

def visit_onion(onion_url, depth, unique_value):
    global previous_url
    
    proxies = {
        "http": "socks5h://127.0.0.1:9050",
        "https": "socks5h://127.0.0.1:9050"
    }
    if depth == 0:
        print("depth == 0입니다.")
        return 0
    try:
        response = requests.get(onion_url, proxies=proxies, allow_redirects=True)
        response.close()
    except Exception as e:
        print("에러발생: ", onion_url, e)
        # onion_url, depth, unique_value = get_url_from_server()
        # visit_onion(onion_url, depth, unique_value)
        return False
    
    if response.status_code == 200 and depth > 0:
        file_name = hashlib.sha256(onion_url.encode()).hexdigest() + ".html"
        fd = open(file_name, "wb")
        fd.write(response.content)
        fd.close()
        soup = BeautifulSoup(response.content, "html.parser")
        title = str(soup.title)
        
        parsed_url = urlparse(onion_url)
        protoident = parsed_url.scheme
        domain = parsed_url.netloc
        path = parsed_url.path
        query = parsed_url.query

        base_url = protoident + '://' + domain + path
        
        for link in soup.find_all('a'):
            aurl = link.get('href')
            if aurl and aurl.startswith("http"):
                visit_onion(aurl, depth - 1, unique_value)
        
        title = title.replace("<title>", "").replace("</title>", "")
        
        visible_text = ""
        for tag in soup.find_all(['p', 'h1', 'h2', 'h3', 'a', 'span']):
            visible_text += tag.get_text() + " "
        
        wordlist = list(set(visible_text.split()))
        
        db_input = {
            "name": "TEST" + unique_value,
            "origin_url": onion_url,
            "parameter": query,
            "title": title,
            "url": base_url,
            "domain": domain,
            "HTML": response.text, 
            "wordlist" : wordlist,
            "referer": previous_url if previous_url else "" 
        }
        
        print("Sending data:", db_input)
        
        # json_data = json.dumps(db_input)
        
        try:
            response = requests.post("http://uskawjdu.iptime.org:8001/postData", json=db_input)
            if response.status_code == 500:
                #print("Server returned an error, retrying crawling...")
                #visit_onion(onion_url, depth, unique_value)
                print("500에러")
            else:
                print("Response from server:", response.status_code)
        except Exception as e:
            print("Error sending data:", e)
            
    else:
        print("Crawling completed for URL:", onion_url)
        
    previous_url = onion_url
    return True

onion_url, depth, unique_value = get_url_from_server()

if onion_url:
    print("Crawling URL:", onion_url)
    visit_onion(onion_url, depth, unique_value)
    #visit_onion("http://1guy2biketrips.michaelahgu3sqef5yz3u242nok2uczduq5oxqfkwq646tvjhdnl35id.onion", 1, unique_value)
else:
    print("Failed to get URL from server.")