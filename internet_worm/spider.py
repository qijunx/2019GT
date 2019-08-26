# -*-coding:utf-8-*-
# 导入所需要的模块
import requests
import xlwt
import re
from OCR import ocr_distinguish
import time
from PIL import Image


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


# 将数据写入txt文件中
def txt_write(filename, data):  # filename为写入txt文件的路径，data为要写入数据列表.
    file = open(filename, 'w', encoding="utf-8")
    for i in range(len(data)):
        # 去除[],这两行按数据不同，可以选择
        s = str(data[i]).replace('[', '').replace(']', '')
        # 去除单引号，逗号，大括号，每行末尾追加换行符
        s = s.replace("'", '').replace(',', '       ').replace('{', '').replace('}', '') + '\n'
        file.write(s)
    file.close()
    print("保存文件成功")


# 将数据写入excel文件中
def excel_write(file_path, datas):  # file_path为写入excel文件的路径，datas为要写入数据列表
    f = xlwt.Workbook()
    sheet1 = f.add_sheet(u'sheet1', cell_overwrite_ok=True)  # 创建sheet
    # 将数据写入第 i 行，第 j 列
    i = 0
    for data in datas:
        for j in range(len(data)):
            sheet1.write(i, j, data[j])
        i = i + 1
    f.save(file_path)  # 保存文件


# 登录网页
def login_url(user_name, password, is_d_yzm):
    # 判断识别验证码的输入方式
    if is_d_yzm == "yes":  # 手动输入
        with open("yzm1.png", "wb") as f:
            f.write(session.get(yzm_url, headers=headers).content)
            f.close()
        image = Image.open("yzm1.png")
        image.show()
        yzm = input("请查看当前目录下的验证码图片：")
    elif is_d_yzm == "no":  # OCR识别
        yzm = ocr_distinguish(yzm_url, session, headers)
    else:
        return ""
    print(type(yzm))
    time.sleep(1)
    post_data = {
        "zjh": user_name,
        "mm": password,
        "v_yzm": yzm
    }
    # 获取响应， 并保存响应的cookie
    loginresponse = session.post(post_url, data=post_data, headers=headers)
    print("状态码：" + str(loginresponse.status_code))
    print(loginresponse.text)
    print(yzm)
    return loginresponse.text


# 获取网页的源代码和数据处理
def get_html_text():
    # 获取成绩所在网页的响应，并提取源代码
    response = session.get(mubiao_url, headers=headers)
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

    # 将取出的信息以字典放入列表， 便于写入txt文件
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

    # 将取出的信息放入列表， 便于写入excel文件
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


if __name__ == '__main__':
    user_name = input("你的账号是：")
    password = input("你的密码是：")
    is_d_yzm = input("请输入辨认验证码的方式\nyes为手动输入，no为OCR自动识别\n")
    text = login_url(user_name, password, is_d_yzm)
    return_flag1 = re.findall(r'<title>(.*?)</title>', text, re.S)
    print(return_flag1)
    if return_flag1[0] == "学分制综合教务":
        print("登录成功")
        all_lists_, all_dict_ = get_html_text()
        txt_write("成绩单.txt", all_dict_)
        excel_write("成绩单.xls", all_lists_)
    elif return_flag1[0] == "URP 综合教务系统 - 登录":
        return_flag2 = re.findall(r'<td.*?<font.*?>(.*?)</font></strong>', text, re.S)
        print(return_flag2)
        if return_flag2[0] == "你输入的验证码错误，请您重新输入！":
            print("你输入的验证码错误，请您重新输入！")
        elif return_flag2[0] == "您的密码不正确，请您重新输入！":
            print("您的密码不正确，请您重新输入！")
