# 导入模块
import requests
url = "http://docs.python-requests.org/zh_CN/latest/_static/requests-sidebar.png"
response = requests.get(url)
with open('image.png','wb') as f:
  f.write(response.content)