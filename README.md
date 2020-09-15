### 0. 前言

网络爬虫（又被称为网页蜘蛛，网络机器人，在FOAF社区中间，更经常的称为网页追逐者），是一种按照一定的规则，自动的抓取万维网信息的程序或者脚本。

我认为一次爬虫的过程, 就是网络请求到数据后, 处理数据, 然后发送数据的过程.

<!-- more -->

### 1. 网络请求(requests)

 python网络请求主要有 `urllib` 和 `requests`  库, 墙裂推荐`requests`

```python
import requests

url = 'http://www.baidu.com'
response = requests.get(url)
html = response.text
print(html)


import requests

url = "http://docs.python-requests.org/zh_CN/latest/_static/requests-sidebar.png"
response = requests.get(url)
with open('image.png','wb') as f:
  f.write(response.content)
```



### 2. 数据提取 (pyquery)

一般我们请求的数据主要分以下几类:

+ html, xml
+ json
+ 字符串

对于 html, xml 我们要使用相关的库进行处理, json直接反序列化处理, 字符串可能需要字符串匹配 和 正则表达式 处理



> 对html/xml 处理的库主要有以下几种:

##### 2.1 beautifulsoup

```bash
pip install beautifulsoup4
```

beautiful Soup将复杂HTML文档转换成一个复杂的树形结构,每个节点都是Python对象

##### 2.2 lxml

lxml 使用的是 xpath 技术

```bash
pip install lxml
```

##### 2.3  lxml, beautifulSoup 对比

BeautifulSoup是一个库，而XPath是一种技术，python中最常用的XPath库是lxml，因此，这里就拿lxml来和BeautifulSoup做比较吧.

+ 性能 lxml >> BeautifulSoup

BeautifulSoup和lxml的原理不一样，BeautifulSoup是基于DOM的，会载入整个文档，解析整个DOM树，因此时间和内存开销都会大很多。而lxml只会局部遍历，另外lxml是用c写的，而BeautifulSoup是用python写的，因此性能方面自然会差很多。

+ 易用性 BeautifulSoup >> lxml

BeautifulSoup用起来比较简单，API非常人性化，支持css选择器。lxml的XPath写起来麻烦，开发效率不如BeautifulSoup。

```
title = soup.select('.content div.title h3')
```

同样的代码用Xpath写起来会很麻烦

```
title = tree.xpath("//*[@class='content']/div[@class='content']/h3")
```

##### 2.4. pyquery 

pyquery 可让你用 jQuery 的语法来对 html/xml 进行操作。这和 jQuery 十分类似。这个库不是（至少还不是）一个可以和 JavaScript交互的代码库，它只是非常像 jQuery API 而已。

```bash
pip install pyquery
```

我们可以看下面这个例子:

```python
    def parse_html(self,content):
        doc = pq(content)
        items = doc(".dt").items()
        for item in items:
            title = item.find("center").text()
            for i in item.find("th").items():
                category = i.find("a").eq(0).text()
                neirong = i.find("a").eq(1).text()
                url = i.find("a").eq(1).attr('href')

                one_data = {
                    "category": category,
                    "context": neirong,
                    "url": url,
                }
                print(one_data)
```



### 3. 无头浏览器(pyppeteer)

以前写爬虫，遇到需要登录的页面，一般都是通过chrome的检查元素，查看登录需要的参数和加密方法，如果网站的加密非常复杂，例如登录qq的，就会很蛋疼。

现在有了无头浏览器，再也不需要考虑登录的参数和加密了，用无头浏览器打开页面，通过JS或JQuery语句，填入账号和密码，然后点击登陆，然后把Cookies保存下来，就可以模拟登陆了。



##### 3.1 PhantomJS(暂停开发)

```
serWarning: Selenium support for PhantomJS has been deprecated, please use headless versions of Chrome or Firefox instead

新版本的Selenium不再支持PhantomJS了，请使用Chrome或Firefox的无头版本来替代。
```



PhantomJS是一个无界面的,可脚本编程的WebKit浏览器引擎。它原生支持多种web 标准：DOM 操作，CSS选择器，JSON，Canvas 以及SVG。因此可以比浏览器更加快速的解析处理js加载。



有时，我们需要浏览器处理网页，但并不需要浏览，比如生成网页的截图、抓取网页数据等操作。[PhantomJS](http://phantomjs.org/)的功能，就是提供一个浏览器环境的命令行接口，你可以把它看作一个“虚拟浏览器”，除了不能浏览，其他与正常浏览器一样。它的内核是WebKit引擎，不提供图形界面，只能在命令行下使用，我们可以用它完成一些特殊的用途。



下载: https://phantomjs.org/download.html , 然后把二进制放到一个目录下, 增加个$PATH 指定即可

```
phantomjs -v
```



##### 3.2. selenium

selenium 是什么？一句话，自动化测试工具。它支持各种浏览器，包括 Chrome，Safari，Firefox 等主流界面式浏览器。换句话说叫 Selenium 支持这些浏览器驱动。话说回来，PhantomJS不也是一个浏览器吗，那么 Selenium 支持不？答案是肯定的，这样二者便可以实现无缝对接了。有人问，为什么不直接用浏览器而用一个没界面的 PhantomJS 呢？答案是：效率高！



嗯，所以呢？安装一下 Python 的 Selenium 库，再安装好 PhantomJS，不就可以实现 Python＋Selenium＋PhantomJS 的无缝对接了嘛！Selenium 用来驱动浏览器, PhantomJS 用来渲染解析界面, Python 进行后期的处理，完美的三剑客！



```
pip install selenium
```



然后我们看一个例子, 通过 selenium 驱动 [chrome driver](https://sites.google.com/a/chromium.org/chromedriver/downloads)打开百度搜索关键词

```python
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

browser = webdriver.Chrome(executable_path="./drivers/chromedriver")
browser.get('http://www.baidu.com/')

kw = browser.find_element_by_id("kw")
kw.send_keys("Selenium", Keys.RETURN)
```



##### 3.3. pyppeteer 

pyppeteer 是依赖于 chromium 这个浏览器来运行的,  并且是基于 python 的新特性 async 实现的，所以它的一些执行也支持异步操作，效率相对于 selenium 来说也提高了。

```bash
pip3 install pyppeteer
```

我们可以来看下面这个例子, 是打开baidu 后截图

```python
import asyncio
from pyppeteer import launch

async def main():
    browser = await launch()
    page = await browser.newPage()
    await page.goto('http://www.baidu.com')
    await page.screenshot({'path': 'example.png'})
    await browser.close()

asyncio.get_event_loop().run_until_complete(main())
```



### 4. 爬虫框架



##### 4.1 pyspider

pyspider上手更简单，操作更加简便，因为它增加了 WEB 界面，写爬虫迅速，集成了phantomjs，可以用来抓取js渲染的页面。

```bash
pip install pyspider
```

安装成功后在 [python 3.7 下运行就报错](https://github.com/binux/pyspider/issues/817), 看来作者很久没维护了




##### 4.2 scrapy

```bash
pip install Scrapy
```

scrapy自定义程度高，比 PySpider更底层一些，适合学习研究，需要学习的相关知识多，不过自己拿来研究分布式和多线程等等是非常合适的。



### 5. 爬虫其他(TODO)

##### 5.1 多线程

 thread 库

##### 5.2 多进程

multiprocessing 库



### 6. 参考资料

+ https://cuiqingcai.com/1052.html
+ https://cuiqingcai.com/6942.html
+ https://github.com/Kr1s77/Python-crawler-tutorial-starts-from-zero
