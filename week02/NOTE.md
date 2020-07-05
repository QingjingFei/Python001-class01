# Week02: 掌握Scrapy爬虫框架

  \* [Week02: 掌握Scrapy爬虫框架](#week02-掌握scrapy爬虫框架)

   \* [1. 异常捕获与处理](#1-异常捕获与处理)

​     \* [1.1 异常的基本知识](#11-异常的基本知识)

​     \* [1.2 用户定义异常](#12-用户定义异常)

​     \* [1.3 异常的2个展示与书写技巧](#13-异常的2个展示与书写技巧)

   \* [2. 使用PyMySQL进行数据库操作](#2-使用pymysql进行数据库操作)

   \* [3. 反爬虫](#3-反爬虫)

​     \* [3.1 模拟浏览器Headers](#31-模拟浏览器headers)

​     \* [3.2 模拟登录Cookies](#32-模拟登录cookies)

​     \* [3.3 模拟浏览器行为](#33-模拟浏览器行为)

​     \* [3.4 自定义中间件&amp;随机代理IP](#34-自定义中间件随机代理ip)

   \* [4. 分布式爬虫](#4-分布式爬虫)

​     \* [4.1 Scrapy如何分布式](#41-scrapy如何分布式)

​     \* [4.2 Redis的基础搭建](#42-redis的基础搭建)

​     \* [4.3 Scrapy与Redis的通信](#43-scrapy与redis的通信)

## 1. 异常捕获与处理

### 1.1 异常的基本知识

所有内置的非系统退出的异常都派生自Exception类。譬如，使用生成器时元素生成完成时调用next()常会遇到StopIteration异常。

**内置异常类：**https://docs.python.org/zh-cn/3.7/library/exceptions.html

常见的异常类型有6个：

1. LookupError下的IndexError和KeyError
2. IOError
3. NameError
4. TypeError
5. AttributeError
6. ZeroDivisionError

此外，注意以下两点：

- 异常的输出从上至下是程序调用从外至里的过程，所以最**关键**的异常入口在**最底下**。

- 但程序的异常捕获有一个**陷阱**：如果已经捕获到一个异常，程序不会再继续捕获后面的异常了。

```python
def f1():
    1/0

def f2():
    list1 = []
    list1[1]
    # 捕获到list1[1]的IndexError异常后
    # 程序不会再捕获ZeroDivisionError异常了  
    f1()
    

def f3():
    f2()


try:
    f3()
except (ZeroDivisionError, Exception) as e:
    print(e)  
```

```shell
>> list index out of range
```

### 1.2 用户定义异常

```python
class UserInputError(Exception):
    def __init__(self, ErrorInfo):
        super().__init__(self, ErrorInfo)
        self.errorinfo = ErrorInfo
    def __str__(self):
        return self.errorinfo

userinput = 'a'

try:
    if (not userinput.isdigit()):
        raise UserInputError('用户输入错误')
except UserInputError as ue:
    print(ue)
finally:
    del userinput
```

```shell
>> 用户输入错误
```

### 1.3 异常的2个展示与书写技巧

1. 美化异常输出结果的python库：**pretty_errors**

2. 优化的文件异常处理：**with**关键字

```python
file1 = open('a.txt', encoding='utf8')
try:
    data = file1.read()
finally:
    file1.close()
```

可以用with关键字改写为：

```python
with open('a.txt', encoding='utf8') as file2:
    data = file2.read()
```

with方法也是可以自定义的：

```python
class Open:
    def __enter__(self):
        print("open")

    def __exit__(self, type, value, trace):
        print("close")
 
    def __call__(self):
        pass

with Open() as f:
    pass
# 上下文协议
```

```shell
>> open
   close
```



注意：我们正越来越多地遇到以双下划线'__'开头和结尾的方法，比如'\_\_init\_\_'、'\_\_enter\_\_'、'\_\_exit\_\_'，这些称作**魔术方法**。后面我们会详细学习它。

## 2. 使用PyMySQL进行数据库操作

**MySQL的安装参考：**[Mac系统下MySQL的下载安装和配置教程](https://blog.csdn.net/WinstonLau/article/details/81323340)

Mac系统安装路径在/usr/local/mysql/下。

**数据库启动/退出命令**

`mysql.server start`  启动mysql服务端，或者Mac系统下可在系统偏好设置中找到MySQL启动。

`ps -ef | grep mysql`  检查mysql服务器进程是否启动

`/usr/local/mysql/bin/mysql -u root -p`  启动客户端

`quit;`或`exit;`  或者Ctrl+D（Mac下）退出MySQL

**数据库基础命令**

`show databases;`  查看所有数据库

`create database db1;`  创建db1库

`use db1`  使用db1库

`show tables;`  查看所有表格

`show create table table_name;`  查看创表生成的DDL

```mysql
mysql> create table tb1(
    -> id INT NOT NULL,
    -> name VARCHAR(100) NOT NULL,
    ->  PRIMARY KEY (id)
    -> ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
Query OK, 0 rows affected (0.01 sec)
mysql> INSERT INTO tb1 values(1, 'tom');
Query OK, 1 row affected (0.00 sec)

mysql> select * from tb1;
+----+------+
| id | name |
+----+------+
|  1 | tom  |
+----+------+
1 row in set (0.00 sec)

mysql> 
```

**MySQL 官方文档手册：**https://dev.mysql.com/doc/

**PyMySQL 官方文档：**https://pypi.org/project/PyMySQL/

## 3. 反爬虫

### 3.1 模拟浏览器Headers

使用fake_useragent库的UseAgent包。

反爬虫需要留意的Headers字段：

- User-agent: 浏览器信息，每次请求可带上不同的浏览器Headers，模拟人工访问。

- Referer：跨站信息，有些网站会验证你从哪一个页面跳转过来的。

- Cookie：用户名、密码等信息，记录登录状态。
- 其他：一些网站自己增加的参数。

1. 使用python库fake_useragent，用来进行伪造user-agent的相关操作。

2. 注意使用`verify_ssl`关键字，并设为`False`，模拟user-agent时不去进行ssl验证，让浏览器请求信息更快。

```python
from fake_useragent import UserAgent
ua = UserAgent(verify_ssl=False)
```

**User-Agent 参考文档：**https://developer.mozilla.org/zh-CN/docs/Web/HTTP/Headers/User-Agent

### 3.2 模拟登录Cookies

使用requests库。

cookies存在有效期，一般来说，简单的爬虫直接复制F12取到的cookies放到Headers去请求就可以了。但当爬虫规模比较大的时候，为免除复制操作的繁琐，就需要模拟登录。

httpbin.org，是一个可以专门进行HTTP的学习和调试的一个网站。可以把我们请求的头信息在网页上展示出来。

### 3.3 模拟浏览器行为

使用selenium库的webdriver包。还需要下载安装chromedriver。

```python
from selenium import webdriver
```

**ChromeDriver 下载地址：**https://chromedriver.storage.googleapis.com/index.html

下载解压后把chromedriver移到自己虚拟环境的bin/目录下：

```shell
mv ~/Downloads/chromedriver venv/bin/chromedriver
```

### 3.4 自定义中间件&随机代理IP

无日志运行爬虫httpbin

```shell
scrapy crawl httpbin --nolog
```

## 4. 分布式爬虫

### 4.1 Scrapy如何分布式

Scrapy原生不支持分布式，多机之间需要Redis实现队列和管道的共享。

scrape-redis库很好地实现了Scrapy和Redis的集成。

使用scrappy-redis之后Scrapy的重要变化：

1. 使用了RedisSpider类替代了Spider类
2. Scheduler的queue由Redis实现
3. item pipeline由Redis实现

### 4.2 Redis的基础搭建

**Redis的安装/配置**

```shell
# 通过brew安装
$ brew install redis
# 开机启动
$ brew services start redis
# 修改配置文件（一般地，daemonize yes）
$ vim /usr/local/etc/redis.conf
```

**Redis的启动/查看/关闭**

```shell
# 服务端启动及查看
$ redis-server /usr/local/etc/redis.conf
$ ps aux | grep redis
# 客户端调用及关闭
$ redis-cli
127.0.0.1:6379> quit
$ 
# 注：Ctrl+D（Mac下）也可退出redis客户端
# 服务器端关闭
$ redis-cli
127.0.0.1:6379> shutdown
(error) ERR Errors trying to SHUTDOWN. Check logs.
127.0.0.1:6379> shutdown nosave
not connected> quit
$ 
```

**Redis图像管理工具：**[Medis](http://getmedis.com/)

### 4.3 Scrapy与Redis的通信

使用scrapy-redis库。

复制本项目的redis.conf放在geekbangtrain/目录下，与分布式爬虫项目scrapycluster/同级。

redis.conf中需要注意的几个设置：

```shell
bind 127.0.0.1  # line 69. 真实生产环境时，要设置为真实的IP地址
port 6379       # line 92. Redis运行端口
daemonize yes   # line 205. 真实生产环境时，守护模式设为yes，关闭终端就不会导致Redis关闭
```

最关键的部分是修改setting.py内的代码，用scrapy-redis组件替换scrapy中原来的部分组件。

```python
BOT_NAME = 'scrapycluster'

SPIDER_MODULES = ['scrapycluster.spiders']
NEWSPIDER_MODULE = 'scrapycluster.spiders'

# Obey robots.txt rules
ROBOTSTXT_OBEY = True

################# 以下是重点 #################
# redis信息
REDIS_HOST='127.0.0.1'
REDIS_PORT=6379

# Scheduler的QUEUE
SCHEDULER = "scrapy_redis.scheduler.Scheduler"

# 去重
DUPEFILTER_CLASS = "scrapy_redis.dupefilter.RFPDupeFilter"

# Requests的默认优先级队列
SCHEDULER_QUEUE_CLASS = 'scrapy_redis.queue.PriorityQueue'

# 将Requests队列持久化到Redis，可支持暂停或重启爬虫
SCHEDULER_PERSIST = True

# 将爬取到的items保存到Redis
ITEM_PIPELINES = {
    'scrapy_redis.pipelines.RedisPipeline': 300
}
```

