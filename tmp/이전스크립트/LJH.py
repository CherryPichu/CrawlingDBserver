import requests
from bs4 import BeautifulSoup
import sys
from urllib.parse import urlparse
import json

def visit_onion(onion_url):
    proxies = {
        "http" : "socks5h://uskawjdu.iptime.org:9050",
        "https" : "socks5h://uskawjdu.iptime.org:9050"
    }
    aurl_list = []
    db_input = []
    
    try:
        response = requests.get(onion_url, proxies=proxies, allow_redirects=True, verify=False)
        response.close()
    except Exception as e:
        print(onion_url, e)
        return False
    
    if response.status_code == 200:
        # fd = open(onion_url[7:] + ".html", "wb")
        # fd.write(response.content)
        # fd.close()
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
            aurl_list.append(aurl)
        
        title = title.replace("<title>","").replace("</title>", "")
        
        # Extract visible text from certain HTML elements
        visible_text = ""
        for tag in soup.find_all(['p', 'h1', 'h2', 'h3', 'a', 'span']):
            visible_text += tag.get_text() + " "
        
        # Split text into words and remove duplicates
        wordlist = list(set(visible_text.split()))
        
        db_input = {
            "origin_url": onion_url,
            "parameter": query,
            "title": title,
            "url": base_url,
            "domain": domain,
            "HTML": visible_text,  # Saving visible text instead of full HTML
            "wordlist" : json.dumps( wordlist),
            "isCrawling": True
        }
        
        # print("Sending data:", db_input)
        
        # Convert dictionary to JSON
        json_data = db_input
        
        # Send POST request
        try:
            response = requests.post("http://uskawjdu.iptime.org:8001/postData", json=json_data)
            print(response.text)
            print("Response from server:", response.status_code)
            response.close()
        except Exception as e:
            print("Error sending data:", e)
            
    else:
        print(onion_url, response.status_code, response.headers)
    return True
    
# tmp_list = []
# onion_url = sys.argv[1]
# visit_onion(onion_url)

def main():
    url = "http://yq5jjvr7drkjrelzhut7kgclfuro65jjlivyzfmxiq2kyv5lickrl4qd.onion/"
    visit_onion(url)
    
if __name__ == "__main__":
    main()
    
    
    