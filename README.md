爬取支付宝订单存入数据库，客户可从订单号操作完成自动支付，无需人工处理，无需接入支付宝。


需要再linux环境下搭建web服务，这里采用的是Django Nginx+uwsgi，使用谷歌浏览器selenium+Chrome保持登录状态
获取cookies，使用BeautifulSoup 解析requests请求到的支付宝订单页面，存入数据库。

这里只有给出django代码，其他环境自行安装

使用方法：

通过访问链接启动登录
http://127.0.0.1:8000/start_chrome_spider

通过接口请求保存订单
http://127.0.0.1:8000/alipay_face?action=session&session=s