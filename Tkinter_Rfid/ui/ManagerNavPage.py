#!/usr/bin/python
# -*- coding: UTF-8 -*-
import sys
from InputPage import *

from InputPageUser import *
sys.path.append("..")
import ui.MainPage
from tkMessageBox import *


class ManagerNavPage(object):
    def __init__(self, master = None):
        self.root = master
        self.root.geometry('%dx%d' % (600, 600))
        self.createPage()

    def createPage(self):
        self.page = Frame(self.root)  # 创建Frame
        self.page.pack()
        Label(self.page).grid(row=0, stick=W, pady=10)
        Button(self.page, text="图书录入", command=self.bInterface).grid(row=1, stick=W, pady=10)
        Button(self.page, text="用户录入", command=self.uInterface).grid(row=3, stick=W, pady=10)
        Button(self.page, text="后退", command=self.back).grid(row=5, stick=W, pady=10)
        Button(self.page, text="退出", command=self.quit).grid(row=7, stick=W, pady=10)


    def bInterface(self):
        self.page.destroy()
        InputPage(self.root)

    def uInterface(self):
        self.page.destroy()
        InputPageUser(self.root)

    def back(self):
        self.page.destroy()
        ui.MainPage.MainPage(self.root)

    def quit(self):
        self.page.destroy()
        self.root.destroy()









