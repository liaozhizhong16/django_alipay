# -*- coding: utf-8 -*-
'''
http://127.0.0.1:8000/alipay_face?action=session&session=s
'''
from django.http import HttpResponse
import json
import requests
import time
from testDemo.models import Alipay
from bs4 import BeautifulSoup as bs

req_url_advanced = "https://consumeprod.alipay.com/record/advanced.htm"
req_url_item = "https://lab.alipay.com/consume/record/items.htm"
req_url_type = "advanced"


def action_session(request):
    session = request.GET.get('session')
    if session == None or len(str(session)) < 5:
        return False
    data = {"session": session}

    with open("session.json", "w+") as file_json:
        json.dump(data, file_json)
        return True


def action_pay(request):
    action_pay = request.GET.get("pay")

    if action_pay == None:
        return "action_pay==None"
    session = None
    with open("session.json") as file_json:
        data = json.load(file_json)
        session = data["session"]
    if session == None or len(str(session)) < 5:
        return "未读取到session"
    cookie = {'ALIPAYJSESSIONID': session}
    req = None
    # try:
    if action_pay == req_url_type:
        req = requests.get(req_url_advanced, cookies=cookie)
    else:
        req = requests.get(req_url_item, cookies=cookie)

    if req.url.startswith('https://auth.alipay.com/'):
        return "cookie无效,请重新登录"
    if "checkSecurity" in req.url:
        return req.text
    soup = bs(req.text, 'lxml')
    for i in soup.select('.amount.outlay'):
        i.parent.decompose()
    for i in soup.select('.subTransCodeValue'):
        i.decompose()
    if action_pay == req_url_type:
        PaymentID, Name, Amount, Time = bili2(soup)
    else:
        PaymentID, Name, Amount, Time = bili(soup)
    length = len(PaymentID)
    print("length=" + str(length) + "  " + str(len(Amount)))
    for i in range(length):
        # print PaymentID[i]+"  "+Name[i]+"  "+Amount[i]
        ip_exist = Alipay.objects.filter(pay_ment_id__contains=str(PaymentID[i]))
        if not ip_exist:
            al = Alipay(pay_ment_id=PaymentID[i], phone_number=Name[i], amount=Amount[i], pay_time=Time[i])
            al.save()

    # except Exception as e:
    #	print str(e)
    return "解析完成" + str(length)


def bili(soup):
    # 流水线号
    PaymentID = []
    for i in soup.select('.consumeBizNo'):
        PaymentID.append(i.string.strip())
    Time = []
    for i in soup.select('.time'):
        Time.append(i.string.strip())
    Name = []
    for i in soup.select('.emoji-li'):
        for ii in i.stripped_strings:
            Name.append(ii)
    Amount = []
    for i in soup.select('.amount.income'):
        Amount.append(i.string.split('.')[0])
    return PaymentID, Name, Amount, Time


def bili2(soup):
    Name = []
    PaymentID = []
    for i in soup.select('.tradeNo.ft-gray p'):
        PaymentID.append(i.string.strip().split(":")[1])
        Name.append("转账")
    Time = []
    now_time = time.strftime('%Y-%m-%d', time.localtime(time.time()))
    for i in soup.select('.time-h.ft-gray'):
        Time.append(now_time + " " + i.string.strip())
    Amount = []
    for i in soup.select('.amount-pay'):
        Amount.append(i.string.split(".")[0].split(" ")[1])
    return PaymentID, Name, Amount, Time

    pass


def hello(request):
    action = request.GET.get('action')
    flag = False
    if action == "session":
        flag = action_session(request)
    elif action == "pay":
        error = action_pay(request)
        return HttpResponse(error)
    else:
        return HttpResponse("请连接正确的action")
    if flag:
        return HttpResponse("操作成功")
    return HttpResponse("操作失败")

# action_session("RZ24aQynoT5PbkgXXkTQBYmYYDjbmhauthRZ24GZ00")
# s=action_pay("RZ24aQynoT5PbkgXXkTQBYmYYDjbmhauthRZ24GZ00")
# print s
