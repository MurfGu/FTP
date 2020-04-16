"""
    ftp文件
    服务端
    多线程并发和套接字
"""
import os
import sys
from threading import Thread
from socket import *
from time import sleep

HOST = "0.0.0.0"
PORT = 8888
ADDR = (HOST, PORT)
FTP = "/home/tarena/file/"  # 文件库


class FtpServer(Thread):
    def __init__(self, connfd, addr):
        super().__init__()
        self.connfd = connfd
        self.addr = addr

    def run(self):
        while True:
            data = self.connfd.recv(1024).decode()
            if data == "L":
                self.do_list()
            if data == "G":
                self.get_file()
            if data == "P":
                self.put_file()
            if data == "Q":
                self.quit()

    def do_list(self):
        # 判断文件库是否为空
        file_list = os.listdir(FTP)
        if not file_list:
            self.connfd.send(b"No")
            return
        else:
            self.connfd.send(b"Yes")
            # 发送文件列表
            sleep(0.1)
            data = "\n".join(file_list)
            self.connfd.send(data.encode())
            print("发送文件列表成功")

    def get_file(self):
        file_name = self.connfd.recv(512).decode()
        file_list = os.listdir(FTP)
        if file_name not in file_list:
            self.connfd.send("没有该文件".encode())
        else:
            self.connfd.send("开始下载文件".encode())
            f = open(FTP + file_name, 'rb')
            print("客户端开始下载")
            while True:
                data = f.read(1024)
                if not data:
                    sleep(0.01)
                    self.connfd.send(b'##')
                    break
                self.connfd.send(data)
            f.close()
            print("文件传输完成")

    def put_file(self):
        file_name = self.connfd.recv(1024).decode()
        file_list = os.listdir(FTP)
        if file_name not in file_list:
            self.connfd.send("开始上传".encode())
            f = open(FTP + file_name, 'wb')
            while True:
                data = self.connfd.recv(1024)
                if data == b'##':
                    print("ok")
                    break
                f.write(data)
            f.flush()
            f.close()
            self.connfd.send("上传完成!".encode())
        else:
            self.connfd.send("文件名已存在".encode())

    def quit(self):
        user_address = self.addr
        print("客户端:", user_address, " 已退出")


def main():
    sock = socket()
    sock.bind(ADDR)
    sock.listen(3)

    while True:
        try:
            connfd, addr = sock.accept()
            print("客户端:", addr, " 已连接")
        except:
            sys.exit("退出服务端")
        t = FtpServer(connfd, addr)
        t.setDaemon(True)
        t.start()


if __name__ == '__main__':
    main()
