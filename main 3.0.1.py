'''
3.0.0 -> 3.0.1
    新增ReportLAB class
    修复“为空”
'''
# -*- coding:UTF-8 -*-
import datetime
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
        sys.exit()

except:
    pass

root = Tk()
root.title('作业助手3.0 by dyx')
root.wm_attributes('-fullscreen', 1)
root.geometry('1920x1080')
root.resizable(False, False)
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
}

SubFrameList = ['Frame for SubjectFrame']
WorkFrameList = ['Frame for WorkFrame']
FrameList = ['Frame for frame in SubjectFrame']
WorkList = ['List of homework']

ADD_WIN_OPENED = 0
REPORT_WIN_OPENED = 0


COUNT = 1
VERSON = '3.0.1'

AUTOSAVE = 1

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

        zu_dang = Tk()
        zu_dang.wm_attributes('-fullscreen', 1)
        zu_dang.attributes('-alpha', 0.3)

        chose_win = Tk()
        chose_win.overrideredirect(1)
        chose_win.configure(bg = '#333333')
        chose_win.title('新建作业项')
        chose_win.geometry('400x500+760+290')
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
            zu_dang.destroy()
            # root.focus_set()


        Label(chose_win, text = '新 建 作 业 项', font = ('微软雅黑', 20, 'bold'), bg = '#333333', fg = 'white').place(x = 0, y = 0, width = 400, height = 80)

        Label(chose_win, text = '科  目：', font = ('微软雅黑', 16, 'bold'), bg = '#333333', fg = 'white').place(x = 20, y = 80, width = 80, height = 60)
        Label(chose_win, text = self.sub_name, font = ('微软雅黑', 16), bg = '#333333', fg = 'white', anchor = 'w').place(x = 100, y = 80, width = 80, height = 60)

        Label(chose_win, text = '项  目：', font = ('微软雅黑', 16, 'bold'), bg = '#333333', fg = 'white').place(x = 20, y = 140, width = 80, height = 60)
        xim = tkinter.ttk.Combobox(chose_win, background = '#37373D', value = xiang_mu_list.split(), font = ('微软雅黑', 15))
        xim.set(xiang_mu_list.split()[0])
        xim.place(x = 100, y = 155, width = 250, height = 30)

        Label(chose_win, text = '范  围：', font = ('微软雅黑', 16, 'bold'), bg = '#333333', fg = 'white').place(x = 20, y = 200, width = 80, height = 60)
        pag = tkinter.ttk.Combobox(chose_win, background = '#37373D', value = pages_list.split(), font = ('微软雅黑', 15))
        pag.set(pages_list.split()[0])
        pag.place(x = 100, y = 215, width = 250, height = 30)

        Label(chose_win, text = '检  查：', font = ('微软雅黑', 16, 'bold'), bg = '#333333', fg = 'white').place(x = 20, y = 260, width = 80, height = 60)
        git = tkinter.ttk.Combobox(chose_win, background = '#37373D', value = give_in_time.split(), font = ('微软雅黑', 15))
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

            if xim.get() == '' or ag.get() == '' or git.get() == '':
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

        surebut = Button(chose_win, text = '确定', font = ('微软雅黑', 13), relief = 'flat', borderwidth = 0, fg = 'white', bg = '#007ACC', activeforeground = 'white', activebackground = '#2E92D5', command = ok)
        surebut.place(x = 180, y = 450, width = 90, height = 30)

        unsurebut = Button(chose_win, text = '取消', font = ('微软雅黑', 13), relief = 'flat', borderwidth = 0, fg = 'white', bg = '#007ACC', activeforeground = 'white', activebackground = '#2E92D5', command = OFFF)
        unsurebut.place(x = 290, y = 450, width = 90, height = 30)

        sjpbut = Button(chose_win, text = '小键盘', font = ('微软雅黑', 13), relief = 'flat', borderwidth = 0, fg = 'white', bg = '#252526', activebackground = '#3C3C3C', activeforeground = 'white', command = xjp)
        sjpbut.place(x = 20, y = 450, width = 90, height = 30)


        ADD_WIN_OPENED = 1
        chose_win.bind('<Control-KeyPress-d>', OFFF)
        zu_dang.mainloop()
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

        sub_label = Label(big_frame, text = name_to_put_on, font = ('微软雅黑', 27), bg = '#3C4419', fg = 'white') # #007ACC #0C2C05
        sub_label.place(x = 0, y = 0, width = self.width - 160, height = 40)

        add_button = Button(big_frame, text = '+', relief = 'flat', borderwidth = 0, font = ('楷体', 32, 'bold'), command = self.add, bg = '#007ACC', fg = 'white', activeforeground = 'white', activebackground = '#2E92D5')
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
        col = ['#404041', '#5F6062']

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

        zu_dang = Tk()
        zu_dang.wm_attributes('-fullscreen', 1)
        zu_dang.attributes('-alpha', 0.3)

        chose_win = Tk()
        chose_win.overrideredirect(1)
        chose_win.configure(bg = '#333333')
        chose_win.title('编辑作业项')
        chose_win.geometry('400x500+760+290')
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
            zu_dang.destroy()
            # root.focus_set()


        Label(chose_win, text = '编 辑 作 业 项', font = ('微软雅黑', 20, 'bold'), bg = '#333333', fg = 'white').place(x = 0, y = 0, width = 400, height = 80)

        Label(chose_win, text = '科  目：', font = ('微软雅黑', 16, 'bold'), bg = '#333333', fg = 'white').place(x = 20, y = 80, width = 80, height = 60)
        Label(chose_win, text = SubTabID[self.sub_id], font = ('微软雅黑', 16), bg = '#333333', fg = 'white', anchor = 'w').place(x = 100, y = 80, width = 80, height = 60)

        Label(chose_win, text = '项  目：', font = ('微软雅黑', 16, 'bold'), bg = '#333333', fg = 'white').place(x = 20, y = 140, width = 80, height = 60)
        xim = tkinter.ttk.Combobox(chose_win, background = '#37373D', value = xiang_mu_list.split(), font = ('微软雅黑', 15))
        xim.set(self.name)
        xim.place(x = 100, y = 155, width = 250, height = 30)

        Label(chose_win, text = '范  围：', font = ('微软雅黑', 16, 'bold'), bg = '#333333', fg = 'white').place(x = 20, y = 200, width = 80, height = 60)
        pag = tkinter.ttk.Combobox(chose_win, background = '#37373D', value = pages_list.split(), font = ('微软雅黑', 15))
        pag.set(self.page)
        pag.place(x = 100, y = 215, width = 250, height = 30)

        Label(chose_win, text = '检  查：', font = ('微软雅黑', 16, 'bold'), bg = '#333333', fg = 'white').place(x = 20, y = 260, width = 80, height = 60)
        git = tkinter.ttk.Combobox(chose_win, background = '#37373D', value = give_in_time.split(), font = ('微软雅黑', 15))
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

            if xim.get() == '' or ag.get() == '' or git.get() == '':
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

        surebut = Button(chose_win, text = '确定', font = ('微软雅黑', 13), relief = 'flat', borderwidth = 0, fg = 'white', bg = '#007ACC', activeforeground = 'white', activebackground = '#2E92D5', command = ok)
        surebut.place(x = 180, y = 450, width = 90, height = 30)

        unsurebut = Button(chose_win, text = '取消', font = ('微软雅黑', 13), relief = 'flat', borderwidth = 0, fg = 'white', bg = '#007ACC', activeforeground = 'white', activebackground = '#2E92D5', command = OFFF)
        unsurebut.place(x = 290, y = 450, width = 90, height = 30)

        sjpbut = Button(chose_win, text = '小键盘', font = ('微软雅黑', 13), relief = 'flat', borderwidth = 0, fg = 'white', bg = '#252526', activebackground = '#3C3C3C', activeforeground = 'white', command = xjp)
        sjpbut.place(x = 20, y = 450, width = 90, height = 30)


        ADD_WIN_OPENED = 1
        chose_win.bind('<Control-KeyPress-d>', OFFF)
        zu_dang.mainloop()
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
        
        self.l1 = Label(WorkFrameList[-1], text = self.name, bg = self._get_color(), fg = 'white', font = ('微软雅黑', 21), anchor = 'w', justify = 'left').pack(side = TOP, fill = X)
        self.b_del = Button(WorkFrameList[-1], text = '删除', bg = '#4E1A0F', fg = '#C54026', relief = 'flat', font = ('微软雅黑', 13), borderwidth = 0, height = 1, command = self.del_item).pack(side = RIGHT)
        self.b_edit = Button(WorkFrameList[-1], text = '编辑', bg = '#B180D7', fg = '#4B206C', relief = 'flat', font = ('微软雅黑', 13), borderwidth = 0, height = 1, command = self.edit_item).pack(side = RIGHT)
        self.l2 = Label(WorkFrameList[-1], text = self.page, bg = self._get_color(), fg = '#A5CDAA', font = ('微软雅黑', 16), anchor = 'w', justify = 'left').pack(side = LEFT)
        self.l3 = Label(WorkFrameList[-1], text = self.time, bg = self._get_color(), fg = '#9CCDC4', font = ('微软雅黑', 16), anchor = 'w', justify = 'left').pack(side = RIGHT)

        WorkFrameList[-1].pack(side = TOP, fill = X)

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

    global AUTOSAVE

    if AUTOSAVE:
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


del_task_button_all = Button(root, text = '删除全部作业项', font = ('微软雅黑', 17), relief = GROOVE, command = DelTaskAll, borderwidth = 0, fg = 'white', bg = '#252526', activebackground = '#3C3C3C', activeforeground = 'white')
del_task_button_all.place(x = 1720, y = 1000, width = 180, height = 60)


Label(root, text = 'Powered by', bg = '#1E1E1E', fg = '#007ACC', font = ('Consolas', 28)).place(x = 860, y = 980, width = 200, height = 40)
Label(root, text = '414', bg = '#1E1E1E', fg = '#007ACC', font = ('Courier new', 42)).place(x = 880, y = 1020, width = 160, height = 60)

root.protocol('WM_WINDOW_DELETE', OFF)
root.bind('<x>', OFF)
root.mainloop()