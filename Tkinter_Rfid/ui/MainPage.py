#!/usr/bin/python
# -*- coding: UTF-8 -*-
import sys

sys.path.append("..")
from ui.LoginPage import *
from tkMessageBox import *

from ui.BorrowBook import *
from ui.ReturnBook import *


class MainPage(object):
    def __init__(self, master = None):
        self.root = master
        self.root.geometry('%dx%d' % (600, 600))
        self.createPage()

    def createPage(self):
        self.page = Frame(self.root)  # 创建Frame
        self.page.pack()
        Label(self.page).grid(row=0, stick=W, pady=10)
        Button(self.page, text="图书馆管理员入口", command=self.mInterface).grid(row=1, stick=W, pady=10)
        Button(self.page, text="图书借阅",command=self.bInterface).grid(row=3, stick=W, pady=10)
        Button(self.page, text="图书归还",command=self.rInterface).grid(row=5, stick=W, pady=10)
        Button(self.page, text="退出", command=self.quit).grid(row=7, stick=W, pady=10)

    def mInterface(self):
        self.page.destroy()
        LoginPage(self.root)

    def bInterface(self):
        self.page.destroy()
        BorrowBook(self.root)

    def rInterface(self):
        self.page.destroy()
        ReturnBook(self.root)

    def quit(self):
        self.page.destroy()
        self.root.destroy()










