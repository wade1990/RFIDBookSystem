#-*- coding:utf-8 -*-
import bluetooth
import ServiceAdapter
import threading
import os
# 服务器套接字(用来接收新链接)
server_socket=None



#连接套接字服务子线程
def serveSocket(sock,info):

    print "in serverSocket def"
    # 开个死循环等待客户端发送信息
    while True:
        # 接收1024个字节,然后以UTF-8解码(中文),如果没有可以接收的信息则自动阻塞线程(API)
        print "wait for receive"
        try:
            receive = sock.recv(1024).decode('utf-8')
        # 打印刚刚读到的东西(info=地址)
            print('['+str(info)+']'+receive)
        except BaseException:
            print(BaseException)
            receiveString("h")
            receive = "xxx"

        rsp = receiveString(receive.encode('utf-8'))

        sock.send(rsp.encode('utf-8'))
        if receive.encode('utf-8') == "xxx":
            print "close serveSocket"
            return 0

def receiveString(rec):
    serviceAdapter = ServiceAdapter.ServiceAdapter()
    result = rec.split('|')
    #接口标志a：录入用户
    if result[0] == "a":
        userid = result[1]
        username = result[2]
        (status, row, uid, msg) = serviceAdapter.rfidScanUsers(userid, username)
        if status == "success":
            return "a|success|%s|%s|%s|" % (userid, username, uid)
        if status == "fail":
            return "a|fail|%s|" % msg

    #接口标志b：录入书籍
    if result[0] == "b":
        bookid = result[1]
        bookname = result[2]
        (status, row, uid, msg) = serviceAdapter.rfidScanBooks(bookid, bookname)
        if status == "success":
            return "b|success|%s|%s|%s|" % (bookid, bookname, uid)
        if status == "fail":
            return "b|fail|%s|" % msg

    #接口标志c：rfid扫描用户卡
    if result[0] == "c":
        (status, userid, username, uid, msg) = serviceAdapter.rfidBorrowBooksUserCard()
        if status == "success":
            return "c|success|%s|%s|%s|" % (userid, username, uid)
        if status == "fail":
            return "c|fail|%s|" % msg

    #接口标志d：rfid扫描图书
    if result[0] == "d":
        (status, bookid, bookname, uid, msg) = serviceAdapter.rfidBorrowBooksBookCard()
        if status == "success":
            return "d|success|%s|%s|%s|" % (bookid, bookname, uid)
        if status == "fail":
            return "d|fail|%s|" % msg

    #接口标志e：借阅图书
    if result[0] == "e":
        idcarduid = result[1]
        idcardtext = result[2]
        bookcarduid = result[3]
        bookcardtext = result[4]
        print "idcarduid = %s" % idcarduid
        print "idcarttext = %s" % idcardtext
        print "bookcarduid = %s" % bookcarduid
        print "bookcardtext = %s" % bookcardtext
        (status, rows, msg) = serviceAdapter.rfidBorrowBooks(idcarduid, idcardtext, bookcarduid, bookcardtext)
        if status == "success":
            return "e|success|"
        if status == "fail":
            return "e|fail|%s|" % msg

    #接口标志f: 归还图书
    if result[0] == "f":
        idcarduid = result[1]
        bookcarduid = result[2]
        (status, msg) = serviceAdapter.rfidReturnBooks(idcarduid, bookcarduid)
        if status == "success":
            return "f|success|"
        if status == "fail":
            return "f|fail|%s|" % msg

    #接口标志g：自编语句查询数据库
    if result[0] == "g":
        tablename = result[1]
        select = result[2]
        (status, result, msg) = serviceAdapter.query(tablename, select)
        if status == "success":
            return "g|success|%s|" % result
        if status == "fail":
            return "g|fail|%s|" % msg

    if result[0] == 'h':
        serviceAdapter.destroy()

    return str(result[0])
 
#主线程

print("wait for connect")
# 创建一个服务器套接字,用来监听端口

server_socket=bluetooth.BluetoothSocket(bluetooth.RFCOMM);
# 允许任何地址的主机连接,未知参数:1(端口号,通道号)
server_socket.bind(("", 0))
# 监听端口/通道
server_socket.listen(0);

# 等待有人来连接,如果没人来,就阻塞线程等待(这本来要搞个会话池,以方便给不同的设备发送数据)
sock,info = server_socket.accept()
# 打印有人来了的消息
print(str(info[0])+' Connected!')
# 创建一个线程专门服务新来的连接(这本来应该搞个线程池来管理线程的)
t = threading.Thread(target=serveSocket, args=(sock, info[0]))
# 设置线程守护,防止程序在线程结束前结束
t.setDaemon(True)
try:
    # 启动线程
    #print "running1"
    t.start()
    #print "running2"
    t.join()
finally:
    print "Disconnected"
    sock.close()
    server_socket.close()
    print "all done"

