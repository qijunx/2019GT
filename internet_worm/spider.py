# -*-coding:utf-8-*-
# 导入所需要的模块
import requests
# from retrying import retry
import re
from OCR import ocr_distinguish

headers = {
        "Accept": "text / html, application / xhtml + xml, image / jxr, * / *",
        "Accept - Encoding": "gzip, deflate",
        "Accept - Language": "zh - CN",
        "Connection": "Keep-Alive",
        "User-Agent": "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 10.0; WOW64; Trident/7.0; .NET4.0C;"
                      " .NET4.0E; .NET CLR 2.0.50727; .NET CLR 3.0.30729; .NET CLR 3.5.30729)"
        }
post_url = 'http://jw.hpu.edu.cn/loginAction.do'
yzm_url = "http://jw.hpu.edu.cn/validateCodeAction.do"
mubiao_url = "http://jw.hpu.edu.cn/gradeLnAllAction.do?type=ln&oper=fainfo&fajhh=4190"
session = requests.session()


# def get_yzm_information():
#     yzm = ocr_distinguish(yzm_url)
#     return yzm


# 登录网页
def login_url(user_name, password):
    # with open("yzm1.png", "wb") as f:
    #     f.write(session.get(yzm_url, headers=headers).content)
    #     f.close()
    #     yzm = input("请查看当前目录下的验证码图片：")
    yzm = ocr_distinguish(yzm_url)
    post_data = {
        "zjh": user_name,
        "mm": password,
        "v_yzm": yzm
    }
    loginresponse = session.post(post_url, data=post_data, headers=headers)
    print("状态码：" + str(loginresponse.status_code))
    print(loginresponse.text)
    print(yzm)
    return loginresponse.text


# # 获取网页的源代码和数据处理
# def get_html_text():
#     response = session.get(mubiao_url, headers=headers)
#     print(response.text)
#
#     kechengmingchengs = re.findall(r'<tr class="odd".*?<td.*?<td.*?<td align="center"(.*?)</td>.*?</tr>',
#                                    response.text, re.S)
#     kechengmingcheng_list = []
#     for kechengmingcheng in kechengmingchengs:
#         kechengmingcheng = re.sub(r'\r\n', "", kechengmingcheng)
#         kechengmingcheng = re.sub('>', "", kechengmingcheng)
#         kechengmingcheng = kechengmingcheng.strip()
#         kechengmingcheng_list.append(kechengmingcheng)
#     # print(kechengmingcheng_list)
#
#     xuefens = re.findall(r'<tr class="odd".*?<td.*?<td.*?<td.*?<td.*?<td align="center"(.*?)</td>.*?</tr>',
#                          response.text, re.S)
#     xuefen_list = []
#     for xuefen in xuefens:
#         xuefen = re.sub(r'\r\n', "", xuefen)
#         xuefen = re.sub('>', "", xuefen)
#         xuefen = xuefen.strip()
#         xuefen_list.append(xuefen)
#     # print(xuefen_list)
#
#     kechengshuxings = re.findall(
#         r'<tr class="odd".*?<td.*?<td.*?<td.*?<td.*?<td.*?<td align="center"(.*?)</td>.*?</tr>', response.text, re.S)
#     kechengshuxing_list = []
#     for kechengshuxing in kechengshuxings:
#         kechengshuxing = re.sub(r'\r\n', "", kechengshuxing)
#         kechengshuxing = re.sub('>', "", kechengshuxing)
#         kechengshuxing = kechengshuxing.strip()
#         kechengshuxing_list.append(kechengshuxing)
#     # print(kechengshuxing_list)
#
#     chengjis = re.findall(r'<td.*?<p.*?>(.*?)&nbsp.*?</P>', response.text, re.S)
#     while '' in chengjis:
#         chengjis.remove('')
#     # print(chengjis)
#
#     all_lists = []
#     for value in zip(kechengmingcheng_list, xuefen_list, kechengshuxing_list, chengjis):
#         kechengmingcheng, xuefen, kechengshuxing, chengji = value
#         all_list = {
#             "课程名称": kechengmingcheng,
#             "学分": xuefen,
#             "课程属性": kechengshuxing,
#             "成绩": chengji
#         }
#         all_lists.append(all_list)
#
#     for all_list in all_lists:
#         print(all_list)


if __name__ == '__main__':
    # user_name = input("你的账号是：")
    # password = input("你的密码是：")
    text = login_url("311808010132", "zj200043")
    # # text = login_url(user_name, password)
    # return_flag1 = re.findall(r'<title>(.*?)</title>', text, re.S)
    # print(return_flag1)
    # if return_flag1[0] == "学分制综合教务":
    #     print("登录成功")
    #     get_html_text()
    # elif return_flag1[0] == "URP 综合教务系统 - 登录":
    #     return_flag2 = re.findall(r'<td.*?<font.*?>(.*?)</font></strong>', text, re.S)
    #     print(return_flag2)
    #     if return_flag2[0] == "你输入的验证码错误，请您重新输入！":
    #         print("你输入的验证码错误，请您重新输入！")
    #     elif return_flag2[0] == "您的密码不正确，请您重新输入！":
    #         print("您的密码不正确，请您重新输入！")
