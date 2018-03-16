# -*- coding: utf-8 -*-
from django.http import HttpResponse
from selenium import webdriver
import time
import random
import threading

'''
http://127.0.0.1:8000/start_chrome_spider?username=user&password=wd
'''
state_str = "未登录"


class Chromes(object):
    def __init__(self, username=None, passwd=None):
        self.username = username
        self.password = passwd
        self._login_url = "https://auth.alipay.com/login/index.htm"
        self.threads = 0
        self.is_login = False
        self.login_times=0
        self.ck=None
        # cookie存储
        self.cookie = {}
        self._browser = webdriver.Chrome()

    # 减慢账号密码的输入速度
    @staticmethod
    def _slow_input(ele, word):
        for i in word:
            # 输出一个字符
            ele.send_keys(i)
            # 随机睡眠0到1秒
            time.sleep(random.uniform(0, 0.5))

    # set cookies 到 session
    def _set_cookies(self):
        cookie = self.cookie
        self.session.cookies.update(cookie)
        # 输出cookie
        # logger.debug(self.session.cookies)
        return True

    # 判断是否需要登录
    def islogin(self):
        flag = True
        if self._login_url in self._browser.current_url:
            print("islogin")
            flag = self.login()
        if flag:
            self.save_cookies()
        self.is_login = flag
        return flag

    def save_cookies(self):
        # 获取cookies转换成字典
        cookies = self._browser.get_cookies()
        # cookie字典
        cookies_dict = {}
        for cookie in cookies:
            if 'name' in cookie and 'value' in cookie:
                cookies_dict[cookie['name']] = cookie['value']
                if cookie['name'] == "ALIPAYJSESSIONID":
                    coo = cookie['value']
                    if not self.ck == coo:
                        self.ck = coo
                        #requests.get("http://127.0.0.1:8000/alipay_face/?action=session&session=" + coo)

        self.cookie = cookies_dict

    def login(self):
        if self._login_url in self._browser.current_url:

            # 点击密码登录的选项卡
            self._browser.find_element_by_xpath('//*[@id="J-loginMethod-tabs"]/li[2]').click()

            # 用户名输入框
            username = self._browser.find_element_by_id('J-input-user')
            username.clear()
            print('正在输入账号.....')
            self._slow_input(username, self.username)
            time.sleep(random.uniform(0.4, 0.8))

            # 密码输入框
            password = self._browser.find_element_by_xpath('//*[@id="password_container"]/input')
            password.clear()
            print('正在输入密码....')
            self._slow_input(password, self.password)

            # 登录按钮
            time.sleep(random.uniform(0.3, 0.5))
            self._browser.find_element_by_id('J-login-btn').click()
            self.login_times=self.login_times+1

            # 输出当前链接
            print("当前页面链接: " + self._browser.title)
            if "登录" in self._browser.title:
                return False
            else:
                return True
        return True

class MyThread(threading.Thread):
    url = 'https://my.alipay.com/portal/i.htm'

    def __init__(self, chrome):
        super(MyThread, self).__init__()
        self.chrome = chrome
        self.flag = True
        self.thread_sum = chrome.threads + 1

    def run(self):
        while self.flag:
            self.chrome._browser.get(self.url)
            self.chrome._browser.implicitly_wait(3)
            if self.chrome.islogin():
                print("" + str(self.thread_sum))
                time.sleep(30)
            else:
                self.flag = False
                self.thread_sum = self.thread_sum - 1
                print("" + str(self.thread_sum))




def start_chrome(requests):
    state_str = ""
    username = requests.GET.get('username')
    password = requests.GET.get('password')
    if username == None:
        state_str = '用户名不能为空'
    if password == None:
        state_str = '密码不能为空'

    chrom.username = username
    chrom.password = password
    if state_str=="":
        is_login = chrom.is_login
        if is_login:
            state_str = "在线中...."
        else:
            state_str = "不在线，登录中..."
        if chrom.threads == 0:
            thread = MyThread(chrom)
            thread.start()

    return HttpResponse("LIAOZZ"+state_str)
chrom = Chromes()
