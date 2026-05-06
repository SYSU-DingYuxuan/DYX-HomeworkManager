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
    更新了文件系统，为每门学科添加了单独的“范围”和“检查”列表
    更新了后台管理系统，以适应新的文件系统
    将设置、帮助、删除、编辑等文字更换为图标
    修改软件进程名为“班级作业助手 by DYX”
    在帮助界面添加了“前往B站”的按钮

3.2.0 -> 3.3.0
    新增编辑学科栏目的功能
    优化部分用户体验

3.3.0 -> 3.3.5
    禁止了在作业输入中输入换行
    修复已知问题

3.3.5 -> 3.4.0
    添加“更新内容”窗口
    在主界面新增“班级标语”功能
    在窗口左上角和右上角分别添加一组“最小化”和“关闭”按钮
    解除了输入中对空格和空缺的禁用，也就是说现在开始可以输入空格，也可以不填
    优化了操作反馈提示
    优化了用户体验：在单击“小键盘”后，会自动聚焦到之前所编辑的文本框，不需要再次单击
    修改“删除”图标为深色图标
    重置了软件对于平面分辨率的检测，现在检测到屏幕分辨率变化时会立刻退出程序
    修复了作业列表为空时无法正常布置作业的问题
    修复了在设置“自动保存”选项后无法配置主界面学科的问题

3.4.0 -> 3.4.1
    修复了输入时换行检测发生的错误。同时修改了规则：不再提示禁止输入换行，而是直接删除换行符
    修改输入时“范围”选项的默认项为空
    优化了小键盘的使用体验，去除了子线程 cmd 窗口
    修复了主界面时间不变的 BUG：是由于局部导入全局引用引起的
    修复了分辨率错误检测的问题，现在可以实时监测屏幕分辨率的变化
    在“添加标语”窗口中添加“小键盘”按钮

'''

import datetime
import json
import os
import subprocess
import sys
import threading
import time
import tkinter.ttk
import webbrowser
from random import choice
from tkinter import *
from tkinter.messagebox import *

import psutil
import setproctitle


PATH = os.path.dirname(os.path.realpath(__file__))   #编写端
#PATH = os.getcwd()                                  #应用端

root = Tk()
root.title('班级作业助手 by DYX')
root.wm_attributes('-fullscreen', 1)
root.iconbitmap(PATH + '\\icons\\Threat.contrast-black.ico')
#root.overrideredirect(1)
root.configure(bg = '#1E1E1E')

prrrr = psutil.Process()
process_name = prrrr.name()

if root.winfo_screenwidth() != 1920 or root.winfo_screenheight() != 1080:

    showerror('警告', f'当前分辨率为{root.winfo_screenwidth()}x{root.winfo_screenheight()}，程序拒绝运行，因为程序只能在1920x1080分辨率下运行。其他分辨率下运行软件会导致界面显示不全。')
    os.system(f'taskkill -im \"{process_name}\" -f')



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
    1 : PATH + '\\list\\chi',
    2 : PATH + '\\list\\mat',
    3 : PATH + '\\list\\eng',
    4 : PATH + '\\list\\phy',
    5 : PATH + '\\list\\che',
    6 : PATH + '\\list\\bio',
    7 : PATH + '\\list\\tec',
    8 : PATH + '\\list\\pol',
    9 : PATH + '\\list\\his',
    10 : PATH + '\\list\\geo',
}

SubFrameList = ['Frame for SubjectFrame']
WorkFrameList = ['Frame for WorkFrame']
FrameList = ['Frame for frame in SubjectFrame']
WorkList = ['List of homework']
BackList = ['List of BackEditFrame']
SetList = ['List of SetEditFrame']



with open(PATH + '\\conf.json', 'r', encoding = 'UTF-8') as conf_file:
    SETTINGS = json.load(conf_file)
SETTINGS['SUBSTATE'] = list(SETTINGS['SUBSTATE'])

with open(PATH + '\\pack_pos.json', 'r', encoding = 'UTF-8') as pos_file:
    POSITIONS = json.load(pos_file)

ADD_WIN_OPENED = 0
REPORT_WIN_OPENED = 0
MAIN_EDIT_WIN_OPENED = 0
BIAO_YU_WIN_OPENED = 0
OSK_OPENED = 0

COUNT = 1
VERSION = '3.4.1'
BLANK = '#@$%!'
BINDER = '*&^}'

def open_osk():
    '''
    global OSK_OPENED

    if OSK_OPENED == 1:
        return
    OSK_OPENED = 1
    '''
    subprocess.Popen('osk', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, creationflags=0x08000000)


class ReportLAB:

    def __init__(self, typee = None, message = None):
        self.type = typee
        self.message = message

    def show(self, typee, message):

        global REPORT_WIN_OPENED

        self.type = typee
        self.message = message

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

reporter = ReportLAB()


class SubjectFrame:

    def __init__(self, sub_name, sub_id, x, y, height, width, index):
        self.sub_id = sub_id
        self.sub_name = sub_name
        self.x = x
        self.y = y
        self.height = height
        self.width = width
        self.index = index

    def reloadPos(self, pos_char):

        char = pos_char.split(' ')

        self.x = float(char[0])
        self.y = float(char[1])
        self.height = float(char[2])
        self.width = float(char[3])

        self.build_up('re')

    def hide(self):
        self.big_frame.place_forget()

    def add(self):
        global PathTab, ADD_WIN_OPENED

        if ADD_WIN_OPENED:
            return

        # -----------------------------------------------------------------------------

        self.focus_object = 'xim'

        xiang_mu_list_file = open(PathTab[self.sub_id] + '\\list.dyx', 'r', encoding = 'UTF-8')
        pages_file = open(PathTab[self.sub_id] + '\\pages.dyx', 'r', encoding = 'UTF-8')
        give_in_time_file = open(PathTab[self.sub_id] + '\\givtime.dyx', 'r', encoding = 'UTF-8')

        pages_list = pages_file.readlines()
        give_in_time = give_in_time_file.readlines()
        xiang_mu_list = xiang_mu_list_file.readlines()

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
            # zu_dang.destroy()
            # root.focus_set()

        def give_focus(a):
            self.focus_object = a

        ffff = Frame(chose_win, bg = '#333333')

        Label(ffff, text = '新 建 作 业 项', font = ('微软雅黑', 20, 'bold'), bg = '#333333', fg = 'white').place(x = 0, y = 0, width = 400, height = 80)

        Label(ffff, text = '科  目：', font = ('微软雅黑', 16, 'bold'), bg = '#333333', fg = 'white').place(x = 20, y = 80, width = 80, height = 60)
        Label(ffff, text = self.sub_name, font = ('微软雅黑', 16), bg = '#333333', fg = 'white', anchor = 'w').place(x = 100, y = 80, width = 80, height = 60)


        Label(ffff, text = '项  目：', font = ('微软雅黑', 16, 'bold'), bg = '#333333', fg = 'white').place(x = 20, y = 140, width = 80, height = 60)
        
        if len(xiang_mu_list) == 0:
            xiang_mu_list.append(' ')

        xim = tkinter.ttk.Combobox(ffff, background = '#37373D', value = xiang_mu_list, font = ('微软雅黑', 15))
        xim.set(xiang_mu_list[0])
        xim.place(x = 100, y = 155, width = 250, height = 30)
        xim.bind('<FocusIn>', lambda x: give_focus('xim'))


        Label(ffff, text = '范  围：', font = ('微软雅黑', 16, 'bold'), bg = '#333333', fg = 'white').place(x = 20, y = 200, width = 80, height = 60)
        
        if len(pages_list) == 0:
            pages_list.append(' ')

        pag = tkinter.ttk.Combobox(ffff, background = '#37373D', value = pages_list, font = ('微软雅黑', 15))
        pag.configure(background = '#37373D')
        # pag.set(pages_list[0])
        pag.place(x = 100, y = 215, width = 250, height = 30)
        pag.bind('<FocusIn>', lambda x: give_focus('pag'))


        Label(ffff, text = '检  查：', font = ('微软雅黑', 16, 'bold'), bg = '#333333', fg = 'white').place(x = 20, y = 260, width = 80, height = 60)
        
        if len(give_in_time) == 0:
            give_in_time.append(' ')

        git = tkinter.ttk.Combobox(ffff, background = '#37373D', value = give_in_time, font = ('微软雅黑', 15))
        git.set(give_in_time[2])
        git.place(x = 100, y = 275, width = 250, height = 30)
        git.bind('<FocusIn>', lambda x: give_focus('git'))

        def ok():
            global WorkList, COUNT

            COUNT += 1           

            XIM = xim.get().replace('\n', '')
            PAG = pag.get().replace('\n', '')
            GIT = git.get().replace('\n', '')

            if XIM == '': XIM = BLANK
            if PAG == '': PAG = BLANK
            if GIT == '': GIT = BLANK


            WorkList.append([COUNT, self.sub_id, XIM, PAG, GIT])

            ReLoad()
            OFFF()
            reporter.show('good', '添加成功！')

        def xjp():
            open_osk()
            if self.focus_object == 'xim':
                xim.focus_set()
            elif self.focus_object == 'pag':
                pag.focus_set()
            elif self.focus_object == 'git':
                git.focus_set()

        def savefile():
            xiang_mu_list_file = open(PathTab[self.sub_id] + '\\list.dyx', 'a', encoding = 'UTF-8')
            pages_file = open(PathTab[self.sub_id] + '\\pages.dyx', 'a', encoding = 'UTF-8')
            give_in_time_file = open(PathTab[self.sub_id] + '\\givtime.dyx', 'a', encoding = 'UTF-8')

            if xim.get().strip() != '' and xim.get() not in xiang_mu_list:
                xiang_mu_list_file.write('\n' + str(xim.get()))

            if pag.get().strip() != '' and pag.get() not in pages_list:
                pages_file.write('\n' + str(pag.get()))

            if git.get().strip() != '' and git.get() not in give_in_time:
                give_in_time_file.write('\n' + str(git.get()))

            xiang_mu_list_file.close()
            pages_file.close()
            give_in_time_file.close()

            reporter.show('good', '保存成功！')

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

    def build_up(self, *way):

        if way == ():
            global FrameList

            self.big_frame = Frame(root, bg = '#252526')
            self.big_frame.place(x = self.x, y = self.y, height = self.height, width = self.width)

            self.name_to_put_on = list(self.sub_name)
            self.name_to_put_on = self.name_to_put_on[0] + '   ' + self.name_to_put_on[1]

            self.sub_label = Label(self.big_frame, text = self.name_to_put_on, font = ('微软雅黑', 27), bg = '#2D3313', fg = 'white') # #007ACC #0C2C05
            self.sub_label.place(x = 0, y = 0, width = self.width - 160, height = 40)

            self.add_button = Button(self.big_frame, text = '+', relief = 'flat', borderwidth = 0, font = ('楷体', 32, 'bold'), command = self.add, bg = '#005C99', fg = 'white', activeforeground = 'white', activebackground = '#2E92D5')
            self.add_button.place(x = self.width - 160, y = 0, width = 80, height = 40)

            self.del_button = Button(self.big_frame, text = '×', relief = 'flat', borderwidth = 0, font = ('楷体', 21, 'bold'), command = self.clear, bg = '#37373D', fg = 'red', activeforeground = 'red', activebackground = 'black')
            self.del_button.place(x = self.width - 80, y = 0, width = 80, height = 40)

            self.work_place = Frame(self.big_frame, bg = '#252526')
            self.work_place.place(x = 0, y = 40, width = self.width, height = self.height - 40)

            FrameList.append(self.work_place)

        elif way == ('no', ):

            self.big_frame = Frame(root, bg = '#252526')

            self.name_to_put_on = list(self.sub_name)
            self.name_to_put_on = self.name_to_put_on[0] + '   ' + self.name_to_put_on[1]

            self.sub_label = Label(self.big_frame, text = self.name_to_put_on, font = ('微软雅黑', 27), bg = '#2D3313', fg = 'white') # #007ACC #0C2C05

            self.add_button = Button(self.big_frame, text = '+', relief = 'flat', borderwidth = 0, font = ('楷体', 32, 'bold'), command = self.add, bg = '#005C99', fg = 'white', activeforeground = 'white', activebackground = '#2E92D5')
            self.del_button = Button(self.big_frame, text = '×', relief = 'flat', borderwidth = 0, font = ('楷体', 21, 'bold'), command = self.clear, bg = '#37373D', fg = 'red', activeforeground = 'red', activebackground = 'black')
            self.work_place = Frame(self.big_frame, bg = '#252526')

            FrameList.append(self.work_place)

        else:
            self.big_frame.place(x = self.x, y = self.y, height = self.height, width = self.width)
            self.sub_label.place(x = 0, y = 0, width = self.width - 160, height = 40)
            self.add_button.place(x = self.width - 160, y = 0, width = 80, height = 40)
            self.del_button.place(x = self.width - 80, y = 0, width = 80, height = 40)
            self.work_place.place(x = 0, y = 40, width = self.width, height = self.height - 40)

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

        xiang_mu_list_file = open(PathTab[self.sub_id] + '\\list.dyx', 'r', encoding = 'UTF-8')
        pages_file = open(PathTab[self.sub_id] + '\\pages.dyx', 'r', encoding = 'UTF-8')
        give_in_time_file = open(PathTab[self.sub_id] + '\\givtime.dyx', 'r', encoding = 'UTF-8')

        pages_list = pages_file.readlines()
        give_in_time = give_in_time_file.readlines()
        xiang_mu_list = xiang_mu_list_file.readlines()

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

        def give_focus(a):
            self.focus_object = a

        ffff = Frame(chose_win, bg = '#333333')

        Label(ffff, text = '编 辑 作 业 项', font = ('微软雅黑', 20, 'bold'), bg = '#333333', fg = 'white').place(x = 0, y = 0, width = 400, height = 80)

        Label(ffff, text = '科  目：', font = ('微软雅黑', 16, 'bold'), bg = '#333333', fg = 'white').place(x = 20, y = 80, width = 80, height = 60)
        Label(ffff, text = SubTabID[self.sub_id], font = ('微软雅黑', 16), bg = '#333333', fg = 'white', anchor = 'w').place(x = 100, y = 80, width = 80, height = 60)


        Label(ffff, text = '项  目：', font = ('微软雅黑', 16, 'bold'), bg = '#333333', fg = 'white').place(x = 20, y = 140, width = 80, height = 60)

        xim = tkinter.ttk.Combobox(ffff, background = '#37373D', value = xiang_mu_list, font = ('微软雅黑', 15))
        xim.set(self.name)
        xim.place(x = 100, y = 155, width = 250, height = 30)
        xim.bind('<FocusIn>', lambda x: give_focus('xim'))


        Label(ffff, text = '范  围：', font = ('微软雅黑', 16, 'bold'), bg = '#333333', fg = 'white').place(x = 20, y = 200, width = 80, height = 60)

        pag = tkinter.ttk.Combobox(ffff, background = '#37373D', value = pages_list, font = ('微软雅黑', 15))
        pag.set(self.page)
        pag.place(x = 100, y = 215, width = 250, height = 30)
        pag.bind('<FocusIn>', lambda x: give_focus('pag'))


        Label(ffff, text = '检  查：', font = ('微软雅黑', 16, 'bold'), bg = '#333333', fg = 'white').place(x = 20, y = 260, width = 80, height = 60)

        git = tkinter.ttk.Combobox(ffff, background = '#37373D', value = give_in_time, font = ('微软雅黑', 15))
        git.set(self.time)
        git.place(x = 100, y = 275, width = 250, height = 30)
        git.bind('<FocusIn>', lambda x: give_focus('git'))

        def ok():
            global WorkList, COUNT

            COUNT += 1

            XIM = xim.get().replace('\n', '')
            PAG = pag.get().replace('\n', '')
            GIT = git.get().replace('\n', '')

            if XIM == '': XIM = BLANK
            if PAG == '': PAG = BLANK
            if GIT == '': GIT = BLANK


            for i in range(1, len(WorkList)):
                if WorkList[i][0] == self.count:
                    WorkList[i][2] = XIM
                    WorkList[i][3] = PAG
                    WorkList[i][4] = GIT
                    break

            ReLoad()
            OFFF()
            reporter.show('good', '修改成功！')

        def xjp():
            open_osk()
            if self.focus_object == 'xim':
                xim.focus_set()
            elif self.focus_object == 'pag':
                pag.focus_set()
            elif self.focus_object == 'git':
                git.focus_set()

        def savefile():
            xiang_mu_list_file = open(PathTab[self.sub_id] + '\\list.dyx', 'a', encoding = 'UTF-8')
            pages_file = open(PathTab[self.sub_id] + '\\pages.dyx', 'a', encoding = 'UTF-8')
            give_in_time_file = open(PathTab[self.sub_id] + '\\givtime.dyx', 'a', encoding = 'UTF-8')

            if xim.get().replace('\n', '') != '' and xim.get().replace('\n', '') not in xiang_mu_list:
                xiang_mu_list_file.write('\n' + str(xim.get().replace('\n', '')))

            if pag.get().replace('\n', '') != '' and pag.get().replace('\n', '') not in pages_list:
                pages_file.write('\n' + str(pag.get().replace('\n', '')))

            if git.get().replace('\n', '') != '' and git.get().replace('\n', '') not in give_in_time:
                give_in_time_file.write('\n' + str(git.get().replace('\n', '')))

            xiang_mu_list_file.close()
            pages_file.close()
            give_in_time_file.close()

            reporter.show('good', '保存成功！')

        savebut = Button(ffff, text = '将项目、范围、检查保存至列表', font = ('微软雅黑', 13), relief = 'flat', borderwidth = 0, fg = 'white', bg = '#252526', activebackground = '#252526', activeforeground = 'white',  command = savefile)
        savebut.place(x = 20, y = 400, width = 280, height = 30)

        surebut = Button(ffff, text = '确定', font = ('微软雅黑', 13), relief = 'flat', borderwidth = 0, fg = 'white', bg = '#007ACC', activeforeground = 'white', activebackground = '#2E92D5', command = ok)
        surebut.place(x = 180, y = 450, width = 90, height = 30)

        unsurebut = Button(ffff, text = '取消', font = ('微软雅黑', 13), relief = 'flat', borderwidth = 0, fg = 'white', bg = '#007ACC', activeforeground = 'white', activebackground = '#2E92D5', command = OFFF)
        unsurebut.place(x = 290, y = 450, width = 90, height = 30)

        sjpbut = Button(ffff, text = '小键盘', font = ('微软雅黑', 13), relief = 'flat', borderwidth = 0, fg = 'white', bg = '#252526', activebackground = '#252526', activeforeground = 'white', command = xjp)
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

        BG = self._get_color()

        if BG == '#4E4F51':
            self.delete_image = PhotoImage(file = PATH + '\\icons\\delete-q.gif')
            self.edit_image = PhotoImage(file = PATH + '\\icons\\edit-q.gif')

        elif BG == '#3E3F41':
            self.delete_image = PhotoImage(file = PATH + '\\icons\\delete-s.gif')
            self.edit_image = PhotoImage(file = PATH + '\\icons\\edit-s.gif')

        self.l1 = Label(WorkFrameList[-1], text = self.name, bg = BG, fg = 'white', font = ('微软雅黑', 25), anchor = 'w', justify = 'left').pack(side = TOP, fill = X)
        self.b_del = Button(WorkFrameList[-1], image = self.delete_image, bg = '#4E1A0F', fg = '#C54026', activebackground = BG, relief = 'groove', font = ('微软雅黑', 13), borderwidth = 0, command = self.del_item).pack(side = RIGHT)
        self.b_edit = Button(WorkFrameList[-1], image = self.edit_image, bg = '#212E3A', fg = '#597C9D', activebackground = BG, relief = 'groove', font = ('微软雅黑', 13), borderwidth = 0, command = self.edit_item).pack(side = RIGHT)
        self.l2 = Label(WorkFrameList[-1], text = self.page, bg = BG, fg = '#A5CDAA', font = ('微软雅黑', 19), anchor = 'w', justify = 'left').pack(side = LEFT)
        self.l3 = Label(WorkFrameList[-1], text = self.time, bg = BG, fg = '#9CCDC4', font = ('微软雅黑', 19), anchor = 'w', justify = 'left').pack(side = RIGHT)

        WorkFrameList[-1].pack(side = TOP, fill = X)

class BackEditFrame:

    def __init__(self, father1, father2, father3, sub_name, sub_id, x, y, width, height):
        self.father1 = father1
        self.father2 = father2
        self.father3 = father3
        self.sub_name = sub_name
        self.sub_id = sub_id
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def config(self):

        global PathTab

        # -------------------------------------------------------

        self.middle_frame1 = Frame(self.father1)
        self.middle_frame1.place(x = self.x, y = self.y, width = self.width, height = self.height)

        title1 = Label(self.middle_frame1, text = self.sub_name, bg = '#3C3C3C', fg = 'white', font = ('微软雅黑', 18))
        title1.place(x = 0, y = 0, width = self.width, height = 40)

        self.fra1 = Text(self.middle_frame1, bg = '#252526', fg = 'white', font = ('微软雅黑', 16), borderwidth = 0)
        self.fra1.place(x = 0, y = 40, width = self.width, height = self.height - 40)

        fil = open(PathTab[self.sub_id] + '\\list.dyx', 'r', encoding = 'UTF-8')
        lis = fil.readlines()
        fil.close()

        for each in lis:
            self.fra1.insert(INSERT, each.strip() + '\n')

        # -------------------------------------------------------

        self.middle_frame2 = Frame(self.father2)
        self.middle_frame2.place(x = self.x, y = self.y, width = self.width, height = self.height)

        title2 = Label(self.middle_frame2, text = self.sub_name, bg = '#3C3C3C', fg = 'white', font = ('微软雅黑', 18))
        title2.place(x = 0, y = 0, width = self.width, height = 40)

        self.fra2 = Text(self.middle_frame2, bg = '#252526', fg = 'white', font = ('微软雅黑', 16), borderwidth = 0)
        self.fra2.place(x = 0, y = 40, width = self.width, height = self.height - 40)

        fil = open(PathTab[self.sub_id] + '\\pages.dyx', 'r', encoding = 'UTF-8')
        lis = fil.readlines()
        fil.close()

        for each in lis:
            self.fra2.insert(INSERT, each.strip() + '\n')

        # -------------------------------------------------------

        self.middle_frame3 = Frame(self.father3)
        self.middle_frame3.place(x = self.x, y = self.y, width = self.width, height = self.height)

        title3 = Label(self.middle_frame3, text = self.sub_name, bg = '#3C3C3C', fg = 'white', font = ('微软雅黑', 18))
        title3.place(x = 0, y = 0, width = self.width, height = 40)

        self.fra3 = Text(self.middle_frame3, bg = '#252526', fg = 'white', font = ('微软雅黑', 16), borderwidth = 0)
        self.fra3.place(x = 0, y = 40, width = self.width, height = self.height - 40)

        fil = open(PathTab[self.sub_id] + '\\givtime.dyx', 'r', encoding = 'UTF-8')
        lis = fil.readlines()
        fil.close()

        for each in lis:
            self.fra3.insert(INSERT, each.strip() + '\n')

    def ok(self):
        mmm = self.fra1.get(1.0, END).split()

        global PathTab
        fil = open(PathTab[self.sub_id] + '\\list.dyx', 'w', encoding = 'UTF-8')
        for i in range(len(mmm)):
            fil.write(mmm[i] + '\n')
        fil.close()

        mmm = self.fra2.get(1.0, END).split()

        fil = open(PathTab[self.sub_id] + '\\pages.dyx', 'w', encoding = 'UTF-8')
        for i in range(len(mmm)):
            fil.write(mmm[i] + '\n')
        fil.close()

        mmm = self.fra3.get(1.0, END).split()

        fil = open(PathTab[self.sub_id] + '\\givtime.dyx', 'w', encoding = 'UTF-8')
        for i in range(len(mmm)):
            fil.write(mmm[i] + '\n')
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

        SETTINGS['SUBSTATE'] = ''.join(SETTINGS['SUBSTATE'])

        with open(PATH + '\\conf.json', 'w', encoding = 'UTF-8') as conf_file:
            json.dump(SETTINGS, conf_file)
        
        SETTINGS['SUBSTATE'] = list(SETTINGS['SUBSTATE'])

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

        reporter.show('good', '修改成功！')

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

class SubButton:

    def __init__(self, sub_id, master, x, y):
        self.sub_id = sub_id
        self.master = master
        self.x = x
        self.y = y

    def swap(self):
        global SETTINGS

        if SETTINGS['SUBSTATE'][self.sub_id - 1] == '1':
            SETTINGS['SUBSTATE'][self.sub_id - 1] = '0'
            self.pug.config(bg = '#FF2B33', fg = '#990033', activeforeground = '#FF2B33', activebackground = '#990033')

        else:
            SETTINGS['SUBSTATE'][self.sub_id - 1] = '1'
            self.pug.config(bg = 'lime', fg = 'green', activeforeground = 'lime', activebackground = 'green')

    def config(self):
        global SubTabID, SETTINGS

        self.pug = Button(self.master, text = SubTabID[self.sub_id], borderwidth = 0, relief = GROOVE, font = ('微软雅黑', 20), command = self.swap)
        self.pug.place(x = self.x, y = self.y, width = 170, height = 56)

        self.swap()
        self.swap()



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

    Button(sets_win, text = '返  回', font = ('微软雅黑', 17), relief = GROOVE, command = off, borderwidth = 0, fg = 'white', bg = '#252526', activebackground = '#252526', activeforeground = 'white').place(x = 1730, y = 1000, height = 60, width = 180)

    sets_win.mainloop()

SSS_OF_NOW = 1

def BackEdit():

    global BackList

    BackList = ['List of BackEditFrame']

    TTT = ['后 台 管 理：项 目', '后 台 管 理：范 围', '后 台 管 理：检 查']


    edit_win = Tk()
    edit_win.wm_attributes('-topmost', 1)
    edit_win.wm_attributes('-fullscreen', 1)
    edit_win.config(bg = '#1E1E1E')

    frr1 = Frame(edit_win, bg = '#1E1E1E')
    frr2 = Frame(edit_win, bg = '#1E1E1E')
    frr3 = Frame(edit_win, bg = '#1E1E1E')

    text_down = Label(edit_win, bg = '#1E1E1E', fg = 'lime', font = ('微软雅黑', 23))
    text_down.place(x = 1550, y = 800, height = 60, width = 340)

    l11 = Label(edit_win, bg = 'green', fg = 'white', font = ('consolas', 23))
    l11.place(x = 1610, y = 900, width = 220, height = 60)

    b11 = Button(edit_win, text = '<', font = ('consolas', 23), fg = 'white', bg = '#007ACC', borderwidth = 0, activeforeground = 'white', activebackground = '#2E92D5', command = lambda : goto(SSS_OF_NOW-1))
    b22 = Button(edit_win, text = '>', font = ('consolas', 23), fg = 'white', bg = '#007ACC', borderwidth = 0, activeforeground = 'white', activebackground = '#2E92D5', command = lambda : goto(SSS_OF_NOW+1))

    b11.place(x = 1550, y = 900, width = 60, height = 60)
    b22.place(x = 1830, y = 900, width = 60, height = 60)

    for i in range(1, 11):
        BackList.append(BackEditFrame(frr1, frr2, frr3, SubTabID[i], i, 20 + ((i-1)%5)*300, 20 + 480 * (i//6), 300, 480))
        BackList[-1].config()

    def sure():
        for i in range(1, len(BackList)):
            BackList[i].ok()
        cancel()

        reporter.show('good', '编辑成功！')

    def cancel(*args):
        edit_win.destroy()

    def goto(x):

        global SSS_OF_NOW

        if x == 0:
            SSS_OF_NOW = 1
        elif x == 4:
            SSS_OF_NOW = 3
        else:
            SSS_OF_NOW = x

        text_down.config(text = TTT[SSS_OF_NOW-1])
        l11.config(text = f'{SSS_OF_NOW} / 3')

        if SSS_OF_NOW == 1:
            frr1.place(x = 0, y = 0, width = 1920, height = 1000, anchor = NW)
            frr2.place_forget()
            frr3.place_forget()
        elif SSS_OF_NOW == 2:
            frr2.place(x = 0, y = 0, width = 1920, height = 1000, anchor = NW)
            frr1.place_forget()
            frr3.place_forget()
        elif SSS_OF_NOW == 3:
            frr3.place(x = 0, y = 0, width = 1920, height = 1000, anchor = NW)
            frr1.place_forget()
            frr2.place_forget()

    goto(1)

    Button(edit_win, text = '保存修改', font = ('微软雅黑', 17), relief = GROOVE, command = sure, borderwidth = 0, fg = 'white', bg = '#252526', activebackground = '#3C3C3C', activeforeground = 'white').place(x = 1730, y = 1000, height = 60, width = 180)
    Button(edit_win, text = '取  消', font = ('微软雅黑', 17), relief = GROOVE, command = cancel, borderwidth = 0, fg = 'white', bg = '#252526', activebackground = '#3C3C3C', activeforeground = 'white').place(x = 1530, y = 1000, height = 60, width = 180)

    osk = Button(edit_win, text = '小 键 盘', font = ('微软雅黑', 17), relief = GROOVE, command = open_osk, borderwidth = 0, fg = 'white', bg = '#252526', activebackground = '#3C3C3C', activeforeground = 'white')
    osk.place(x = 20, y = 1000, height = 60, width = 180)
    #edit_win.bind('<x>', cancel)
    edit_win.mainloop()

def PreLoad():
    global WorkList, COUNT, FrameList, SubFrameList, SETTINGS, POSITIONS

    fil = open(PATH + '\\history\\today.dyx', 'r', encoding = 'UTF-8')
    WorkList = WorkList + fil.readlines()
    fil.close()

    for i in range(1, len(WorkList)):

        WorkList[i] = WorkList[i].strip().split(BINDER)

        WorkList[i][0] = int(WorkList[i][0])
        WorkList[i][1] = int(WorkList[i][1])

    for i in range(1, len(WorkList)):
        WorkList[i][0] = i

    COUNT = len(WorkList) - 1

    wid_set = SETTINGS['SUBSTATE']
    cnt = str(wid_set.count('1'))

    j = 0

    for i in range(1, 11):
        if wid_set[i-1] == '1':
            SubFrameList[i].reloadPos(POSITIONS[cnt][j])
            j += 1
        else:
            SubFrameList[i].hide()

    ReLoad()

def ReLoad():
    global WorkFrameList, WorkList

    while len(WorkFrameList) != 1:
        WorkFrameList[1].destroy()
        del WorkFrameList[1]

    for i in range(1, len(WorkList)):
        SUB_ID = WorkList[i][1]
        NAME = WorkList[i][2]
        PAGE = WorkList[i][3]
        TIME = WorkList[i][4]
        if SUB_ID == BLANK: SUB_ID = ''
        if NAME == BLANK: NAME = ''
        if PAGE == BLANK: PAGE = ''
        if TIME == BLANK: TIME = ''
        new = WorkFrame(count = WorkList[i][0], sub_id = SUB_ID, name = NAME, page = PAGE, time = TIME)
        new.config()

    global SETTINGS

    if SETTINGS['AUTOSAVE']:
        save()

def save():
    global WorkList, SETTINGS

    res = []
    for i in range(1, len(WorkList)):
        WorkList[i][0] = str(WorkList[i][0])
        WorkList[i][1] = str(WorkList[i][1])
        res.append(BINDER.join(WorkList[i]))

    fil = open(PATH + '\\history\\today.dyx', 'w', encoding = 'UTF-8')
    fil.write('\n'.join(res))
    fil.close()

    for i in range(1, len(WorkList)):
        WorkList[i][0] = int(WorkList[i][0])
        WorkList[i][1] = int(WorkList[i][1])

    SETTINGS['SUBSTATE'] = ''.join(SETTINGS['SUBSTATE'])

    with open(PATH + '\\conf.json', 'w', encoding = 'UTF-8') as conf_file:
        json.dump(SETTINGS, conf_file)

    SETTINGS['SUBSTATE'] = list(SETTINGS['SUBSTATE'])

def DelTaskAll():

    if not askyesno('警告', '请确认操作：删除全部作业项\n此为不可逆操作，删除后无法复原\n是否继续？'):
        return

    global WorkList
    WorkList = ['List of homework']
    ReLoad()

    reporter.show('good', '删除成功！')

def OFF(*args):
    save()
    root.destroy()
    sys.exit()

def helper():
    global VERSION

    help_win = Tk()
    help_win.title('使用说明书')
    help_win.attributes('-fullscreen', True)
    help_win.wm_attributes('-topmost', True)
    help_win.config(bg = '#1e1e1e')

    Label(help_win, text = f'班级作业助手 {VERSION} 使用说明书', bg = '#1e1e1e', fg = 'white', anchor = W, font = ('微软雅黑', 50)).place(x = 80, y = 20, width = 1760, height = 100)

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


    if str(datetime.datetime.now())[0:4] == '2024' or str(datetime.datetime.now())[0:4] == '2025' and int(str(datetime.datetime.now())[5:7]) <= 6:
        tgt = '612'
    else:
        tgt = '202512届'

    but0 = Button(help_win, text = '写在前面', fg = 'white', bg = '#212E3A', font = ('微软雅黑', 20), activebackground = '#3F9CD6', activeforeground = 'white', relief = GROOVE, borderwidth = 0, command = lambda : reLoadLabel('写在前面', '制作本程序的初衷，是在不使用黑板的基础上，使屏幕白板上的作业有序、整齐。一般不用黑板的嘛，不然擦黑板的同学还得擦；若是能用黑板写，我强烈建议用黑板，因为黑板没那么坏眼睛。\n\n本软件参考微软深色配色，这样在晚上看着就不会太刺眼。\n\n一开始做这个软件的时候 是没料到会持续维护这么长的时间的。\n\n我很有幸，有202214 级的同学共同见证了此软件的发展史。你们给予了我这个实践的机会，非常感谢你们给予我的理解和支持，和在软件出现问题时的包容，以及为促使软件向前发展而提出的宝贵建议。\n\n本软件还将继续维护下去，并愿意免费提供给大家一起使用。再次感谢大家的使用。'))
    but1 = Button(help_win, text = '新建作业项', fg = 'white', bg = '#212E3A', font = ('微软雅黑', 20), activebackground = '#3F9CD6', activeforeground = 'white', relief = GROOVE, borderwidth = 0, command = lambda : reLoadLabel('新建作业项', '点击每个学科框上部的“+”按钮即可添加作业。单击“小键盘”可调用出屏幕小键盘。\n\n作业项可以从预设列表中选择，也可以自由编辑，只是不能含有换行。此外，过长的作业名称可能会显示不全。\n\n“范围”选项，可以是页码等内容。\n\n“检查”指的是上交时间。\n\n“将项目、范围、检查保存至列表”按钮可以将自定义的内容添加至列表内，重复的内容自动跳过。你可以去后台编辑处进行整理。\n\n本程序对于每个输入框中的内容仅做换行检查，不检查违禁词或者内容的逻辑性。这意味着你们可以整活，但最好不要。\n\n此外，程序不会自动修改内容，比如“明天交”到第二天不会自动改为“今天交”。'))
    but2 = Button(help_win, text = '编辑作业项', fg = 'white', bg = '#212E3A', font = ('微软雅黑', 20), activebackground = '#3F9CD6', activeforeground = 'white', relief = GROOVE, borderwidth = 0, command = lambda : reLoadLabel('编辑作业项', '点击每条作业项中的“编辑”即可修改作业项。用法与新增作业项基本相同，此处不再叙述。'))
    but3 = Button(help_win, text = '删除作业项', fg = 'white', bg = '#212E3A', font = ('微软雅黑', 20), activebackground = '#3F9CD6', activeforeground = 'white', relief = GROOVE, borderwidth = 0, command = lambda : reLoadLabel('删除作业项', '一共有三种方法可以删除作业项：单项删除、整科删除、全部删除。请注意，这三种删除方式都是不可逆的，操作后无法还原。\n\n单项删除：点击作业项上的“删除”按钮。\n\n整科删除：单击作业框上的“×”按钮进行删除。\n\n全部删除：软件右下角有“删除全部作业项”按钮。该命令在执行前会弹窗询问，以防止误触（其他二者不会弹窗询问）。'))
    but4 = Button(help_win, text = '学科管理', fg = 'white', bg = '#212E3A', font = ('微软雅黑', 20), activebackground = '#3F9CD6', activeforeground = 'white', relief = GROOVE, borderwidth = 0, command = lambda : reLoadLabel('学科管理', '主界面>>学科管理 可以编辑主界面显示的科目框。绿色为启用，红色为隐藏，单击来切换。\n被隐藏的科目若有已添加的作业项，也不会被清除。\n布局会自动保存，并在下一次软件启动时自动应用。'))
    but5 = Button(help_win, text = '后台管理', fg = 'white', bg = '#212E3A', font = ('微软雅黑', 20), activebackground = '#3F9CD6', activeforeground = 'white', relief = GROOVE, borderwidth = 0, command = lambda : reLoadLabel('后台管理', '主界面>>后台管理 可以编辑每一门学科的作业列表，以及预设的范围列表和上交时间列表。'))
    but6 = Button(help_win, text = '设置', fg = 'white', bg = '#212E3A', font = ('微软雅黑', 20), activebackground = '#3F9CD6', activeforeground = 'white', relief = GROOVE, borderwidth = 0, command = lambda : reLoadLabel('设置', '在主界面>>设置图标 中可以修改一些设置。通过点击按钮来修改设置。修改的设置会自动立刻保存，但部分设置要在软件下一次启动时生效。\n\n自动保存：\n自动记录添加的作业，以免意外或非法退出造成的数据丢失。\n\n自动关机：\n开启后，电脑将在21:40:30时启动关机300秒倒计时，300秒后自动关机。\n\n设置功能仍在完善中'))
    but7 = Button(help_win, text = '关于', fg = 'white', bg = '#212E3A', font = ('微软雅黑', 20), activebackground = '#3F9CD6', activeforeground = 'white', relief = GROOVE, borderwidth = 0, command = lambda : reLoadLabel(f'班级作业助手 {VERSION}', f'开发者：杭州第二中学钱江学校 {tgt} 丁誉轩\n\nQQ: 431495254\n\nBilibili: 卢丁喆丰群\n所有更新消息将在这个账号第一时间发布，敬请关注，欢迎投币）\n\nCSDN: do_while_false\n\n软件官方QQ群：704376858\n你可以在这个群内下载最新版本的软件、反馈问题，也可以与作者交流\n\n源代码不公开。'))
    but8 = Button(help_win, text = '其他功能', fg = 'white', bg = '#212E3A', font = ('微软雅黑', 20), activebackground = '#3F9CD6', activeforeground = 'white', relief = GROOVE, borderwidth = 0, command = lambda : reLoadLabel('其他功能', '主界面的时间就是学校时间，误差不超过10秒，供参考'))
    but9 = Button(help_win, text = '更新日志', fg = 'white', bg = '#212E3A', font = ('微软雅黑', 20), activebackground = '#3F9CD6', activeforeground = 'white', relief = GROOVE, borderwidth = 0, command = lambda : reLoadLabel('更新日志', NEWS))

    but0.place(x = 120, y = 240, height = 60, width = 200)
    but1.place(x = 120, y = 300, height = 60, width = 200)
    but2.place(x = 120, y = 360, height = 60, width = 200)
    but3.place(x = 120, y = 420, height = 60, width = 200)
    but4.place(x = 120, y = 480, height = 60, width = 200)
    but5.place(x = 120, y = 540, height = 60, width = 200)
    but6.place(x = 120, y = 600, height = 60, width = 200)
    but7.place(x = 120, y = 660, height = 60, width = 200)
    but8.place(x = 120, y = 720, height = 60, width = 200)
    but9.place(x = 120, y = 780, height = 60, width = 200)

    def back(*args):
        help_win.destroy()

    def surf():
        webbrowser.open('https://space.bilibili.com/1004176582')
        back()

    Button(help_win, text = '去作者 Bilibili 看看视频说明', font = ('微软雅黑', 17), relief = GROOVE, command = surf, borderwidth = 0, fg = 'white', bg = '#252526', activebackground = '#3C3C3C', activeforeground = 'white').place(x = 20, y = 1000, height = 60, width = 400)


    Button(help_win, text = '好 的', font = ('微软雅黑', 17), relief = GROOVE, command = back, borderwidth = 0, fg = 'white', bg = '#252526', activebackground = '#3C3C3C', activeforeground = 'white').place(x = 1730, y = 1000, height = 60, width = 180)

    reLoadLabel('写在前面', '制作本程序的初衷，是在不使用黑板的基础上，使屏幕白板上的作业有序、整齐。一般不用黑板的嘛，不然擦黑板的同学还得擦；若是能用黑板写，我强烈建议用黑板，因为黑板没那么坏眼睛。\n\n本软件参考微软深色配色，这样在晚上看着就不会太刺眼。\n\n一开始做这个软件的时候 是没料到会持续维护这么长的时间的。\n\n我很有幸，有202214 级的同学共同见证了此软件的发展史。你们给予了我这个实践的机会，非常感谢你们给予我的理解和支持，和在软件出现问题时的包容，以及为促使软件向前发展而提出的宝贵建议。\n\n本软件还将继续维护下去，并愿意免费提供给大家一起使用。再次感谢大家的使用。')

    help_win.bind('<x>', back)
    help_win.mainloop()

def check_screen(e):
    if root.winfo_screenwidth() != 1920 or root.winfo_screenheight() != 1080:
        
        showerror('警告', f'当前分辨率为{root.winfo_screenwidth()}x{root.winfo_screenheight()}，程序拒绝运行，因为程序只能在1920x1080分辨率下运行。其他分辨率下运行软件会导致界面显示不全。')
        OFF()

def shuaxin():

    global SETTINGS

    while True:
        timenow = str(datetime.datetime.now())
        toh = int(timenow[11:13])
        tom = int(timenow[14:16])
        tos = int(timenow[17:19])
        tts = 60 - tos

        if toh >= 21 and tom >= 40 and tos >= 30:
            if SETTINGS['AUTOOFF']:
                os.system('shutdown -s -t 300 -c 班级作业助手-自动关机：电脑将在300秒后关机')

        main_time_text.config(text = timenow[0:19])

        # We need to check whether the screen size is always at 1920x1080. 
        # Version 3.4.0 added this function. However, after adding this function, the original time function can't work normally in the executable file. 
        # We use python 3.8.6, command "pyinstaller -F -w -i Threat.contrast-black.ico main3.4.0.py"

        # From version 3.4.1, a new method is used.
        '''
        sX = win32api.GetSystemMetrics(0)
        sY = win32api.GetSystemMetrics(1)

        if sX != 1920 or sY != 1080:

            prrrr = psutil.Process()
            process_name = prrrr.name()

            showerror('警告', f'当前分辨率为{sX}x{sY}，程序拒绝运行，因为程序只能在1920x1080分辨率下运行。其他分辨率下运行软件会导致界面显示不全。')
            os.system(f'taskkill -im \"{process_name}\" -f')
        '''
        time.sleep(1)


def reloadFrame():

    global MAIN_EDIT_WIN_OPENED

    subbut = []

    if MAIN_EDIT_WIN_OPENED == 1:
        return

    MAIN_EDIT_WIN_OPENED = 1

    wid_win = Tk()
    wid_win.title('编辑主界面学科')
    wid_win.overrideredirect(1)
    wid_win.geometry('430x530+745+275')
    wid_win.resizable(False, False)
    wid_win.configure(bg = '#37373D')
    wid_win.wm_attributes('-topmost', 1)

    ffff = Frame(wid_win, bg = '#333333')

    Label(ffff, text = '配 置 主 界 面', font = ('微软雅黑', 20, 'bold'), bg = '#333333', fg = 'white').place(x = 0, y = 0, width = 400, height = 80)

    def OFFF(*args):
        global MAIN_EDIT_WIN_OPENED

        MAIN_EDIT_WIN_OPENED = 0
        wid_win.destroy()


    def ok():
        global FrameList, SubFrameList, SETTINGS, POSITIONS

        wid_set = SETTINGS['SUBSTATE']
        cnt = str(wid_set.count('1'))

        j = 0

        for i in range(1, 11):
            if wid_set[i-1] == '1':
                SubFrameList[i].reloadPos(POSITIONS[cnt][j])
                j += 1
            else:
                SubFrameList[i].hide()

        ReLoad()

        OFFF()

        reporter.show('good', '修改成功！')

    subbut.append(SubButton(1, ffff, 20, 100))
    subbut.append(SubButton(2, ffff, 210, 100))
    subbut.append(SubButton(3, ffff, 20, 166))
    subbut.append(SubButton(4, ffff, 210, 166))
    subbut.append(SubButton(5, ffff, 20, 232))
    subbut.append(SubButton(6, ffff, 210, 232))
    subbut.append(SubButton(7, ffff, 20, 298))
    subbut.append(SubButton(8, ffff, 210, 298))
    subbut.append(SubButton(9, ffff, 20, 364))
    subbut.append(SubButton(10, ffff, 210, 364))

    for i in range(len(subbut)):
        subbut[i].config()



    ffff.place(x = 15, y = 15, width = 400, height = 500)

    surebut = Button(ffff, text = '完成', font = ('微软雅黑', 13), relief = 'flat', borderwidth = 0, fg = 'white', bg = '#007ACC', activeforeground = 'white', activebackground = '#2E92D5', command = ok)
    surebut.place(x = 20, y = 440, width = 360, height = 40)

    wid_win.bind('<x>', OFFF)
    wid_win.mainloop()

def config_biaoyu():
    global BIAO_YU_WIN_OPENED
    
    if BIAO_YU_WIN_OPENED == 1:
        return
    BIAO_YU_WIN_OPENED = 1

    biao_win = Toplevel()
    biao_win.title('编辑班级标语')
    biao_win.geometry('500x140+400+800')
    biao_win.resizable(False, False)
    biao_win.config(bg = '#3C3C3C')
    biao_win.wm_attributes('-topmost', 1)
    biao_win.iconbitmap(PATH + '\\icons\\Threat.contrast-black.ico')
    biao_win.transient(root)

    '''
    def _disable_minbox():
        win_id = biao_win.winfo_id()
        hwnd = win32gui.GetParent(win_id) 
        style = win32gui.GetWindowLong(hwnd, win32con.GWL_STYLE)
        style &= ~win32con.WS_MINIMIZEBOX
        win32gui.SetWindowLong(hwnd, win32con.GWL_STYLE, style)
    '''
    
    def biao_off(*args):
        global BIAO_YU_WIN_OPENED
        BIAO_YU_WIN_OPENED = 0
    

    def biao_ok():
        YYYY = biao_get.get().strip()
        if YYYY == '':
            YYYY = '单击以添加班级标语'
        biao_yu_text.config(text = YYYY)
        SETTINGS['Biaoyu'] = YYYY
        biao_win.destroy()

    biao_get = Entry(biao_win, bg = '#6C6C6C', fg = 'white', font = ('微软雅黑', 14), borderwidth = 0)
    biao_get.insert(0, SETTINGS['Biaoyu'])
    biao_get.focus_set()
    biao_get.place(x = 40, y = 20, width = 420, height = 40)

    biao_ok_but = Button(biao_win, text = '确定', font = ('微软雅黑', 13), borderwidth = 0, fg = 'lime', bg = '#49494B', activebackground = '#252526', activeforeground = 'white', command = biao_ok)
    biao_ok_but.place(x = 60, y = 80, width = 180, height = 35)

    biao_off_but = Button(biao_win, text = '取消', font = ('微软雅黑', 13), borderwidth = 0, fg = 'red', bg = '#49494B', activebackground = '#252526', activeforeground = 'white', command = lambda: biao_win.destroy())
    biao_off_but.place(x = 260, y = 80, width = 180, height = 35)

    Button(biao_win, bg = '#353535', fg = 'white', text = '小键盘', font = ('微软雅黑', 5), command = open_osk, activebackground = '#333333', activeforeground = 'white', borderwidth = 0).place(relx = 0.98, rely = 0.96, anchor = 'se', height = 14, width = 30)

    #biao_win.tk.call('focus', biao_win._w)
    biao_win.bind('<Destroy>', biao_off)
    biao_win.mainloop()

def shownews():
    global VERSION

    newswin = Toplevel()
    newswin.overrideredirect(1)
    newswin.title(f'{VERSION} 更新详情')
    newswin.geometry('940x600+490+190')
    newswin.resizable(False, False)
    newswin.wm_attributes('-topmost', 1)
    newswin.config(bg = '#49494B')

    newswid = Frame(newswin, bg = '#333333')
    newswid.place(x = 20, y = 20, height = 560, width = 900)

    this_new = '''3.4.0 -> 3.4.1
    修改了输入作业时的换行符检测策略：不再提示禁止输入换行，而是直接删除换行符
    修改输入时“范围”选项的默认项为空
    优化了小键盘的使用体验，去除了子线程 cmd 窗口
    修复了主界面时间不变的 BUG：是由于局部导入全局引用引起的
    修复了分辨率错误检测的问题，现在可以实时监测屏幕分辨率的变化
    在“添加标语”窗口中添加“小键盘”按钮

*已知问题：
    在执行“将项目、范围、检查保存至列表”命令时，若内容存在空格，可能导致后续选择该项目后提示“存在换行”。目前通过更改对换行的处理策略来避免出现这样的问题，但代码上仍然存在漏洞，后续更新将尝试修复。'''

    def ok_and_never():
        SETTINGS['ShowNew'] = 0
        newswin.destroy()

    Label(newswid, text = f'班级作业助手 {VERSION} 版本更新', bg = '#333333', fg = 'white', font = ('微软雅黑', 40)).place(x = 0, y = 10, width = 900, height = 100)
    Label(newswid, text = this_new, bg = '#2d2d2d', fg = '#DCDCAA', font = ('consolas', 15), justify = 'left', wraplength = 860).place(x = 20, y = 120, width = 860, height = 280)

    Button(newswid, text = ' → 很好，很好，很好', font = ('微软雅黑', 15), anchor = 'w', borderwidth = 0, fg = 'lime', bg = '#49494B', activebackground = '#252526', activeforeground = 'white', command = lambda: newswin.destroy()).place(x = 20, y = 420, width = 860, height = 50)
    Button(newswid, text = ' → 很棒，然后不用再出示了', font = ('微软雅黑', 15), anchor = 'w', borderwidth = 0, fg = 'white', bg = '#49494B', activebackground = '#252526', activeforeground = 'white', command = ok_and_never).place(x = 20, y = 490, width = 860, height = 50)


    newswin.mainloop()

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
    SubFrameList[i].build_up('no')

PreLoad()

Button(root, relief = GROOVE, text = '保存并退出', font = ('微软雅黑', 13), borderwidth = 0, fg = 'white', bg = '#49494B', activebackground = '#252526', activeforeground = 'white', command = OFF).place(x = 20, y = 1030, width = 180, height = 30)
Button(root, relief = GROOVE, text = '最小化', font = ('微软雅黑', 13), borderwidth = 0, fg = 'white', bg = '#333333', activebackground = '#252526', activeforeground = 'white', command = lambda : root.iconify()).place(x = 20, y = 1000, width = 180, height = 30)

Button(root, relief = GROOVE, text = '×', font = ('微软雅黑', 15), borderwidth = 0, fg = 'white', bg = '#49494B', activebackground = '#252526', activeforeground = 'white', command = OFF).place(x = 0, y = 0, width = 20, height = 20)
Button(root, relief = GROOVE, text = '-', font = ('微软雅黑', 15), borderwidth = 0, fg = 'white', bg = '#333333', activebackground = '#252526', activeforeground = 'white', command = lambda : root.iconify()).place(x = 20, y = 0, width = 20, height = 20)

Button(root, relief = GROOVE, text = '×', font = ('微软雅黑', 15), borderwidth = 0, fg = 'white', bg = '#49494B', activebackground = '#252526', activeforeground = 'white', command = OFF).place(x = 1900, y = 0, width = 20, height = 20)
Button(root, relief = GROOVE, text = '-', font = ('微软雅黑', 15), borderwidth = 0, fg = 'white', bg = '#333333', activebackground = '#252526', activeforeground = 'white', command = lambda : root.iconify()).place(x = 1880, y = 0, width = 20, height = 20)


settings_image = PhotoImage(file = PATH + '\\icons\\Settings.gif')
settings_but = Button(root, image = settings_image, text = '设置', font = ('微软雅黑', 17), relief = GROOVE, command = SetEdit, fg = 'white', bg = '#37373D', borderwidth = 0, activebackground = '#252526', activeforeground = 'white')
settings_but.place(x = 1160, y = 1000, width = 60, height = 60)

help_image = PhotoImage(file = PATH + '\\icons\\help.gif')
shuo_ming_but = Button(root, image = help_image, font = ('微软雅黑', 17), relief = FLAT, command = helper, fg = 'white', bg = '#37373D', borderwidth = 0, activebackground = '#252526', activeforeground = 'white')
shuo_ming_but.place(x = 1240, y = 1000, width = 60, height = 60)

main_edit_but = Button(root, text = '学科管理', font = ('微软雅黑', 17), relief = FLAT, command = reloadFrame, borderwidth = 0, fg = 'white', bg = '#37373D', activebackground = '#252526', activeforeground = 'white')
main_edit_but.place(x = 1320, y = 1000, width = 180, height = 60)

power_shell_but = Button(root, text = '后台管理', font = ('微软雅黑', 17), relief = FLAT, command = BackEdit, borderwidth = 0, fg = 'white', bg = '#37373D', activebackground = '#252526', activeforeground = 'white')
power_shell_but.place(x = 1520, y = 1000, width = 180, height = 60)

del_task_button_all = Button(root, text = '删除全部作业项', font = ('微软雅黑', 17), relief = GROOVE, command = DelTaskAll, borderwidth = 0, fg = 'white', bg = '#37373D', activebackground = '#252526', activeforeground = 'white')
del_task_button_all.place(x = 1720, y = 1000, width = 180, height = 60)

#Label(root, text = 'Powered by 414', bg = '#1e1e1e', fg = '#0089E6', font = ('Consolas', 24),anchor = 'w').place(x = 240, y = 990, width = 330, height = 40)

main_time_text = Label(root, bg = '#1e1e1e', fg = 'white', font = ('Consolas', 24), anchor = 'w')
main_time_text.place(x = 240, y = 1035, width = 500, height = 40)
#Label(root, text = '414', bg = '#1E1E1E', fg = '#0089E6', font = ('Courier new', 42)).place(x = 880, y = 1020, width = 160, height = 60)


th = threading.Thread(target = shuaxin, name = 'thread_time')
th.setDaemon(True)
th.start()

edit_image_for_biaoyu = PhotoImage(file = PATH + '\\icons\\edit-d.gif')
biaoyu_get = Button(root, image = edit_image_for_biaoyu, borderwidth = 0, command = config_biaoyu)
biaoyu_get.place(x = 1080, y = 995, width = 40, height = 40)


biao_yu_text = Label(root, text = SETTINGS['Biaoyu'], bg = '#424242', fg = 'white', font = ('微软雅黑', 21), anchor = 'w')
biao_yu_text.place(x = 240, y = 995, width = 840, height = 40)


Label(root, bg = '#1e1e1e', fg = 'grey', text = f'班级作业助手 {VERSION} by 丁誉轩 ©  版权所有，侵权必究', font = ('微软雅黑', 6)).place(x = 1920, y = 1080, anchor = SE, width = 250, height = 15)
    
root.protocol('WM_WINDOW_DELETE', OFF)
root.bind('<x>', OFF)

if SETTINGS['ShowNew'] == 1:
    root.after(1, shownews)

root.bind('<Configure>', check_screen)
root.mainloop()

