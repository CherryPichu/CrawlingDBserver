import requests
from bs4 import BeautifulSoup
import sys, re, json

def visit_onion(onion_url):
    proxies = {
        "http" : "socks5h://uskawjdu.iptime.org:9050",
        "https" : "socks5h://uskawjdu.iptime.org:9050"
    }
    try:
        response = requests.get(onion_url, proxies=proxies, allow_redirects=True, verify=False)
        response.close()
    except Exception as e:
        print(onion_url, e)
        return False
    if response.status_code == 200:
        if "https" in onion_url:
            protocol_index = 8
        else:
            protocol_index = 7

        param_index = onion_url.find("?")
        if param_index > 0:
            parameter = onion_url[param_index:]
            url_buffer = onion_url[:param_index]
        else:
            parameter = ""
            url_buffer = onion_url

        domain_index = url_buffer[protocol_index:].find("/")
        if domain_index > 0:
            domain = url_buffer[protocol_index:domain_index]
        else:
            domain = url_buffer[protocol_index:]
        
        # with open(url_buffer[protocol_index:] + ".html", "wb") as f:
        #     f.write(response.content)

        soup = BeautifulSoup(response.content, "html.parser")
        title = str(soup.title)
        title = title.replace("<title>","").replace("</title>", "")

        text_without_punctuation = re.sub(r'[^\w ]', '', soup.text)
        words = text_without_punctuation.split()

        child_domain = []
        for a_tag in soup.find_all('a'):
            child_domain.append(a_tag.get('href'))

      
        row = {
            'origin_url': onion_url,
            'parameter': parameter, 
            'title': title,
            'url': url_buffer,
            'domain': domain,
            "HTML": response.text,
            "wordlist": json.dumps( words),
            "isCrawling": True
        }
        # print(row)
        response = requests.post("http://uskawjdu.iptime.org:8001/postData", json=row)
        # print(response.text)
        response.close()
        
        if( response.status_code != 200) :
            return False
        
    else:
        print(onion_url, response.status_code, response.headers)
    return True
    
def main():
    url = "yq5jjvr7drkjrelzhut7kgclfuro65jjlivyzfmxiq2kyv5lickrl4qd.onion/"
    visit_onion(url)
if __name__ == "__main__":
    main()
    