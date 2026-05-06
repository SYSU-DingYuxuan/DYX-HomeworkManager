# -*- coding:UTF-8 -*-


NEWS = '''
3.0.0 -> 3.0.1
    新增ReportLAB class
    改进了人机交互模式
    修复了新建/修改作业时输入条为空时出现的问题

3.0.1 -> 3.0.2
    新增后台管理功能
    优化信息反馈系统

3.0.2 -> 3.0.3
    更改了配色方案
    移除了“新增作业”的背景模糊效果
    新增使用说明书
    在“新建作业”界面添加“将项目、范围、检查保存至列表”功能
    修改了软件图标

3.0.3 -> 3.1.0
    修复了“修改作业项”无法成功的BUG
    修复了“将项目、范围、检查保存至列表”不成功的BUG
    整理了主界面下部的按钮
    更改了“使用说明书”界面中的文本显示容器
    新增了设置功能
    新增了自动关机功能
    修改了主界面下方的文字位置
    在主界面新增时间显示
    增加了 1 个线程

3.1.0 -> 3.2.0
    将设置、删除、编辑等文字更换为图标
'''

import datetime
import json
import os
import sys
import threading
import time
import tkinter.ttk
from random import choice
from tkinter import *
from tkinter.messagebox import *


PATH = os.path.dirname(os.path.realpath(__file__))   #编写端
#PATH = os.getcwd()                                  #应用端

try:
    from win32 import win32api, win32gui, win32print
    from win32.lib import win32con

    sX = win32api.GetSystemMetrics(0)
    sY = win32api.GetSystemMetrics(1)

    if sX != 1920 or sY != 1080:
        showerror('警告', f'当前分辨率为{sX}x{sY}，程序拒绝运行，因为程序只能在1920x1080分辨率下运行。')
        os._exit(0)

except:
    pass

root = Tk()
root.title('作业助手3.0 by dyx')
root.wm_attributes('-fullscreen', 1)
root.geometry('1920x1080')
root.resizable(False, False)
root.iconbitmap(PATH + '\\icons\\Threat.contrast-black.ico')
#root.overrideredirect(1)
root.configure(bg = '#1E1E1E')


SubTab = {
    '语文' : 1,
    '数学' : 2,
    '英语' : 3,
    '物理' : 4,
    '化学' : 5,
    '生物' : 6,
    '技术' : 7,
    '政治' : 8,
    '历史' : 9,
    '地理' : 10
}

SubTabID = {
    1 : '语文',
    2 : '数学',
    3 : '英语',
    4 : '物理',
    5 : '化学',
    6 : '生物',
    7 : '技术',
    8 : '政治',
    9 : '历史',
    10 : '地理'
}

PathTab = {
    1 : PATH + '\\list\\chi.dyx',
    2 : PATH + '\\list\\mat.dyx',
    3 : PATH + '\\list\\eng.dyx',
    4 : PATH + '\\list\\phy.dyx',
    5 : PATH + '\\list\\che.dyx',
    6 : PATH + '\\list\\bio.dyx',
    7 : PATH + '\\list\\tec.dyx',
    8 : PATH + '\\list\\pol.dyx',
    9 : PATH + '\\list\\his.dyx',
    10 : PATH + '\\list\\geo.dyx',
    11 : PATH + '\\pages.dyx',
    12 : PATH + '\\givtime.dyx'
}

SubFrameList = ['Frame for SubjectFrame']
WorkFrameList = ['Frame for WorkFrame']
FrameList = ['Frame for frame in SubjectFrame']
WorkList = ['List of homework']
BackList = ['List of BackEditFrame']
SetList = ['List of SetEditFrame']



with open(PATH + '\\conf.json', 'r', encoding = 'UTF-8') as conf_file:
    SETTINGS = json.load(conf_file)

ADD_WIN_OPENED = 0
REPORT_WIN_OPENED = 0

COUNT = 1
VERSON = '3.1.0'



class ReportLAB:

    def __init__(self, typee, message):
        self.type = typee
        self.message = message

    def show(self):

        global REPORT_WIN_OPENED

        if not REPORT_WIN_OPENED:
            REPORT_WIN_OPENED = 1

            self.PPP = Toplevel(root)
            self.PPP.wm_attributes('-topmost', 1)
            self.PPP.overrideredirect(1)
            self.PPP.attributes('-alpha', 0.8)

            if self.type == 'good':
                self.color = 'green'
            elif self.type == 'bad':
                self.color = 'red'

            self.PPP.geometry('400x100+760+490')

            Label(self.PPP, text = self.message, font = ('微软雅黑', 22), fg = 'white', bg = self.color).place(x = 0, y = 0, width = 400, height = 100)

            def E():
                self.PPP.destroy()

                global REPORT_WIN_OPENED
                REPORT_WIN_OPENED = 0

            self.PPP.after(2000, E)
            self.PPP.mainloop()

class SubjectFrame:

    def __init__(self, sub_name, sub_id, x, y, height, width, index):
        self.sub_id = sub_id
        self.sub_name = sub_name
        self.x = x
        self.y = y
        self.height = height
        self.width = width
        self.index = index

    def add(self):
        global PathTab, ADD_WIN_OPENED

        if ADD_WIN_OPENED:
            return

        # -----------------------------------------------------------------------------
        
        xiang_mu_list_file = open(PathTab[self.sub_id], 'r', encoding = 'UTF-8')
        pages_file = open(PATH + '\\pages.dyx', 'r', encoding = 'UTF-8')
        give_in_time_file = open(PATH + '\\givtime.dyx', 'r', encoding = 'UTF-8')

        pages_list = pages_file.readline()
        give_in_time = give_in_time_file.readline()
        xiang_mu_list = xiang_mu_list_file.readline()

        xiang_mu_list_file.close()
        pages_file.close()
        give_in_time_file.close()
        
        # -----------------------------------------------------------------------------
        '''
        zu_dang = Tk()
        zu_dang.wm_attributes('-fullscreen', 1)
        zu_dang.attributes('-alpha', 0.3)
        '''
        chose_win = Tk()
        chose_win.overrideredirect(1)
        chose_win.configure(bg = '#37373D')
        chose_win.title('新建作业项')
        chose_win.geometry('430x530+745+275')
        chose_win.resizable(False, False)
        chose_win.wm_attributes('-topmost', 1)

        chose_win.option_add('*TCombobox*background', '#37373D')
        chose_win.option_add('*TCombobox*Font', ('微软雅黑', 15))
        chose_win.option_add('*TCombobox*Foreground', '#16825D')

        # -----------------------------------------------------------------------------

        def OFFF(*args):

            global ADD_WIN_OPENED
            ADD_WIN_OPENED = 0

            chose_win.destroy()
            #zu_dang.destroy()
            # root.focus_set()

        ffff = Frame(chose_win, bg = '#333333')

        Label(ffff, text = '新 建 作 业 项', font = ('微软雅黑', 20, 'bold'), bg = '#333333', fg = 'white').place(x = 0, y = 0, width = 400, height = 80)

        Label(ffff, text = '科  目：', font = ('微软雅黑', 16, 'bold'), bg = '#333333', fg = 'white').place(x = 20, y = 80, width = 80, height = 60)
        Label(ffff, text = self.sub_name, font = ('微软雅黑', 16), bg = '#333333', fg = 'white', anchor = 'w').place(x = 100, y = 80, width = 80, height = 60)

        Label(ffff, text = '项  目：', font = ('微软雅黑', 16, 'bold'), bg = '#333333', fg = 'white').place(x = 20, y = 140, width = 80, height = 60)
        xim = tkinter.ttk.Combobox(ffff, background = '#37373D', value = xiang_mu_list.split(), font = ('微软雅黑', 15))
        xim.set(xiang_mu_list.split()[0])
        xim.place(x = 100, y = 155, width = 250, height = 30)

        Label(ffff, text = '范  围：', font = ('微软雅黑', 16, 'bold'), bg = '#333333', fg = 'white').place(x = 20, y = 200, width = 80, height = 60)
        pag = tkinter.ttk.Combobox(ffff, background = '#37373D', value = pages_list.split(), font = ('微软雅黑', 15))
        pag.configure(background = '#37373D')
        pag.set(pages_list.split()[0])
        pag.place(x = 100, y = 215, width = 250, height = 30)

        Label(ffff, text = '检  查：', font = ('微软雅黑', 16, 'bold'), bg = '#333333', fg = 'white').place(x = 20, y = 260, width = 80, height = 60)
        git = tkinter.ttk.Combobox(ffff, background = '#37373D', value = give_in_time.split(), font = ('微软雅黑', 15))
        git.set(give_in_time.split()[2])
        git.place(x = 100, y = 275, width = 250, height = 30)

        def ok():
            global WorkList, COUNT

            COUNT += 1
            if ' ' in xim.get() or ' ' in pag.get() or ' ' in git.get():
                a1 = ReportLAB('bad', '不可以有空格哦~')
                a1.show()
                del a1
                return

            if xim.get() == '' or pag.get() == '' or git.get() == '':
                a1 = ReportLAB('bad', '不可以为空哦~')
                a1.show()
                del a1
                return

            WorkList.append([COUNT, self.sub_id, xim.get(), pag.get(), git.get()])

            ReLoad()
            OFFF()
            a1 = ReportLAB('good', '添加成功！')
            a1.show()
            del a1

        def xjp():
            os.system('osk')

        def savefile():
            xiang_mu_list_file = open(PathTab[self.sub_id], 'a', encoding = 'UTF-8')
            pages_file = open(PATH + '\\pages.dyx', 'a', encoding = 'UTF-8')
            give_in_time_file = open(PATH + '\\givtime.dyx', 'a', encoding = 'UTF-8')

            if xim.get() not in xiang_mu_list:
                xiang_mu_list_file.write(' ' + str(xim.get()))
            
            if pag.get() not in pages_list:
                pages_file.write(' ' + str(pag.get()))
            
            if git.get() not in give_in_time:
                give_in_time_file.write(' ' + str(git.get()))

            xiang_mu_list_file.close()
            pages_file.close()
            give_in_time_file.close()

            a1 = ReportLAB('good', '保存成功！')
            a1.show()
            del a1

        savebut = Button(ffff, text = '将项目、范围、检查保存至列表', font = ('微软雅黑', 13), relief = 'flat', borderwidth = 0, fg = 'white', bg = '#252526', activebackground = '#3C3C3C', activeforeground = 'white',  command = savefile)
        savebut.place(x = 20, y = 400, width = 280, height = 30)

        surebut = Button(ffff, text = '确定', font = ('微软雅黑', 13), relief = 'flat', borderwidth = 0, fg = 'white', bg = '#007ACC', activeforeground = 'white', activebackground = '#2E92D5', command = ok)
        surebut.place(x = 180, y = 450, width = 90, height = 30)

        unsurebut = Button(ffff, text = '取消', font = ('微软雅黑', 13), relief = 'flat', borderwidth = 0, fg = 'white', bg = '#007ACC', activeforeground = 'white', activebackground = '#2E92D5', command = OFFF)
        unsurebut.place(x = 290, y = 450, width = 90, height = 30)

        sjpbut = Button(ffff, text = '小键盘', font = ('微软雅黑', 13), relief = 'flat', borderwidth = 0, fg = 'white', bg = '#252526', activebackground = '#3C3C3C', activeforeground = 'white', command = xjp)
        sjpbut.place(x = 20, y = 450, width = 90, height = 30)

        ffff.place(x = 15, y = 15, width = 400, height = 500)

        ADD_WIN_OPENED = 1
        chose_win.bind('<Control-KeyPress-d>', OFFF)
        #zu_dang.mainloop()
        #chose_win.protocol('WM_WINDOW_DELETE', OFFF)
        chose_win.mainloop()

        '''
        def GET_FOCUS():
            while True:
                chose_win.focus_set()

        th = threading.Thread(target = GET_FOCUS, name = 'thread_1')
        th.setDaemon(True)
        th.start()
        '''

        #chose_win.focus_force()

    def clear(self):
        global WorkList

        for i in range(1, len(WorkList)):
            if WorkList[i][1] == self.sub_id:
                WorkList[i] = 0

        for i in range(len(WorkList)-1, 0, -1):
            if WorkList[i] == 0:
                del WorkList[i]

        ReLoad()

    def build_up(self):

        global FrameList

        big_frame = Frame(root, bg = '#252526')
        big_frame.place(x = self.x, y = self.y, height = self.height, width = self.width)

        name_to_put_on = list(self.sub_name)
        name_to_put_on = name_to_put_on[0] + '   ' + name_to_put_on[1]

        sub_label = Label(big_frame, text = name_to_put_on, font = ('微软雅黑', 27), bg = '#2D3313', fg = 'white') # #007ACC #0C2C05
        sub_label.place(x = 0, y = 0, width = self.width - 160, height = 40)

        add_button = Button(big_frame, text = '+', relief = 'flat', borderwidth = 0, font = ('楷体', 32, 'bold'), command = self.add, bg = '#005C99', fg = 'white', activeforeground = 'white', activebackground = '#2E92D5')
        add_button.place(x = self.width - 160, y = 0, width = 80, height = 40)

        del_button = Button(big_frame, text = '×', relief = 'flat', borderwidth = 0, font = ('楷体', 21, 'bold'), command = self.clear, bg = '#37373D', fg = 'red', activeforeground = 'red', activebackground = 'black')
        del_button.place(x = self.width - 80, y = 0, width = 80, height = 40)

        work_place = Frame(big_frame, bg = '#252526')
        work_place.place(x = 0, y = 40, width = self.width, height = self.height - 40)
        FrameList.append(work_place)

class WorkFrame:

    def __init__(self, count, sub_id, name, page, time):
        self.count = count
        self.sub_id = sub_id
        self.name = name
        self.page = page
        self.time = time

    def _get_color(self):
        global WorkList
        col = ['#4E4F51', '#3E3F41']

        cnt = 0
        for each in WorkList:
            if each[1] == self.sub_id:
                cnt += 1
            if each[0] == self.count:
                break

        return col[cnt % 2]

    def edit_item(self):
        global PathTab, ADD_WIN_OPENED

        if ADD_WIN_OPENED:
            return

        # -----------------------------------------------------------------------------

        xiang_mu_list_file = open(PathTab[self.sub_id], 'r', encoding = 'UTF-8')
        pages_file = open(PATH + '\\pages.dyx', 'r', encoding = 'UTF-8')
        give_in_time_file = open(PATH + '\\givtime.dyx', 'r', encoding = 'UTF-8')

        pages_list = pages_file.readline()
        give_in_time = give_in_time_file.readline()
        xiang_mu_list = xiang_mu_list_file.readline()

        xiang_mu_list_file.close()
        pages_file.close()
        give_in_time_file.close()

        # -----------------------------------------------------------------------------

        '''
        zu_dang = Tk()
        zu_dang.wm_attributes('-fullscreen', 1)
        zu_dang.attributes('-alpha', 0.3)
        '''

        chose_win = Tk()
        chose_win.overrideredirect(1)
        chose_win.configure(bg = '#37373D')
        chose_win.title('编辑作业项')
        chose_win.geometry('430x530+745+275')
        chose_win.resizable(False, False)
        chose_win.wm_attributes('-topmost', 1)

        chose_win.option_add('*TCombobox*background', '#37373D')
        chose_win.option_add('*TCombobox*Font', ('微软雅黑', 15))
        chose_win.option_add('*TCombobox*Foreground', '#16825D')

        # -----------------------------------------------------------------------------

        def OFFF(*args):

            global ADD_WIN_OPENED
            ADD_WIN_OPENED = 0

            chose_win.destroy()
            #zu_dang.destroy()
            # root.focus_set()

        ffff = Frame(chose_win, bg = '#333333')

        Label(ffff, text = '编 辑 作 业 项', font = ('微软雅黑', 20, 'bold'), bg = '#333333', fg = 'white').place(x = 0, y = 0, width = 400, height = 80)

        Label(ffff, text = '科  目：', font = ('微软雅黑', 16, 'bold'), bg = '#333333', fg = 'white').place(x = 20, y = 80, width = 80, height = 60)
        Label(ffff, text = SubTabID[self.sub_id], font = ('微软雅黑', 16), bg = '#333333', fg = 'white', anchor = 'w').place(x = 100, y = 80, width = 80, height = 60)

        Label(ffff, text = '项  目：', font = ('微软雅黑', 16, 'bold'), bg = '#333333', fg = 'white').place(x = 20, y = 140, width = 80, height = 60)
        xim = tkinter.ttk.Combobox(ffff, background = '#37373D', value = xiang_mu_list.split(), font = ('微软雅黑', 15))
        xim.set(self.name)
        xim.place(x = 100, y = 155, width = 250, height = 30)

        Label(ffff, text = '范  围：', font = ('微软雅黑', 16, 'bold'), bg = '#333333', fg = 'white').place(x = 20, y = 200, width = 80, height = 60)
        pag = tkinter.ttk.Combobox(ffff, background = '#37373D', value = pages_list.split(), font = ('微软雅黑', 15))
        pag.set(self.page)
        pag.place(x = 100, y = 215, width = 250, height = 30)

        Label(ffff, text = '检  查：', font = ('微软雅黑', 16, 'bold'), bg = '#333333', fg = 'white').place(x = 20, y = 260, width = 80, height = 60)
        git = tkinter.ttk.Combobox(ffff, background = '#37373D', value = give_in_time.split(), font = ('微软雅黑', 15))
        git.set(self.time)
        git.place(x = 100, y = 275, width = 250, height = 30)

        def ok():
            global WorkList, COUNT

            COUNT += 1
            if ' ' in xim.get() or ' ' in pag.get() or ' ' in git.get():
                a1 = ReportLAB('bad', '不可以有空格哦~')
                a1.show()
                del a1
                return

            if xim.get() == '' or pag.get() == '' or git.get() == '':
                a1 = ReportLAB('bad', '不可以为空哦~')
                a1.show()
                del a1
                return

            for i in range(1, len(WorkList)):
                if WorkList[i][0] == self.count:
                    WorkList[i][2] = xim.get()
                    WorkList[i][3] = pag.get()
                    WorkList[i][4] = git.get()

            ReLoad()
            OFFF()
            a1 = ReportLAB('good', '修改成功！')
            a1.show()
            del a1

        def xjp():
            os.system('osk')

        def savefile():
            xiang_mu_list_file = open(PathTab[self.sub_id], 'a', encoding = 'UTF-8')
            pages_file = open(PATH + '\\pages.dyx', 'a', encoding = 'UTF-8')
            give_in_time_file = open(PATH + '\\givtime.dyx', 'a', encoding = 'UTF-8')

            if xim.get() not in xiang_mu_list:
                xiang_mu_list_file.write(' ' + str(xim.get()))
            
            if pag.get() not in pages_list:
                pages_file.write(' ' + str(pag.get()))
            
            if git.get() not in give_in_time:
                give_in_time_file.write(' ' + str(git.get()))

            xiang_mu_list_file.close()
            pages_file.close()
            give_in_time_file.close()

            a1 = ReportLAB('good', '保存成功！')
            a1.show()
            del a1

        savebut = Button(ffff, text = '将项目、范围、检查保存至列表', font = ('微软雅黑', 13), relief = 'flat', borderwidth = 0, fg = 'white', bg = '#252526', activebackground = '#3C3C3C', activeforeground = 'white',  command = savefile)
        savebut.place(x = 20, y = 400, width = 280, height = 30)

        surebut = Button(ffff, text = '确定', font = ('微软雅黑', 13), relief = 'flat', borderwidth = 0, fg = 'white', bg = '#007ACC', activeforeground = 'white', activebackground = '#2E92D5', command = ok)
        surebut.place(x = 180, y = 450, width = 90, height = 30)

        unsurebut = Button(ffff, text = '取消', font = ('微软雅黑', 13), relief = 'flat', borderwidth = 0, fg = 'white', bg = '#007ACC', activeforeground = 'white', activebackground = '#2E92D5', command = OFFF)
        unsurebut.place(x = 290, y = 450, width = 90, height = 30)

        sjpbut = Button(ffff, text = '小键盘', font = ('微软雅黑', 13), relief = 'flat', borderwidth = 0, fg = 'white', bg = '#252526', activebackground = '#3C3C3C', activeforeground = 'white', command = xjp)
        sjpbut.place(x = 20, y = 450, width = 90, height = 30)

        ffff.place(x = 15, y = 15, width = 400, height = 500)

        ADD_WIN_OPENED = 1
        chose_win.bind('<Control-KeyPress-d>', OFFF)
        #zu_dang.mainloop()
        #chose_win.protocol('WM_WINDOW_DELETE', OFFF)
        chose_win.mainloop()

    def del_item(self):
        global WorkList

        for i in range(1, len(WorkList)):
            if WorkList[i][0] == self.count:
                del WorkList[i]
                break

        ReLoad()

    def config(self):
        global WorkFrameList

        self.f = Frame(master = FrameList[self.sub_id], bg = self._get_color())
        WorkFrameList.append(self.f)

        self.l1 = Label(WorkFrameList[-1], text = self.name, bg = self._get_color(), fg = 'white', font = ('微软雅黑', 25), anchor = 'w', justify = 'left').pack(side = TOP, fill = X)
        self.b_del = Button(WorkFrameList[-1], text = '删除', bg = '#4E1A0F', fg = '#C54026', relief = 'flat', font = ('微软雅黑', 13), borderwidth = 0, height = 1, command = self.del_item).pack(side = RIGHT)
        self.b_edit = Button(WorkFrameList[-1], text = '编辑', bg = '#212E3A', fg = '#597C9D', relief = 'flat', font = ('微软雅黑', 13), borderwidth = 0, height = 1, command = self.edit_item).pack(side = RIGHT)
        self.l2 = Label(WorkFrameList[-1], text = self.page, bg = self._get_color(), fg = '#A5CDAA', font = ('微软雅黑', 19), anchor = 'w', justify = 'left').pack(side = LEFT)
        self.l3 = Label(WorkFrameList[-1], text = self.time, bg = self._get_color(), fg = '#9CCDC4', font = ('微软雅黑', 19), anchor = 'w', justify = 'left').pack(side = RIGHT)

        WorkFrameList[-1].pack(side = TOP, fill = X)

class BackEditFrame:

    def __init__(self, father, sub_name, sub_id, x, y, width, height):
        self.father = father
        self.sub_name = sub_name
        self.sub_id = sub_id
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def config(self):

        global PathTab

        self.middle_frame = Frame(self.father)
        self.middle_frame.place(x = self.x, y = self.y, width = self.width, height = self.height)

        title = Label(self.middle_frame, text = self.sub_name, bg = '#3C3C3C', fg = 'white', font = ('微软雅黑', 18))
        title.place(x = 0, y = 0, width = self.width, height = 40)

        self.fra = Text(self.middle_frame, bg = '#252526', fg = 'white', font = ('微软雅黑', 16), borderwidth = 0)
        self.fra.place(x = 0, y = 40, width = self.width, height = self.height - 40)

        fil = open(PathTab[self.sub_id], 'r', encoding = 'UTF-8')
        lis = fil.readline().split()
        fil.close()

        for each in lis:
            self.fra.insert(INSERT, each + '\n')

    def ok(self):
        mmm = self.fra.get(1.0, END).split()

        global PathTab
        fil = open(PathTab[self.sub_id], 'w', encoding = 'UTF-8')
        for i in range(len(mmm)):
            fil.write(mmm[i] + ' ')
        fil.close()

class SetEditFrame:

    def __init__(self, master, thing, x, y, text_on):
        self.thing = thing
        self.master = master
        self.x = x
        self.y = y
        self.text_on = text_on

    def saveout(self):
        global SETTINGS

        with open(PATH + '\\conf.json', 'w', encoding = 'UTF-8') as conf_file:
            json.dump(SETTINGS, conf_file)

    def ok(self, val):
        global SETTINGS

        SETTINGS[self.thing] = val

        self.saveout()

        if val == 1:
            self.lab.config(text = self.text_on + '      开    ')
        elif val == 0:
            self.lab.config(text = self.text_on + '      关    ')
        else:
            self.lab.config(text = self.text_on + f'      {val}    ')

        a1 = ReportLAB('good', '修改成功！')
        a1.show()
        del a1

    def create(self):

        val = SETTINGS[self.thing]
        self.widget = Frame(self.master, bg = '#1e1e1e')
        
        self.lab = Label(self.widget, bg = '#1e1e1e', fg = 'white', font = ('微软雅黑', 25), width = 20)
        if val == 1:
            self.lab.config(text = self.text_on + '      开    ')
        elif val == 0:
            self.lab.config(text = self.text_on + '      关    ')
        else:
            self.lab.config(text = self.text_on + f'      {val}    ')
        self.lab.pack(side = 'left')
        self.but1 = Button(self.widget, text = '开', font = ('微软雅黑', 20), bg = 'green', fg = 'lime', activebackground = '#006000', activeforeground = 'green', width = 10, height = 1, borderwidth = 0, relief = GROOVE, command = lambda: self.ok(1))
        self.but1.pack(side = 'left')
        self.but2 = Button(self.widget, text = '关', font = ('微软雅黑', 20), bg = '#8D1D2C', fg = 'red', activebackground = '#6A1621', activeforeground = '#8D1D2C', width = 10, height = 1, borderwidth = 0, relief = GROOVE, command = lambda: self.ok(0))
        self.but2.pack(side = 'left')

        self.widget.place(x = self.x, y = self.y)

class ScrolledText(Text):
    def __init__(self, master = None, **kw):
        self.frame = Frame(master)
        self.vbar = Scrollbar(self.frame)
        self.vbar.pack(side = RIGHT, fill = Y)

        kw.update({'yscrollcommand': self.vbar.set})
        Text.__init__(self, self.frame, borderwidth = 0, **kw)
        self.config(selectbackground = '#181818')
        self.pack(side = LEFT, fill = BOTH, expand = True)
        self.vbar['command'] = self.yview

        text_meths = vars(Text).keys()
        methods = vars(Pack).keys() | vars(Grid).keys() | vars(Place).keys()
        methods = methods.difference(text_meths)

        for m in methods:
            if m[0] != '_' and m != 'config' and m != 'configure':
                setattr(self, m, getattr(self.frame, m))

    def __str__(self):
        return str(self.frame)

    def stop(self):
        self['state'] = 'disabled'

def SetEdit():

    global SETTINGS, SetList

    SetList = ['List of SetEditFrame']

    sets_win = Tk()
    sets_win.wm_attributes('-topmost', 1)
    sets_win.wm_attributes('-fullscreen', 1)
    sets_win.title('设置')
    sets_win.config(bg = '#1e1e1e')

    def off(*args):
        sets_win.destroy()

    sets_win.bind('<x>', off)

    SetList.append(SetEditFrame(sets_win, 'AUTOSAVE', 20, 100, '自动保存'))
    SetList.append(SetEditFrame(sets_win, 'AUTOOFF', 20, 200, '自动关机'))

    for i in range(1, len(SetList)):
        SetList[i].create()

    Button(sets_win, text = '返  回', font = ('微软雅黑', 17), relief = GROOVE, command = off, borderwidth = 0, fg = 'white', bg = '#252526', activebackground = '#3C3C3C', activeforeground = 'white').place(x = 1730, y = 1000, height = 60, width = 180)

    sets_win.mainloop()


def BackEdit():

    global BackList

    BackList = ['List of BackEditFrame']

    edit_win = Tk()
    edit_win.wm_attributes('-topmost', 1)
    edit_win.wm_attributes('-fullscreen', 1)
    edit_win.config(bg = '#1E1E1E')

    for i in range(1, 11):
        BackList.append(BackEditFrame(edit_win, SubTabID[i], i, 20 + ((i-1)%5)*300, 20 + 480 * (i//6), 300, 480))
        BackList[-1].config()
    BackList.append(BackEditFrame(edit_win, '范围', 11, 1600, 20, 300, 480))
    BackList[-1].config()
    BackList.append(BackEditFrame(edit_win, '上交时间', 12, 1600, 500, 300, 480))
    BackList[-1].config()

    def sure():
        for i in range(1, 13):
            BackList[i].ok()
        cancel()

        a1 = ReportLAB('good', '编辑成功！')
        a1.show()
        del a1


    def cancel(*args):
        edit_win.destroy()

    Button(edit_win, text = '保存修改', font = ('微软雅黑', 17), relief = GROOVE, command = sure, borderwidth = 0, fg = 'white', bg = '#252526', activebackground = '#3C3C3C', activeforeground = 'white').place(x = 1730, y = 1000, height = 60, width = 180)
    Button(edit_win, text = '取  消', font = ('微软雅黑', 17), relief = GROOVE, command = cancel, borderwidth = 0, fg = 'white', bg = '#252526', activebackground = '#3C3C3C', activeforeground = 'white').place(x = 1530, y = 1000, height = 60, width = 180)

    def open_osk():
        os.system('osk')

    osk = Button(edit_win, text = '小 键 盘', font = ('微软雅黑', 17), relief = GROOVE, command = open_osk, borderwidth = 0, fg = 'white', bg = '#252526', activebackground = '#3C3C3C', activeforeground = 'white')
    osk.place(x = 20, y = 1000, height = 60, width = 180)
    #edit_win.bind('<x>', cancel)
    edit_win.mainloop()

def PreLoad():
    global WorkList, COUNT

    fil = open(PATH + '\\history\\today.dyx', 'r', encoding = 'UTF-8')
    WorkList = WorkList + fil.readlines()
    fil.close()

    for i in range(1, len(WorkList)):
        WorkList[i] = WorkList[i].split()

        WorkList[i][0] = int(WorkList[i][0])
        WorkList[i][1] = int(WorkList[i][1])

    for i in range(1, len(WorkList)):
        WorkList[i][0] = i

    COUNT = len(WorkList) - 1

    ReLoad()

def ReLoad():
    global WorkFrameList, WorkList

    while len(WorkFrameList) != 1:
        WorkFrameList[1].destroy()
        del WorkFrameList[1]

    for i in range(1, len(WorkList)):
        new = WorkFrame(count = WorkList[i][0], sub_id = WorkList[i][1], name = WorkList[i][2], page = WorkList[i][3], time = WorkList[i][4])
        new.config()

    global SETTINGS

    if SETTINGS['AUTOSAVE']:
        save()

def save():
    global WorkList

    res = []
    for i in range(1, len(WorkList)):
        WorkList[i][0] = str(WorkList[i][0])
        WorkList[i][1] = str(WorkList[i][1])
        res.append(' '.join(WorkList[i]))

    fil = open(PATH + '\\history\\today.dyx', 'w', encoding = 'UTF-8')
    fil.write('\n'.join(res))
    fil.close()

    for i in range(1, len(WorkList)):
        WorkList[i][0] = int(WorkList[i][0])
        WorkList[i][1] = int(WorkList[i][1])

def DelTaskAll():

    if not askyesno('警告', '请确认操作：删除全部作业项\n此为不可逆操作，删除后无法复原\n是否继续？'):
        return

    global WorkList
    WorkList = ['List of homework']
    ReLoad()

def OFF(*args):
    save()
    root.destroy()
    sys.exit()

def helper():
    global VERSON

    help_win = Tk()
    help_win.title('使用说明书')
    help_win.attributes('-fullscreen', True)
    help_win.wm_attributes('-topmost', True)
    help_win.config(bg = '#1e1e1e')

    Label(help_win, text = f'班级作业助手 {VERSON} 使用说明书', bg = '#1e1e1e', fg = 'white', anchor = W, font = ('微软雅黑', 50)).place(x = 80, y = 40, width = 1760, height = 100)

    title_label = Label(help_win, bg = '#111111', fg = 'white', anchor = W, justify = 'left',font = ('微软雅黑', 35), borderwidth = 0)
    title_label.place(x = 320, y = 140, width = 1480, height = 100)

    inner_text = ScrolledText(help_win, bg = '#181818', fg = 'white', font = ('微软雅黑', 19))
    inner_text.place(x = 320, y = 240, height = 700, width = 1480)

    def reLoadLabel(tit, mes):
        title_label.config(text = tit)
        inner_text['state'] = 'normal'
        inner_text.delete(1.0, END)
        inner_text.insert(INSERT, mes)
        inner_text['state'] = 'disabled'


    but1 = Button(help_win, text = '新建作业项', fg = 'white', bg = '#212E3A', font = ('微软雅黑', 20), activebackground = '#3F9CD6', activeforeground = 'white', relief = GROOVE, borderwidth = 0,command = lambda : reLoadLabel('新建作业项', '点击每个学科框上部的“+”按钮即可添加作业。单击“小键盘”可调用出屏幕小键盘。\n\n作业项可以从预设列表中选择，也可以自由编辑，但是要注意不可以为空或者含有空格。此外，过长的作业名称可能会显示不全。\n\n“范围”选项，可以是页码等内容。\n\n“检查”指的是上交时间。\n\n“将项目、范围、检查保存至列表”按钮可以将自定义的内容添加至列表内，重复的内容自动跳过。你可以去后台编辑处进行整理。\n\n本程序对于每个输入框中的内容仅做空格检查，不检查违禁词或者内容的逻辑性。这意味着你们可以整活，但最好不要。\n\n此外，程序不会自动修改内容，比如“明天交”到第二天不会自动改为“今天交”。'))
    but2 = Button(help_win, text = '编辑作业项', fg = 'white', bg = '#212E3A', font = ('微软雅黑', 20), activebackground = '#3F9CD6', activeforeground = 'white', relief = GROOVE, borderwidth = 0,command = lambda : reLoadLabel('编辑作业项', '点击每条作业项中的“编辑”即可修改作业项。用法与新增作业项基本相同，此处不再叙述。'))
    but3 = Button(help_win, text = '删除作业项', fg = 'white', bg = '#212E3A', font = ('微软雅黑', 20), activebackground = '#3F9CD6', activeforeground = 'white', relief = GROOVE, borderwidth = 0,command = lambda : reLoadLabel('删除作业项', '一共有三种方法可以删除作业项：单项删除、整科删除、全部删除。请注意，这三种删除方式都是不可逆的，操作后无法还原。\n\n单项删除：点击作业项上的“删除”按钮。\n\n整科删除：单击作业框上的“×”按钮进行删除。\n\n全部删除：软件右下角有“删除全部作业项”按钮。该命令在执行前会弹窗询问，以防止误触（其他二者不会弹窗询问）。'))
    but4 = Button(help_win, text = '后台管理', fg = 'white', bg = '#212E3A', font = ('微软雅黑', 20), activebackground = '#3F9CD6', activeforeground = 'white', relief = GROOVE, borderwidth = 0,command = lambda : reLoadLabel('后台管理', '主界面>>后台管理 可以编辑每一门学科的作业列表，以及预设的范围列表和上交时间列表。'))
    but5 = Button(help_win, text = '设置', fg = 'white', bg = '#212E3A', font = ('微软雅黑', 20), activebackground = '#3F9CD6', activeforeground = 'white', relief = GROOVE, borderwidth = 0,command = lambda : reLoadLabel('设置', '在主界面>>设置中可以修改一些设置。通过点击按钮来修改设置。修改的设置会自动立刻保存，但部分设置要在软件下一次启动时生效。\n\n自动保存：\n自动记录添加的作业，以免意外或非法退出造成的数据丢失。\n\n自动关机：\n开启后，电脑将在21:44:40时启动关机30秒倒计时，30秒后自动关机。\n\n设置功能仍在完善中'))
    but6 = Button(help_win, text = '关于', fg = 'white', bg = '#212E3A', font = ('微软雅黑', 20), activebackground = '#3F9CD6', activeforeground = 'white', relief = GROOVE, borderwidth = 0,command = lambda : reLoadLabel(f'班级作业助手 {VERSON}', '开发者：杭州第二中学钱江学校 202214 丁誉轩\n\nQQ: 431495254\n\nBilibili: 卢丁喆丰群\n所有更新消息将在这个账号第一时间发布，敬请关注\n\nCSDN: do_while_false\n\n软件官方QQ群：704376858\n你可以在这个群内下载最新版本的软件、反馈问题，也可以与作者交流\n\n源代码共计1723行，不公开,但是你可以贿赂贿赂我：）'))
    but7 = Button(help_win, text = '未来版本前瞻', fg = 'white', bg = '#212E3A', font = ('微软雅黑', 20), activebackground = '#3F9CD6', activeforeground = 'white', relief = GROOVE, borderwidth = 0,command = lambda : reLoadLabel('未来版本前瞻', '未来的版本中，将要实现：\n\n可拖动的作业容器\n每个学科单独的范围、上交时间列表（数据库2.0\n\n等等。将花整个高中的时间维护此软件。'))
    but8 = Button(help_win, text = '更新日志', fg = 'white', bg = '#212E3A', font = ('微软雅黑', 20), activebackground = '#3F9CD6', activeforeground = 'white', relief = GROOVE, borderwidth = 0,command = lambda : reLoadLabel('更新日志', NEWS))

    but1.place(x = 120, y = 240, height = 60, width = 200)
    but2.place(x = 120, y = 300, height = 60, width = 200)
    but3.place(x = 120, y = 360, height = 60, width = 200)
    but4.place(x = 120, y = 420, height = 60, width = 200)
    but5.place(x = 120, y = 480, height = 60, width = 200)
    but6.place(x = 120, y = 540, height = 60, width = 200)
    but7.place(x = 120, y = 600, height = 60, width = 200)
    but8.place(x = 120, y = 660, height = 60, width = 200)

    def back(*args):
        help_win.destroy()
    
    Button(help_win, text = '好 的', font = ('微软雅黑', 17), relief = GROOVE, command = back, borderwidth = 0, fg = 'white', bg = '#252526', activebackground = '#3C3C3C', activeforeground = 'white').place(x = 1730, y = 1000, height = 60, width = 180)

    reLoadLabel('新建作业项', '点击每个学科框上部的“+”按钮即可添加作业。单击“小键盘”可调用出屏幕小键盘。\n\n作业项可以从预设列表中选择，也可以自由编辑，但是要注意不可以为空或者含有空格。此外，过长的作业名称可能会显示不全。\n\n“范围”选项，可以是页码等内容。\n\n“检查”指的是上交时间。\n\n“将项目、范围、检查保存至列表”按钮可以将自定义的内容添加至列表内，重复的内容自动跳过。你可以去后台编辑处进行整理。\n\n本程序对于每个输入框中的内容仅做空格检查，不检查违禁词或者内容的逻辑性。这意味着你们可以整活，但最好不要。\n\n此外，程序不会自动修改内容，比如“明天交”到第二天不会自动改为“今天交”。')

    help_win.bind('<x>', back)
    help_win.mainloop()

def shuaxin():

    global SETTINGS

    while True:
        timenow = str(datetime.datetime.now())
        toh = int(timenow[11:13])
        tom = int(timenow[14:16])
        tos = int(timenow[17:19])
        tts = 60 - tos

        if toh == 21 and tom >= 44 and tos >= 40:
            if SETTINGS['AUTOOFF']:
                os.system('shutdown -s -t 30 -c 班级作业助手-自动关机：电脑将在30秒后关机')
        
        main_time_text.config(text = timenow[0:19])
        time.sleep(1)

'''
def ING():
    a1 = ReportLAB('good', '正在开发中，敬请期待！')
    a1.show()
    del a1
def ToolBox():

    Tool_win = Tk()
    Tool_win.config(bg = '#1E1E1E')
    Tool_win.attributes('-fullscreen', True)
    Tool_win.title('更多功能')
    Tool_win.wm_attributes('-topmost', True)

    def off(*args):
        Tool_win.destroy()

    many_homework_but = Button(Tool_win, text = '多作业模式', borderwidth = 0,font = ('微软雅黑', 20), relief = GROOVE, fg = 'white', bg = '#252526', activebackground = '#3C3C3C', activeforeground = 'white', command = ING)
    many_homework_but.place(x = 20, y = 20, width = 455, height = 220)

    power_shell_but = Button(Tool_win, text = '后台管理\n\n管理作业列表、范围、检查方式列表', borderwidth = 0,font = ('微软雅黑', 20), relief = GROOVE, fg = 'white', bg = '#252526', activebackground = '#3C3C3C', activeforeground = 'white', command = BackEdit)
    power_shell_but.place(x = 495, y = 20, width = 455, height = 220)

    shuo_ming_but = Button(Tool_win, text = '使用说明书', borderwidth = 0,font = ('微软雅黑', 20), relief = GROOVE, fg = 'white', bg = '#252526', activebackground = '#3C3C3C', activeforeground = 'white', command = helper)
    shuo_ming_but.place(x = 970, y = 20, width = 455, height = 220)



    Button(Tool_win, text = '好 的', font = ('微软雅黑', 17), relief = GROOVE, command = off, borderwidth = 0, fg = 'white', bg = '#252526', activebackground = '#3C3C3C', activeforeground = 'white').place(x = 1730, y = 1000, height = 60, width = 180)

    Tool_win.bind('x', off)

    Tool_win.mainloop()

ToolBut = Button(root, text = '工具箱', font = ('微软雅黑', 17), relief = GROOVE, command = ToolBox, borderwidth = 0, fg = 'white', bg = '#252526', activebackground = '#3C3C3C', activeforeground = 'white')
ToolBut.place(x = 220, y = 1000, width = 180, height = 60)
'''

SubFrameList.append(SubjectFrame('语文', 1, 20, 20, 920/3, 1840/3, 1))
SubFrameList.append(SubjectFrame('数学', 2, 1960/3, 20, 920/3, 1840/3, 2))
SubFrameList.append(SubjectFrame('英语', 3, 3860/3, 20, 920/3, 1840/3, 3))
SubFrameList.append(SubjectFrame('物理', 4, 20, 40 + 920/3, 920/3, 455, 4))
SubFrameList.append(SubjectFrame('化学', 5, 495, 40 + 920/3, 920/3, 455, 5))
SubFrameList.append(SubjectFrame('生物', 6, 970, 40 + 920/3, 920/3, 455, 6))
SubFrameList.append(SubjectFrame('技术', 7, 1445, 40 + 920/3, 920/3, 455, 7))
SubFrameList.append(SubjectFrame('政治', 8, 20, 60 + 2 * 920/3, 920/3, 1840/3, 8))
SubFrameList.append(SubjectFrame('历史', 9, 1960/3, 60 + 2 * 920/3, 920/3, 1840/3, 9))
SubFrameList.append(SubjectFrame('地理', 10, 3860/3, 60 + 2 * 920/3, 920/3, 1840/3, 10))

for i in range(1, len(SubFrameList)):
    SubFrameList[i].build_up()


PreLoad()


Button(root, relief = GROOVE, text = '保存并退出', font = ('微软雅黑', 13), borderwidth = 0, fg = 'white', bg = '#49494B', activebackground = '#3C3C3C', activeforeground = 'white', command = OFF).place(x = 20, y = 1030, width = 180, height = 30)
Button(root, relief = GROOVE, text = '最小化', font = ('微软雅黑', 13), borderwidth = 0, fg = 'white', bg = '#333333', activebackground = '#3C3C3C', activeforeground = 'white', command = lambda : root.iconify()).place(x = 20, y = 1000, width = 180, height = 30)

shuo_ming_but = Button(root, text = '设置', font = ('微软雅黑', 17), relief = GROOVE, command = SetEdit, fg = 'white', bg = '#252526', borderwidth = 0, activebackground = '#3C3C3C', activeforeground = 'white')
shuo_ming_but.place(x = 1320, y = 1000, width = 80, height = 60)

settings_but = Button(root, text = '帮助', font = ('微软雅黑', 17), relief = GROOVE, command = helper, fg = 'white', bg = '#252526', borderwidth = 0, activebackground = '#3C3C3C', activeforeground = 'white')
settings_but.place(x = 1420, y = 1000, width = 80, height = 60)

power_shell_but = Button(root, text = '后台管理', font = ('微软雅黑', 17), relief = GROOVE, command = BackEdit, borderwidth = 0, fg = 'white', bg = '#252526', activebackground = '#3C3C3C', activeforeground = 'white')
power_shell_but.place(x = 1520, y = 1000, width = 180, height = 60)

del_task_button_all = Button(root, text = '删除全部作业项', font = ('微软雅黑', 17), relief = GROOVE, command = DelTaskAll, borderwidth = 0, fg = 'white', bg = '#252526', activebackground = '#3C3C3C', activeforeground = 'white')
del_task_button_all.place(x = 1720, y = 1000, width = 180, height = 60)

Label(root, text = 'Powered by 414', bg = '#1e1e1e', fg = '#0089E6', font = ('Consolas', 24),anchor = 'w').place(x = 240, y = 990, width = 330, height = 40)

main_time_text = Label(root, bg = '#1e1e1e', fg = 'white', font = ('Consolas', 24),anchor = 'w')
main_time_text.place(x = 240, y = 1030, width = 500, height = 40)
#Label(root, text = '414', bg = '#1E1E1E', fg = '#0089E6', font = ('Courier new', 42)).place(x = 880, y = 1020, width = 160, height = 60)




th = threading.Thread(target = shuaxin, name = 'thread_1')
th.setDaemon(True)
th.start()


root.protocol('WM_WINDOW_DELETE', OFF)
root.bind('<x>', OFF)
root.mainloop()
