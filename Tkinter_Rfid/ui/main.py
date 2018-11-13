#!/usr/bin/python
# -*- coding: UTF-8 -*-
import sys

sys.path.append("..")
from ui.MainPage import *

root = Tk()
root.title("图书管理程序")
MainPage(root)
root.mainloop()
