# Week01：使用Python库获取豆瓣影评

Table of Contents

=================



  \* [Week01：使用Python库获取豆瓣影评](#week01使用python库获取豆瓣影评)

   \* [0. pip安装提速技巧](#0-pip安装提速技巧)

​     \* [0.1 常用 pip 源地址](#01-常用-pip-源地址)

​     \* [0.2 修改方式](#02-修改方式)

   \* [1. Python基础语法的介绍](#1-python基础语法的介绍)

   \* [2. 前端基础知识](#2-前端基础知识)

​     \* [2.1 网页的三个组成部分](#21-网页的三个组成部分)

​     \* [2.2 HTTP协议](#22-http协议)

​     \* [2.3 XPath](#23-xpath)

   \* [3. Scrapy框架](#3-scrapy框架)

​     \* [3.1 Scrapy框架结构解析](#31-scrapy框架结构解析)

​     \* [3.2 Scrapy框架目录解析](#32-scrapy框架目录解析)

​     \* [3.3 爬虫器的启动](#33-爬虫器的启动)

   \* [4. 作业总结](#4-作业总结)

## 0. pip安装提速技巧

### 0.1 常用 pip 源地址

- 豆瓣： https://pypi.doubanio.com/simple/
- 清华： https://mirrors.tuna.tsinghua.edu.cn/help/pypi/
- 中科大： https://pypi.mirrors.ustc.edu.cn/simple/
- 阿里云： https://mirrors.aliyun.com/pypi/simple/

### 0.2 修改方式

- **临时替换**

```shell
pip install -i some-package
```

- **永久替换（先升级 pip：pip install pip -U ）**

```shell
pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
```

## 1. Python基础语法的介绍

**Python 简介：** https://docs.python.org/zh-cn/3.7/tutorial/introduction.html

**Python 数据结构：** https://docs.python.org/zh-cn/3.7/tutorial/datastructures.html

**Python 其他流程控制工具：** https://docs.python.org/zh-cn/3.7/tutorial/controlflow.html

**Python 中的类：** https://docs.python.org/zh-cn/3.7/tutorial/classes.html

**Python 定义函数：** https://docs.python.org/zh-cn/3.7/tutorial/controlflow.html#defining-functions

## 2. 前端基础知识

### 2.1 网页的三个组成部分

- 结构 —— html
- 表现 —— css
- 行为 —— js

### 2.2 HTTP协议

**HTTP Headers**

**Headers**是服务端发送的除网页内容之外的一些**控制**信息。

其中**user-agent**和**cookies**是写爬虫程序时需要重点构造的，用来模拟浏览器行为。

- **user-agent: ** 客户端浏览器的基本信息。
- **cookies: ** 有些网站需要登录后才可以访问。Cookie就是服务端验证了用户名和密码后返回给客户端的一些信息。客户端下一次去请求时需要携带这些信息（Cookie，通常是加密过的）才可成功访问。

**网络协议体系模型**

从底向上依次是：物理层→链路层→网络层→传输层→应用层

TCP协议处于传输层。

HTTP协议处于应用层。

**网页的两种请求方式**

- **get**
- **post**

### 2.3 XPath

**XPath 中文文档：** https://www.w3school.com.cn/xpath/index.asp

**XPath 英文文档：** https://www.w3.org/TR/2017/REC-xpath-31-20170321/#nt-bnf

**Scrapy Xpath 官方学习文档：** https://docs.scrapy.org/en/latest/topics/selectors.html#working-with-xpaths

Python使用XPath解析可以安装lxml库。Scrapy框架直接支持XPath解析。

html页面是一棵dom树。以下介绍常见的符号含义：

- / ------------- 从当前结点处寻找
- // ------------ 从任意结点处寻找
- . ------------- 从当前结点处往下寻找
- .. ------------ 从当前结点兄弟处寻找
- [] ------------ 过滤条件
- @ ------------ 属性
- text() -------- 文本

举2个例子：

1. //div[@class="movie-item"]./a/@href

   提取的是：所有class属性为"movie-item"的div标签下的a标签的href属性值。

2. //div[@class="movie-item"]../a/text()

   提取的是：与所有class属性为"movie-item"的div标签同级的a标签的文本。

## 3. Scrapy框架

### 3.1 Scrapy框架结构解析

**Scrapy 架构官方文档介绍：** https://docs.scrapy.org/en/latest/topics/architecture.html

![image-scrapy官方图](https://github.com/QingjingFei/Python001-class01/blob/master/week01/pics/scrapy官方图.png)

*注：一个Scrapy Engine可以对应多个Spiders。*

### 3.2 Scrapy框架目录解析

让我们通过Scrapy项目的创建，来认识它的目录结构：

```shell
$ scrapy startproject maoyan
New Scrapy project 'maoyan', using template ......, created in:
......
You can start your first spider with:
    cd maoyan
    scrapy genspider example example.com
$ cd maoyan
$ scrapy genspider maoyanmovie maoyan.com
Created spider 'maoyanmovie' using template 'basic' in module:
  maoyan.spiders.maoyanmovie
$ ls
maoyan     scrapy.cfg
$ cd maoyan
$ ls
__init__.py    __pycache__    items.py       middlewares.py pipelines.py   settings.py    spiders
$ cd spiders
$ ls
__init__.py    __pycache__    maoyanmovie.py
$ vim maoyanmovie.py
```

![image-scrapy架构](https://github.com/QingjingFei/Python001-class01/blob/master/week01/pics/scrapy架构.png)

*注：使用Scrapy框架时，需要自己写的一般只有爬虫器和管道。*

本例maoyan项目中，需要自行修改的文件有：

- maoyanmovie.py: 请求链接、解析网页等主体爬虫业务逻辑。
- items.py: 模块间传递的数据定义。
- pipelines.py: 数据存储处理。
- settings.py: 爬虫器的相关设置，比如常见的user-agent、cookies、下载延迟等。

具体代码见于week01/hw02文件夹内。

*注：user-agent和cookies既可以在settings.py中设置，也可以在maoyanmovie.py中设置，可以参考[链接](https://blog.csdn.net/fuck487/article/details/84617194)。*



### 3.3 爬虫器的启动

**开启爬虫**命令使用`scrapy crawl ...`，可以在最初的mayan/文件夹下的任意路径运行。

```shell
$ scrapy crawl maoyanmovie
```

## 4. 作业总结

在爬取猫眼电影时，会遇到反爬。

1. 刚开始会遇到拖动验证页面。

   解决办法：将该页面下载后本地用浏览器打开，手工拖动后即能展示所请求页面。开发者模式下复制cookies内的uuid值，写入代码中即可正常访问。cookies的有效期约有半小时，临时使用没有问题。
   
2. 请求过多后出现IP限制访问页面。

   解决办法：暂未解决，期待下周的内容。
