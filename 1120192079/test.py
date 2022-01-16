import requests
import os

url = "https://img2020.cnblogs.com/blog/1744409/202201/1744409-20220112155511412-749056801.png"

r = requests.get(url)
target_filename = './' + os.path.basename(url)
with open(target_filename,"wb") as my:
    my.write(r.content)