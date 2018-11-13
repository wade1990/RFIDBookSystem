#!/usr/bin/python
# -*- coding: UTF-8 -*-
import time
import sys

sys.path.append("..")
from Tkinter import *
from MFRC522pg.WriteBooks import *
import ui.MainPage

reload(sys)
sys.setdefaultencoding('utf-8')
from tkMessageBox import *

class InputPage(object):
    def __init__(self, master = None):
        self.root = master
        self.root.geometry('%dx%d' % (600, 600))
        self.bookName = StringVar
        self.bookId = StringVar
        self.bookUid = StringVar
        self.isSuccess = StringVar
        self.createPage()
        self.writebooks = RC522WriteBooks()

    def createPage(self):
        self.page = Frame(self.root)  # 创建Frame
        self.page.pack()
        Label(self.page).grid(row=0, stick=W, pady=10)



        Label(self.page, text='图书ID').grid(row=1, stick=W, pady=10)
        self.bookid = Entry(self.page)
        self.bookid.grid(row=1, column=1, stick=E)

        Label(self.page, text='图书名称').grid(row=2, stick=W, pady=10, columnspan = 2)
        self.bookname = Entry(self.page)
        self.bookname.grid(row=2, column=1, stick=E)

        Button(self.page, text="写入RFID", command=self.rfidScan).grid(row=3, stick=W, pady=10)

        Label(self.page, text='图书UID').grid(row=4, stick=W, pady=10)

        Label(self.page, text='写入状态').grid(row=5, stick=W, pady=10)

        Button(self.page, text="查询",command=self.queryData).grid(row=6, stick=W,pady=10)

        Button(self.page, text="后退", command=self.back).grid(row=6, column=1, stick=E)

        self.text = Text(self.page, height=6, width=60)
        self.text.grid(row=7,rowspan=3,columnspan=2,stick=E,pady=10)
        Button(self.page, text="退出", command=self.exit).grid(row=10, column=1, stick=E)
        self.text.insert(1.0, "请先输入'图书ID'和'图书名称'，录入完毕后点击'写入RFID'\n")

    def rfidScan(self):
        self.bookId = self.bookid.get()
        self.bookName = self.bookname.get()
        if self.bookId != "" and self.bookName != "":
            self.text.insert(1.0, "请刷书卡\n")
            self.page.update()
            time.sleep(1)
            (uid, status, rows) = self.writebooks.writeBooks(self.bookId,self.bookName)
            print "%d, %s" % (int(status), uid)
            if int(status) == 0:
                Label(self.page, text=uid).grid(row=4, column=1, stick=E)
                Label(self.page, text="写入成功！！！").grid(row=5, column=1, stick=E)
                self.text.insert(1.0, "RFID卡写入成功\n")
                for i in rows:
                    a = str(tuple(i)).replace("u'", "\'").decode("unicode-escape")
                self.text.insert(1.0, "%s\n" % a)
            if int(status) == 1:
                Label(self.page, text="写入失败！！！").grid(row=5, column=1, stick=E)
                self.text.insert(1.0, "数据写入失败，该RFID已经被其他图书使用（RFID中的UID与数据库中已有的uid重复）\n")
            if int(status) == 2:
                Label(self.page, text="写入失败！！！").grid(row=5, column=1, stick=E)
                self.text.insert(1.0, "数据写入失败，图书ID不能重复（BookID与数据库中已有的bookid重复）\n")
        else:
            Label(self.page, text="写入失败！！！").grid(row=5, column=1, stick=E)
            self.text.insert(1.0, "请完整输入ID和名称\n")

    def queryData(self):
        select = "select * from books"
        self.text.delete(0.0,END)
        rowx = self.writebooks.queryall("books", select)
        for i in rowx:
            self.text.insert(END, "%s\n" % str(tuple(i)).replace("u'", "'").decode("unicode-escape"))

    def back(self):
        self.writebooks.databaseClose()
        self.page.destroy()
        ui.MainPage.MainPage(self.root)

    def exit(self):
        self.writebooks.databaseClose()
        self.page.destroy()
        self.root.destroy()

