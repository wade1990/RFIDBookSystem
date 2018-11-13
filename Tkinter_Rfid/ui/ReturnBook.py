#!/usr/bin/python
# -*- coding: UTF-8 -*-

import time
import sys

sys.path.append("..")

from Tkinter import *
from tkMessageBox import *
reload(sys)
sys.setdefaultencoding('utf-8')

from MFRC522pg.WriteBorrowlistsReturn import *
import ui.MainPage

class ReturnBook(object):
    def __init__(self, master = None):
        self.root = master
        self.root.geometry('%dx%d' % (600, 600))
        self.createPage()
        self.rrbls = RC522WriteBorrowlistsReturn()


    def createPage(self):
        self.page = Frame(self.root)  # 创建Frame
        self.page.pack()
        Label(self.page).grid(row=0, stick=W, pady=10)
        self.startBowstart = Button(self.page, text="开始归还",command=self.startBorrow)
        self.startBowstart.grid(row=1, stick=W, pady=10)
        self.startBowstop = Button(self.page, text="归还完成", command=self.back)
        self.startBowstop.grid(row=1, column=1,stick=E)
        Button(self.page, text="退出", command=self.stopBorrow).grid(row=10, column=1,stick=E)
        Button(self.page, text="继续", command=self.returncontinue).grid(row=10, stick=W, pady=10)



    def startBorrow(self):
        Label(self.page, text='用户ID').grid(row=2, stick=W, pady=10)

        Label(self.page, text='用户姓名').grid(row=3, stick=W, pady=10)

        Label(self.page, text='图书ID').grid(row=4, stick=W, pady=10)

        Label(self.page, text='图书书名').grid(row=5, stick=W, pady=10)
        self.text = Text(self.page, height=6, width=60)
        self.text.grid(row=7, rowspan=3, columnspan=2, stick=E, pady=10)
        taguseridcard = 1
        tagbookcard =1
        while(taguseridcard):
            self.text.insert(1.0, "请先扫描用户ID卡\n")
            self.page.update()
            (self.idcarduid, self.idcardtext, idcardtypetext) = self.rrbls.readUserIDCard()
            if idcardtypetext.replace(' ', '') == 'USERIDCARD':
                print "ok"
                taguseridcard = 0
                self.text.insert(1.0, "扫描成功\n")
                select = "select USERID from users where UID=%s" % str(self.idcarduid)
                result = self.rrbls.queryall("users", select)
                Label(self.page, text=str(tuple(result)[0][0])).grid(row=2, column=1, stick=E)
                Label(self.page, text=self.idcardtext.replace(" ", "")).grid(row=3, column=1, stick=E)

            else:
                print "Read Failure, after 2 seconds, pls use id card and retry"
                self.text.insert(1.0, "请使用用户ID卡重试\n")
                self.page.update()
                time.sleep(2)
        time.sleep(1)


        while (tagbookcard):
            self.text.insert(1.0, "请扫描图书RFID卡\n")
            self.page.update()
            (bookcarduid, bookcardtext, bookcardtypetext) = self.rrbls.readBookCard()
            # print type('BOOK')
            if bookcardtypetext.replace(' ', '') == 'BOOKCARD':
                print "ok"
                tagbookcard = 0
                self.text.insert(1.0, "扫描成功\n")
                select = "select BOOKID from books where UID=%s" % str(bookcarduid)
                result = self.rrbls.queryall("books", select)
                Label(self.page, text=str(tuple(result)[0][0])).grid(row=4, column=1, stick=E)
                Label(self.page, text=bookcardtext.replace(" ", "")).grid(row=5, column=1, stick=E)
            else:
                print "Read Failure, after 2 seconds, pls use id card and retry"
                self.text.insert(1.0, "请使用图书RFID卡重试\n")
                self.page.update()
                time.sleep(2)

        (status, userid) = self.rrbls.writeBorrowlistsReturn(self.idcarduid, bookcarduid)
        if status == 0:
            self.text.insert(1.0, "还书失败，数据库无此书借阅记录，请联系管理员\n")
        if status == 1:
            self.text.insert(1.0, "还书成功\n")
        if status == 2:
            self.text.insert(1.0, "还书失败，本书目前被ID=%d同学借阅\n" % userid)
        self.text.insert(1.0, "如果想继续还书，请点击继续按钮\n")


    def back(self):
        self.rrbls.databaseClose()
        self.page.destroy()
        ui.MainPage.MainPage(self.root)

    def stopBorrow(self):
        self.rrbls.databaseClose()
        self.page.destroy()
        self.root.destroy()

    def returncontinue(self):
        tagbookcard = 1
        while (tagbookcard):
            self.text.insert(1.0, "请扫描图书RFID卡\n")
            self.page.update()
            (bookcarduid, bookcardtext, bookcardtypetext) = self.rrbls.readBookCard()
            # print type('BOOK')
            if bookcardtypetext.replace(' ', '') == 'BOOKCARD':
                print "ok"
                tagbookcard = 0
                self.text.insert(1.0, "扫描成功\n")
                select = "select BOOKID from books where UID=%s" % str(bookcarduid)
                result = self.rrbls.queryall("books", select)
                Label(self.page, text=str(tuple(result)[0][0])).grid(row=4, column=1, stick=E)
                Label(self.page, text=bookcardtext.replace(" ", "")).grid(row=5, column=1, stick=E)
            else:
                print "Read Failure, after 2 seconds, pls use id card and retry"
                self.text.insert(1.0, "请使用图书RFID卡重试\n")
                self.page.update()
                time.sleep(2)

        (status, userid) = self.rrbls.writeBorrowlistsReturn(self.idcarduid, bookcarduid)
        if status == 0:
            self.text.insert(1.0, "还书失败，数据库无此书借阅记录，请联系管理员\n")
        if status == 1:
            self.text.insert(1.0, "还书成功\n")
        if status == 2:
            self.text.insert(1.0, "还书失败，本书目前被ID=%d同学借阅\n" % userid)
        self.text.insert(1.0, "如果想继续还书，请点击继续按钮\n")






