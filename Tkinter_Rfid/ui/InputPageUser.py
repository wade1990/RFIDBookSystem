#!/usr/bin/python
# -*- coding: UTF-8 -*-
import time
import sys

sys.path.append("..")
from Tkinter import *
from MFRC522pg.WriteUser import *
import ui.MainPage

reload(sys)
sys.setdefaultencoding('utf-8')
from tkMessageBox import *

class InputPageUser(object):
    def __init__(self, master = None):
        self.root = master
        self.root.geometry('%dx%d' % (600, 600))
        self.userName = StringVar
        self.userId = StringVar
        self.userUid = StringVar
        self.isSuccess = StringVar
        self.createPage()
        self.writeusers = RC522WriteUsers()

    def createPage(self):
        self.page = Frame(self.root)  # 创建Frame
        self.page.pack()
        Label(self.page).grid(row=0, stick=W, pady=10)

        Label(self.page, text='用户ID').grid(row=1, stick=W, pady=10)
        self.userid = Entry(self.page)
        self.userid.grid(row=1, column=1, stick=E)

        Label(self.page, text='用户姓名').grid(row=2, stick=W, pady=10, columnspan = 2)
        self.username = Entry(self.page)
        self.username.grid(row=2, column=1, stick=E)

        Button(self.page, text="写入RFID", command=self.rfidScan).grid(row=3, stick=W, pady=10)

        Label(self.page, text='用户UID').grid(row=4, stick=W, pady=10)

        Label(self.page, text='写入状态').grid(row=5, stick=W, pady=10)

        Button(self.page, text="查询",command=self.queryData).grid(row=6, stick=W,pady=10)

        Button(self.page, text="后退", command=self.back).grid(row=6, column=1, stick=E)

        self.text = Text(self.page, height=6, width=60)
        self.text.grid(row=7,rowspan=3,columnspan=2,stick=E,pady=10)
        Button(self.page, text="退出", command=self.exit).grid(row=10, column=1, stick=E)
        self.text.insert(1.0, "请先输入'用户ID'和'用户姓名'，录入完毕后点击'写入RFID'\n")

    def rfidScan(self):
        self.userId = self.userid.get()
        self.userName = self.username.get()
        if self.userId != "" and self.userName != "":
            self.text.insert(1.0, "请刷用户ID卡\n")
            self.page.update()
            time.sleep(1)
            (uid, status, rows) = self.writeusers.writeUser(self.userId,self.userName)
            #print "%d, %s" % (int(status), uid)
            if int(status) == 0:
                Label(self.page, text=uid).grid(row=4, column=1, stick=E)
                Label(self.page, text="写入成功！！！").grid(row=5, column=1, stick=E)
                self.text.insert(1.0, "RFID卡写入成功\n")
                for i in rows:
                    a = str(tuple(i)).replace("u'", "\'").decode("unicode-escape")
                self.text.insert(1.0, "%s\n" % a)
            if int(status) == 1:
                Label(self.page, text="写入失败！！！").grid(row=5, column=1, stick=E)
                self.text.insert(1.0, "数据写入失败，该RFID已经被其他用户使用（RFID中的UID与数据库中已有的uid重复）\n")
            if int(status) == 2:
                Label(self.page, text="写入失败！！！").grid(row=5, column=1, stick=E)
                self.text.insert(1.0, "数据写入失败，用户ID不能重复（USERID与数据库中已有的USERID重复）\n")
        else:
            Label(self.page, text="写入失败！！！").grid(row=5, column=1, stick=E)
            self.text.insert(1.0, "请完整输入ID和名称\n")

    def queryData(self):
        select = "select * from users"
        self.text.delete(0.0,END)
        rowl = self.writeusers.queryall("users", select)
        for i in rowl:
            self.text.insert(END, "%s\n" % str(tuple(i)).replace("u'", "'").decode("unicode-escape"))

    def back(self):
        self.writeusers.databaseClose()
        self.page.destroy()
        ui.MainPage.MainPage(self.root)

    def exit(self):
        self.writeusers.databaseClose()
        self.page.destroy()
        self.root.destroy()

