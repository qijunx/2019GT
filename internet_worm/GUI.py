# -*-coding:utf-8-*-
# 导入所需要的模块
import tkinter as tk
import re
from tkinter import messagebox
from tkinter import ttk
from spider import login_url, get_html_text, text_write, excel_write
from VPN import vpn_login, vpn_get_html_text


# 定义窗体切换标志的标志位
change_screen_flag = 0
# 定义功能窗口返回登录窗口的标志位
back_flag = False
# 定义退出窗口的标志位
quit_flag = True
# 定义是否是由VPN登录的标志位
is_vpn_flag = 0

user_name = 0
password = 0

new_lists = []
new_dicts = {}


# 登录界面
def login_in_interface():
    global change_screen_flag, back_flag

    # 用户按下登录键后执行的函数
    def user_login():
        global user_name, password, change_screen_flag, is_vpn_flag
        user_name = var_user_name.get()
        password = var_password.get()
        login = tk.messagebox.askquestion(title="温馨提示", message="你确定要进入吗？一入此系统，后果自负！")
        try:
            text = login_url(user_name, password)
        except:
            vpn_flag = tk.messagebox.askquestion(title="温馨提示", message="你的网络不是校园网，"
                                                                       "请切换至校园网登录或者点击是使用VPN登录")
            if vpn_flag == "yes":
                is_vpn_flag = 1
                text = vpn_login(user_name, password)
            else:
                is_vpn_flag = 0
                messagebox.showinfo(title="提示", message="你放弃使用VPN登录请切换至校园再使用本系统")
                return ""
        return_flag1 = re.findall(r'<title>(.*?)</title>', text, re.S)
        print(return_flag1)
        if login == "yes" and return_flag1[0] == "学分制综合教务":
            messagebox.showinfo(title="提示", message="登录成功")
            print("登录成功")
            change_screen_flag = 1
            login_window.destroy()
        elif login == "no" or return_flag1[0] == "URP 综合教务系统 - 登录":
            print("登录失败")
            return_flag2 = re.findall(r'<td.*?<font.*?>(.*?)</font></strong>', text, re.S)
            print(return_flag2)
            if return_flag2[0] == "你输入的验证码错误，请您重新输入！":
                print("你输入的验证码错误，请您重新输入！")
                messagebox.showerror(title="提示", message="验证码错误，登录失败，请重新输入")
            elif return_flag2[0] == "您的密码不正确，请您重新输入！":
                print("您的密码不正确，请您重新输入！")
                messagebox.showerror(title="提示", message="密码错误，登录失败，请重新输入")

    # 用户按下退出键后执行的函数
    def login_quit_system():
        global quit_flag, back_flag
        login_quit = tk.messagebox.askquestion(title="温馨提示", message="你确定要退出吗？后面的故事还很精彩欧！")
        if login_quit == "yes":
            messagebox.showinfo(title="提示", message="退出成功")
            print("退出成功")
            quit_flag = False
            back_flag = True
            login_window.destroy()
        else:
            print("退出失败")
            messagebox.showerror(title="提示", message="退出失败")

    login_window = tk.Tk()
    login_window.resizable(False, False)
    login_window.title("校园网爬虫系统")
    login_window.geometry("450x300")

    # 欢迎
    tk.Label(login_window, text="欢迎使用本爬虫系统", bg="green", fg="red", font=("Arial", 26), height=2).place(x=30, y=10)

    # 用户名 和 密码
    tk.Label(login_window, text="Username:").place(x=50, y=150)
    tk.Label(login_window, text="Password:").place(x=50, y=190)

    # 输入用户信息
    var_user_name = tk.StringVar()
    var_user_name.set("你的学号")
    entry_user_name = tk.Entry(login_window, textvariable=var_user_name)
    entry_user_name.place(x=160, y=150)
    var_password = tk.StringVar()
    entry_password = tk.Entry(login_window, textvariable=var_password, show="*")
    entry_password.place(x=160, y=190)

    # 登录按键
    button_login = tk.Button(login_window, text="登录(Login)", command=user_login)
    button_login.place(x=170, y=230)

    # 退出按键
    button_quit = tk.Button(login_window, text="退出(Quit)", command=login_quit_system)
    button_quit.place(x=360, y=260)

    if change_screen_flag == 1:
        login_window.destroy()

    login_window.mainloop()


# 功能界面
def function_interface():
    # 用户按下返回键后执行的函数
    def back_system():
        global change_screen_flag
        function_back = tk.messagebox.askquestion(title="温馨提示", message="你确定要返回登录界面吗？")
        if function_back == "yes":
            print("返回成功")
            messagebox.showinfo(title="提示", message="返回成功")
            function_window.destroy()
            change_screen_flag = 0
        else:
            print("返回失败")
            messagebox.showerror(title="提示", message="返回失败")

    # 用户按下退出键后执行的函数
    def function_quit_system():
        global quit_flag, back_flag
        function_quit = tk.messagebox.askquestion(title="温馨提示", message="故事已经结束，你确定要退出吗？")
        if function_quit == "yes":
            messagebox.showinfo(title="提示", message="退出成功")
            print("退出成功")
            back_flag = True
            function_window.destroy()
        else:
            print("退出失败")
            messagebox.showerror(title="提示", message="退出失败")

    # 对表格控件添加信息
    def insert_information():
        global new_lists
        deal_lists = new_lists.copy()
        del deal_lists[0]
        print(new_lists)
        print(deal_lists)
        i = 0
        for deal_list in deal_lists:
            tree.insert("", i, value=deal_list)
            i = i + 1

    # 用户按下查询键后执行的函数
    def query_results():
        global new_lists, new_dicts
        query = tk.messagebox.askquestion(title="最后警告", message="最后一次确定了？生死有命，富贵在天！Action？")
        if query == "yes":
            if is_vpn_flag == 0:
                new_lists, new_dicts = get_html_text()
            elif is_vpn_flag == 1:
                new_lists, new_dicts = vpn_get_html_text()
            print("查询成功")
            insert_information()
        else:
            print("查询失败")
            messagebox.showerror(title="提示", message="查询失败")

    # 用户按下导出为txt文档键后执行的函数
    def export_txt():
        global new_dicts
        txt_export = tk.messagebox.askquestion(title="提示", message="你确定要将成绩导出为txt文档吗？")
        if txt_export == "yes":
            print("导出txt文档成功")
            text_write("成绩单1.txt", new_dicts)
            messagebox.showinfo(title="提示", message="导出txt成功")
        else:
            print("导出txt文档失败")
            messagebox.showerror(title="提示", message="导出txt失败")

    # 用户按下导出为Excel表格键后执行的函数
    def export_excel():
        global new_lists
        excel_export = tk.messagebox.askquestion(title="提示", message="你确定要将成绩导出为excel表格吗？")
        if excel_export == "yes":
            print("导出excel表格成功")
            excel_write("成绩单1.xls", new_lists)
            messagebox.showinfo(title="提示", message="导出excel表格成功")
        else:
            print("导出excel表格失败")
            messagebox.showerror(title="提示", message="导出excel表格失败")

    global change_screen_flag
    function_window = tk.Tk()
    function_window.resizable(False, False)
    function_window.title("校园网爬虫系统")
    function_window.geometry("800x800")

    # 头信息
    tk.Label(function_window, text="爬虫系统", bg="green", fg="red", font=("Arial", 30), width=26, height=2).place(x=20, y=10)

    # 查询功能按键
    button_login = tk.Button(function_window, text="查询(Query)", borderwidth=20, wraplength=120, command=query_results)
    button_login.place(x=20, y=180)

    # 返回按键
    button_back = tk.Button(function_window, text="返回(Back)", command=back_system)
    button_back.place(x=10, y=700)

    # 退出按键
    button_quit = tk.Button(function_window, text="退出(Quit)", command=function_quit_system)
    button_quit.place(x=10, y=760)

    # 导出为txt文档按键
    button_export_txt = tk.Button(function_window, text="导出为txt文档", borderwidth=20, wraplength=120, command=export_txt)
    button_export_txt.place(x=20, y=450)

    # 导出为Excel表格按键
    button_export_excel = tk.Button(function_window, text="导出为Excel表格", borderwidth=20, wraplength=120, command=export_excel)
    button_export_excel.place(x=20, y=540)

    # 表格控件，用于显示信息
    tree = ttk.Treeview(function_window, height=30, show="headings")
    tree.place(x=185, y=160)

    tree["columns"] = ("课程名", "学分", "课程属性", "成绩")

    tree.column("课程名", width=200, anchor='center')
    tree.column("学分", width=50, anchor='center')
    tree.column("课程属性", width=150, anchor='center')
    tree.column("成绩", width=200, anchor='center')

    tree.heading("课程名", text="课程名称")
    tree.heading("学分", text="学分")
    tree.heading("课程属性", text="课程属性")
    tree.heading("成绩", text="成绩")

    if change_screen_flag == 0:
        function_window.destroy()

    function_window.mainloop()


if __name__ == '__main__':
    while True:
        login_in_interface()
        if quit_flag:
            function_interface()

        if back_flag:
            break

    print("退出系统成功")
