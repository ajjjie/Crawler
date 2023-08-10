# Web Crawler

- 教程：http://c.biancheng.net/python_spider/what-is-spider.html

- 基本流程
  - 使用urllib.request打开url得到网页html对象
  - 使用浏览器打开网页源代码分析网页结构及元素节点
  - 使用beautiful soup或正则表达式提取数据

### 网页构成

#### 结构

- html：网页的基本结构
- css：层叠样式表
- JavaScript：网页的行为（交互、特效等）

#### 分类

- 静态：标准html文件

- 动态：动态页面使用“动态页面技术”与服务器进行少量的数据交换，从而实现了网页的异步加载。打开百度图片（https://image.baidu.com/）并搜索 Python，当滚动鼠标滑轮时，网页会从服务器数据库自动加载数据并渲染页面，这是动态网页和静态网页最基本的区别。

#### 审查网页元素

1. F12
2. 点击审查元素
3. 移动鼠标
4. 获取代码段

<img src="http://c.biancheng.net/uploads/allimg/210819/9-210Q9110Qa39.gif" alt="python爬虫审查元素" style="zoom:67%;" />

### Urllib

```python
from urllib import requese
response=request.urlopen('http://www.baidu.com/') # 发起request并获取响应对象
bytes = response.read() # read()返回结果为 bytes 数据类型
string = response.read().decode() # decode()将字节串转换为 string 类型
url = response.geturl() # 返回响应对象的URL地址
code = response.getcode() # 返回请求时的HTTP响应码
```

### User-Agent

- User-Agent 即用户代理，简称“UA”，它是一个特殊字符串头。网站服务器通过识别 “UA”来确定用户所使用的操作系统版本、CPU 类型、浏览器版本等信息。而网站服务器则通过判断 UA 来给客户端发送不同的页面。

- 反爬时，要伪装成浏览器UA

- 在线识别本机UA：https://useragent.buyaocha.com/

- 重构UA：

  ```python
  from fake_useragent import UserAgent
  ua = UserAgent()
  headers = ua.firefox
  req = request.Request(url=url,headers=headers)
  res = request.urlopen(req)
  ```

  

### URL

- 即统一资源定位符（Uniform Resource Locator），是web页的地址

- 基本组成：如协议、域名、端口号、路径和查询字符串等

- URL 中规定了一些具有特殊意义的字符，常被用来分隔两个不同的 URL 组件，这些字符被称为**保留字符**。例如：
  - 冒号：用于分隔协议和主机组件，斜杠用于分隔主机和路径
  - `?`：用于分隔路径和查询参数等。
  - `=`用于表示查询参数中的键值对。
  - `&`符号用于分隔查询多个键值对。

- python库urllib.parse可用来解码/编码