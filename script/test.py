import requests

baseurl = "https://cheiron-v1-auth.somma.kr/api/login"

data ={
    "id" : "test",
    "password" : ""
}

res = requests.post(baseurl, json=data)

print(res.text)

print(res.headers)