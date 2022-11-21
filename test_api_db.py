import json

import requests

post = requests.post(
    "http://127.0.0.1:8888/insert",
    data=json.dumps(["author", "title", "description", "url", "pub_date"]),
)
print(post.status_code)

get_first = requests.get("http://127.0.0.1:8888/news")
print(get_first.status_code)

purge = requests.get("http://127.0.0.1:8888/purge")
print(purge.status_code)

get_second = requests.get("http://127.0.0.1:8888/news")
print(get_second.status_code)
