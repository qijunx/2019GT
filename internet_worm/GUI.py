# -*-coding:utf-8-*-
# 导入所需要的模块
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk


# 定义窗体切换标志的标志位
change_screen_flag = 0
# 定义功能窗口返回登录窗口的标志位
back_flag = False
# 定义退出窗口的标志位
quit_flag = True

user_name = 0
password = 0


# 用户按下查询键后执行的函数
def query_results():
    query = tk.messagebox.askquestion(title="最后警告", message="最后一次确定了？生死有命，富贵在天！Action？")
    if query == "yes":
        pass
    else:
        print("查询失败")
        messagebox.showerror(title="提示", message="查询失败")


# 用户按下导出为txt文档键后执行的函数
def export_txt():
    txt_export = tk.messagebox.askquestion(title="提示", message="你确定要将成绩导出为txt文档吗？")
    if txt_export == "yes":
        print("导出txt文档成功")
        messagebox.showinfo(title="提示", message="导出txt成功")
    else:
        print("导出txt文档失败")
        messagebox.showerror(title="提示", message="导出txt失败")


# 用户按下导出为Excel表格键后执行的函数
def export_excel():
    excel_export = tk.messagebox.askquestion(title="提示", message="你确定要将成绩导出为excel表格吗？")
    if excel_export == "yes":
        print("导出excel表格成功")
        messagebox.showinfo(title="提示", message="导出excel表格成功")
    else:
        print("导出excel表格失败")
        messagebox.showerror(title="提示", message="导出excel表格失败")


# 对表格控件添加信息
def insert_information():
    pass


# 登录界面
def login_in_interface():
    global change_screen_flag, back_flag

    # 用户按下登录键后执行的函数
    def user_login():
        global user_name, password, change_screen_flag
        user_name = var_user_name.get()
        password = var_password.get()
        login = tk.messagebox.askquestion(title="温馨提示", message="你确定要进入吗？一入此系统，后果自负！")
        if login == "yes":
            messagebox.showinfo(title="提示", message="登录成功")
            print("登录成功")
            change_screen_flag = 1
            login_window.destroy()
        else:
            print("登录失败")
            messagebox.showerror(title="提示", message="登录失败")

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

    tree.heading("课程名", text="课程名")
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
