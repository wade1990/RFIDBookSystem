#!/usr/bin/python
# -*- coding: UTF-8 -*-
import time
import sys

sys.path.append("..")

reload(sys)
sys.setdefaultencoding('utf-8')
from MFRC522pg.WriteUser import *
from MFRC522pg.WriteBooks import *
from MFRC522pg.WriteBorrowlists import *
from MFRC522pg.WriteBorrowlistsReturn import *

class ServiceAdapter():
    def __init__(self):
        self.writeusers = RC522WriteUsers()
        self.writebooks = RC522WriteBooks()
        self.borrowbooks = RC522WriteBorrowlists()
        self.returnBooks = RC522WriteBorrowlistsReturn()
        self.success = "success"
        self.fail = "fail"

    def rfidScanUsers(self, userid, username):

        if userid != "" and username != "":
            (uid, status, rows) = self.writeusers.writeUser(userid, username)
            if int(status) == 0:
                return self.success, rows, uid, None
            if int(status) == 1:
                msg = "数据写入失败，该RFID已经被其他用户使用（RFID中的UID与数据库中已有的uid重复）"
                return self.fail, None, None, msg
            if int(status) == 2:
                msg = "数据写入失败，用户ID不能重复（USERID与数据库中已有的USERID重复)"
                return self.fail, None, None, msg
        else:
            msg = "请完整输入ID和名称"
            return self.fail, msg, None

    def rfidScanBooks(self, bookid, bookname):

        if bookid != "" and bookname != "":
            (uid, status, rows) = self.writebooks.writeBooks(bookid, bookname)
            if int(status) == 0:
                return self.success, rows, uid, None
            if int(status) == 1:
                msg = "数据写入失败，该RFID已经被其他图书使用（RFID中的UID与数据库中已有的uid重复)"
                return self.fail, None, None, msg
            if int(status) == 2:
                msg = "数据写入失败，图书ID不能重复（BookID与数据库中已有的bookid重复）"
                return self.fail, None, None, msg
        else:
            msg = "请完整输入ID和名称"
            return self.fail, None, None, msg

    def rfidBorrowBooksUserCard(self):
        (idcarduid, idcardtext, idcardtypetext) = self.borrowbooks.readUserIDCard()
        if idcardtypetext.replace(' ', '') == 'USERIDCARD':
            select = "select USERID from users where UID=%s" % str(idcarduid)
            userid = self.borrowbooks.queryall("users", select)
            return self.success, str(tuple(userid)[0][0]), idcardtext.replace(" ", ""), idcarduid, None
        else:
            msg = "请使用用户ID卡重试"
            return self.fail, None, None, None, msg

    def rfidBorrowBooksBookCard(self):
        (bookcarduid, bookcardtext, bookcardtypetext) = self.borrowbooks.readBookCard()
        if bookcardtypetext.replace(' ', '') == 'BOOKCARD':
            select = "select BOOKID from books where UID=%s" % str(bookcarduid)
            bookid = self.borrowbooks.queryall("books", select)
            return self.success, str(tuple(bookid)[0][0]), bookcardtext.replace(" ", ""), bookcarduid, None
        else:
            msg = "请使用图书RFID卡重试"
            return self.fail, None, None, None, msg

    def rfidBorrowBooks(self, idcarduid, idcardtext, bookcarduid, bookcardtext):
        (status, rows) = self.borrowbooks.writeBorrowlists(idcarduid, idcardtext, bookcarduid, bookcardtext)
        if status == 0:
            return self.success, rows, None
        if status == 1:
            for i in rows:
                userid = i[5]
                username = str(tuple(i[6])) \
                    .replace("u'", "") \
                    .replace(",", "") \
                    .replace("'", "") \
                    .replace(" ", "") \
                    .replace("(", "") \
                    .replace(")", "") \
                    .decode('unicode-escape')
            msg = "借书失败，借书数据已经存在，id=%s, name=%s 正在借阅此书\n" % (userid, username)
            return self.fail, None, msg

    def rfidReturnBooks(self, idcarduid, bookcarduid):
        (status, userid) = self.returnBooks.writeBorrowlistsReturn(idcarduid, bookcarduid)
        if status == 0:
            msg = "还书失败，数据库无此书借阅记录，请联系管理员"
            return self.fail, msg
        if status == 1:
            return self.success, None
        if status == 2:
            msg = "还书失败，本书目前被ID=%d同学借阅\n" % userid
            return self.fail, msg

    def query(self, tablename, select):
        result = ""
        rowl = self.borrowbooks.queryall(tablename, select)
        if rowl == 0:
            msg = "查询失败，数据库无此表"
            return self.fail, None, msg
        if rowl == "":
            msg = "查询失败，记录不存在"
            return self.fail, None, msg
        else:
            for i in rowl:
                result = "%s\n%s" % (result, str(tuple(i)).replace("u'", "'").decode("unicode-escape"))
            return self.success, result, None

    def destroy(self):
        self.returnBooks.databaseClose()




