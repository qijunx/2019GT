# -*-coding:utf-8-*-
import requests
import time
import re
from OCR import ocr_distinguish
from PIL import Image

requests.packages.urllib3.disable_warnings()

headers = {
        "Accept": "text / html, application / xhtml + xml, image / jxr, * / *",
        "Accept - Encoding": "gzip, deflate",
        "Accept - Language": "zh - CN",
        "Connection": "Keep-Alive",
        "User-Agent": "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 10.0; WOW64; Trident/7.0; .NET4.0C;"
                      " .NET4.0E; .NET CLR 2.0.50727; .NET CLR 3.0.30729; .NET CLR 3.5.30729)"
        }

VPN_url = "https://vpn.hpu.edu.cn/por/login_psw.csp"
VPN_post_url = "https://vpn.hpu.edu.cn/web/1/http/1/218.196.240.97/loginAction.do"
VPN_yzm_url = "https://vpn.hpu.edu.cn/web/0/http/1/218.196.240.97/validateCodeAction.do"
VPN_mubiao_url = "https://vpn.hpu.edu.cn/web/1/http/2/218.196.240.97/gradeLnAllAction.do?type=ln&oper=fainfo&fajhh=4190"
session = requests.session()


# VPN登录
def vpn_login(username, password, is_d_yzm):
    VPN_data = {
        "svpn_name": username,
        "svpn_password": password
    }

    vpn_response = session.post(VPN_url, data=VPN_data, headers=headers, verify=False)
    print(vpn_response.text)

    # 判断识别验证码的输入方式
    if is_d_yzm == "yes":  # 手动输入
        with open("yzm_test.png", "wb") as f:
            f.write(session.get(VPN_yzm_url, headers=headers, verify=False).content)
            f.close()
        image = Image.open("yzm_test.png")
        image.show()
        yzm = input("请查看当前目录下的验证码图片：")
    elif is_d_yzm == "no":  # OCR识别
        yzm = ocr_distinguish(VPN_yzm_url, session, headers)
    else:
        return ""
    print(type(yzm))
    time.sleep(1)
    post_data = {
        "zjh": "311808010132",
        "mm": "zj200043",
        "v_yzm": yzm
    }
    # 获取响应， 并保存响应的cookie
    loginresponse = session.post(VPN_post_url, data=post_data, headers=headers, verify=False)
    print("状态码：" + str(loginresponse.status_code))
    print(loginresponse.text)
    print(yzm)

    return loginresponse.text


# 获取网页的源代码和数据处理
def vpn_get_html_text():
    # 获取成绩所在网页的响应，并提取源代码
    response = session.get(VPN_mubiao_url, headers=headers, verify=False)
    print(response.text)

    # 采用正则表达式获取课程名称
    kechengmingchengs = re.findall(r'<tr class="odd".*?<td.*?<td.*?<td align="center"(.*?)</td>.*?</tr>',
                                   response.text, re.S)
    kechengmingcheng_list = []
    for kechengmingcheng in kechengmingchengs:
        kechengmingcheng = re.sub(r'\r\n', "", kechengmingcheng)
        kechengmingcheng = re.sub('>', "", kechengmingcheng)
        kechengmingcheng = kechengmingcheng.strip()
        kechengmingcheng_list.append(kechengmingcheng)
    # print(kechengmingcheng_list)

    # 采用正则表达式获取学分
    xuefens = re.findall(r'<tr class="odd".*?<td.*?<td.*?<td.*?<td.*?<td align="center"(.*?)</td>.*?</tr>',
                         response.text, re.S)
    xuefen_list = []
    for xuefen in xuefens:
        xuefen = re.sub(r'\r\n', "", xuefen)
        xuefen = re.sub('>', "", xuefen)
        xuefen = xuefen.strip()
        xuefen_list.append(xuefen)
    # print(xuefen_list)

    # 采用正则表达式获取课程属性
    kechengshuxings = re.findall(
        r'<tr class="odd".*?<td.*?<td.*?<td.*?<td.*?<td.*?<td align="center"(.*?)</td>.*?</tr>', response.text, re.S)
    kechengshuxing_list = []
    for kechengshuxing in kechengshuxings:
        kechengshuxing = re.sub(r'\r\n', "", kechengshuxing)
        kechengshuxing = re.sub('>', "", kechengshuxing)
        kechengshuxing = kechengshuxing.strip()
        kechengshuxing_list.append(kechengshuxing)
    # print(kechengshuxing_list)

    # 采用正则表达式获取成绩
    chengjis = re.findall(r'<td.*?<p.*?>(.*?)&nbsp.*?</P>', response.text, re.S)
    while '' in chengjis:
        chengjis.remove('')
    # print(chengjis)

    all_dicts = []
    for value in zip(kechengmingcheng_list, xuefen_list, kechengshuxing_list, chengjis):
        kechengmingcheng, xuefen, kechengshuxing, chengji = value
        all_dict = {
            "课程名称": kechengmingcheng,
            "学分": xuefen,
            "课程属性": kechengshuxing,
            "成绩": chengji
        }
        all_dicts.append(all_dict)

    all_lists = [["课程名称", "学分", "课程属性", "成绩"]]
    for value in zip(kechengmingcheng_list, xuefen_list, kechengshuxing_list, chengjis):
        kechengmingcheng, xuefen, kechengshuxing, chengji = value
        all_list = [kechengmingcheng, xuefen, kechengshuxing, chengji]
        all_lists.append(all_list)

    for all_dict in all_dicts:
        print(all_dict)

    for all_list in all_lists:
        print(all_list)

    return all_lists, all_dicts
