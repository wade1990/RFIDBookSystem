#!/usr/bin/python
# -*- coding: UTF-8 -*-

import sqlite3

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class ISsql:

    SQL_SUCCESS = 1;
    SQL_FAILED = 0;

    def __init__(self, dataBase):

        #self.dataBase = "booksystem.db"
        self.conn = sqlite3.connect(dataBase)
        self.cur = self.conn.cursor()

    def tableIsExist(self, name):
        select = "SELECT count(*) FROM sqlite_master WHERE type='table' AND name='%s'" % name
        c = self.cur.execute(select)
        b = c.fetchall()[0][0]
        return b

    def insertDataUsers(self, userid, name, uid):
        insert = "insert into users(USERID, NAME, UID) values(%d,'%s','%s')" % (userid, name, uid)
        if(self.tableIsExist("users")):
            self.cur.execute(insert)
            self.conn.commit()
            #print "insert success"
            return self.SQL_SUCCESS
        else:
            print "insert fail, table is not exist."
            return self.SQL_FAILED

    def insertDataBooks(self, bookid, name, uid):
        insert = "insert into books(BOOKID, NAME, UID) values(%d,'%s','%s')" % (bookid, name, uid)
        if (self.tableIsExist("books")):
            self.cur.execute(insert)
            self.conn.commit()

            return self.SQL_SUCCESS
        else:
            print "insert fail, table is not exist."
            return self.SQL_FAILED

    def insertDataBorrowlists(self, bookid, bookname, bookuid,userid,username,useruid, status):
        insert = "insert into borrowlists(BOOKID, BOOKNAME, BOOKUID, USERID, USERNAME, USERUID, STATUS) values(%d,'%s','%s',%d,'%s','%s', %d)" % (bookid,bookname,bookuid,userid,username,useruid, status)
        if (self.tableIsExist("borrowlists")):
            self.cur.execute(insert)
            self.conn.commit()
            #print "insert success"
            return self.SQL_SUCCESS
        else:
            print "insert fail, table is not exist."
            return self.SQL_FAILED

    def selectDataByOne(self, tablename, columnname, data):
        #print type(data)
        if type(data) == int:
            select = "select * from %s where %s = %d" % (tablename, columnname, data)
        if type(data) == str:
            select = "select * from %s where %s = '%s'" % (tablename, columnname, data)
        if (self.tableIsExist(tablename)):
            d = self.cur.execute(select)
            result = d.fetchall()
            print "query success"
            return result
        else:
            print "select fail, table is not exist."
            return self.SQL_FAILED

    def selectDataByN(self, tablename, select):
        #print type(data)
        if (self.tableIsExist(tablename)):
            d = self.cur.execute(select)
            result = d.fetchall()
            print "query success"
            return result
        else:
            print "select fail, table is not exist."
            return self.SQL_FAILED

    def selectDataByOneCount(self, tablename, columnname, data):
        #print type(data)
        if type(data) == int:
            select = "select count(*) from %s where %s = %d" % (tablename, columnname, data)
        if type(data) == str:
            select = "select count(*) from %s where %s = '%s'" % (tablename, columnname, data)
        if (self.tableIsExist(tablename)):
            b = self.cur.execute(select)
            result = b.fetchall()[0][0]

            print "query success"
            return result
        else:
            print "select fail, table is not exist."
            return self.SQL_FAILED

    def selectDataByTwoCount(self, tablename, columnname1, data1, coumnname2, data2):
        #print type(data)
        if type(data1) == int:
            select = "select count(*) from %s where %s = %d and %s = %d" % (tablename, columnname1, data1, coumnname2, data2)
        if type(data1) == str:
            select = "select count(*) from %s where %s = '%s' and %s = %d" % (tablename, columnname1, data1, coumnname2, data2)
        if (self.tableIsExist(tablename)):
            b = self.cur.execute(select)
            result = b.fetchall()[0][0]

            print "query success"
            return result
        else:
            print "select fail, table is not exist."
            return self.SQL_FAILED

    def selectDataByOneParm(self, tablename, columnname, data, parm):
        #print type(data)
        if type(data) == int:
            select = "select %s from %s where %s = %d" % (parm, tablename, columnname, data)
        if type(data) == str:
            select = "select %s from %s where %s = '%s'" % (parm, tablename, columnname, data)
        if (self.tableIsExist(tablename)):
            b = self.cur.execute(select)
            result = b.fetchone()
            print "query success"
            return result
        else:
            print "select fail, table is not exist."
            return self.SQL_FAILED


    def deleteDataByOne(self, tablename, columnname, data):
        #print type(data)
        if type(data) == int:
            delete = "delete from %s where %s = %d" % (tablename, columnname, data)
        if type(data) == str:
            delete = "delete from %s where %s = '%s'" % (tablename, columnname, data)
        if (self.tableIsExist(tablename)):
            result = self.cur.execute(delete)
            self.conn.commit()
            print "delete success"
            return result
        else:
            print "insert fail, table is not exist."
            return self.SQL_FAILED

    def updateDataByOne(self, tablename, setcolumnname, setdata, wherecolumnname1, wheredata1, wherecolumnname2, wheredata2):
        #print type(data)
        if type(wheredata1) == int:
            update = "update %s set %s = %d where %s = %d and %s = %d" % (tablename, setcolumnname, setdata, wherecolumnname1, wheredata1, wherecolumnname2, wheredata2)
        if type(wheredata1) == str:
            update = "update %s set %s = %d where %s = '%s' and %s = %d" % (tablename, setcolumnname, setdata, wherecolumnname1, wheredata1, wherecolumnname2, wheredata2)
        if (self.tableIsExist(tablename)):
            result = self.cur.execute(update)
            self.conn.commit()
            print "update success"
            return result
        else:
            print "insert fail, table is not exist."
            return self.SQL_FAILED

    def databaseClose(self):
        self.cur.close()
        self.conn.close()

if __name__ == '__main__':
    sql = ISsql()
    # insertDataUsers测试
    """
    idata = sql.insertDataUsers(30,"郑书雨","123456789012345")
    if(idata):
        print "insert success"
    row = sql.selectDataUsersByID(30)

    for i in row:
        #sql返回数据为tuple格式，转换为str，在转码显示中文
        print str(tuple(i)).replace("u'", "'").decode("unicode-escape")
    """
    # insertDataBooks测试
    """
    idata = sql.insertDataBooks(2, "中国寓言故事", "123456789012345")
    if (idata):
        print "insert success"
    row = sql.selectDataBooksByName("中国寓言故事")

    for i in row:
        # sql返回数据为tuple格式，转换为str，在转码显示中文
        print str(tuple(i)).replace("u'", "'").decode("unicode-escape")
    """
    """
    iidata = sql.insertDataBorrowlists(2, "中国寓言故事", "123456789012345", 30, "郑书雨", "123456789012345")
    if (idata):
        print "insert success"
    """
    #row = sql.selectDataByOne("users", "USERID", 30)
    #row = sql.selectDataByOne("users", "NAME", "郑书雨")
    #row = sql.selectDataByOne("books", "BOOKID", 2)
    #row = sql.selectDataByOne("borrowlists", "BOOKID", 2)
    sql.deleteDataByOne("users", "USERID", 30)
    row = sql.selectDataByOne("users", "USERID", 30)
    #sql.updateDataByOne("borrowlists", "STATUS", 1, "USERID", 30, "BOOKID", 2)
    #row = sql.selectDataByOne("borrowlists", "BOOKID", 2)
    for i in row:
        # sql返回数据为tuple格式，转换为str，在转码显示中文
        print str(tuple(i)).replace("u'", "'").decode("unicode-escape")








