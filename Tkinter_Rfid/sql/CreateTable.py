#!/usr/bin/python
# -*- coding: UTF-8 -*-

import sqlite3

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class Sql:

    def __init__(self):

        self.dataBase = "booksystem.db"
        self.conn = sqlite3.connect(self.dataBase)
        self.cur = self.conn.cursor()

    def tableIsExist(self,name):
        select = "SELECT count(*) FROM sqlite_master WHERE type='table' AND name=\'%s\'" % name
        c = self.cur.execute(select)
        b = c.fetchall()[0][0]
        return b

    def createTable(self):
        create_user_table = "create table users (" \
                            "ID INTEGER PRIMARY KEY AUTOINCREMENT," \
                            "TIME Timestamp NOT NULL DEFAULT (datetime('now','localtime'))," \
                            "USERID int," \
                            "NAME text," \
                            "UID text)"
        create_book_table = "create table books (" \
                            "ID INTEGER PRIMARY KEY AUTOINCREMENT," \
                            "TIME Timestamp NOT NULL DEFAULT (datetime('now','localtime'))," \
                            "BOOKID int," \
                            "NAME text," \
                            "UID text)"
        create_borrowlist_table = "create table borrowlists (" \
                                  "ID INTEGER PRIMARY KEY AUTOINCREMENT," \
                                  "TIME Timestamp NOT NULL DEFAULT (datetime('now','localtime'))," \
                                  "BOOKID int," \
                                  "BOOKNAME text," \
                                  "BOOKUID text," \
                                  "USERID int," \
                                  "USERNAME text," \
                                  "USERUID text," \
                                  "STATUS int DEFAULT 0)"
        if(self.tableIsExist("users")):
            print "users table exist"
        else:
            self.cur.execute(create_user_table)
            self.conn.commit()
            print "users table create success"

        if (self.tableIsExist("books")):
            print "books table exist"
        else:
            self.cur.execute(create_book_table)
            self.conn.commit()
            print "books table create success"

        if (self.tableIsExist("borrowlists")):
            print "borrowlists table exist"
        else:
            self.cur.execute(create_borrowlist_table)
            self.conn.commit()
            print "borrowlists table create success"


        #self.cur.execute("insert into users (USERID, NAME, UID) values (30, '郑', 11222333)")
        #self.conn.commit()
        self.cur.close()
        self.conn.close()

if __name__ == '__main__':
    sql = Sql()
    sql.createTable()


