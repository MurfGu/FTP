"""
    ftp文件
    客户端
"""

from socket import *
from time import sleep

ADDR = ("127.0.0.1", 8000)
DOWNLOAD = "/home/tarena/murf/month02/download/"


class FtpClient:
    def __init__(self, sockfd):
        self.sockfd = sockfd

    def do_list(self):
        self.sockfd.send(b"L")  # 发送请求
        # 等待回复 Yes/No
        data = self.sockfd.recv(128).decode()
        if data == "Yes":
            msg = self.sockfd.recv(4096).decode()
            print(msg)
        else:
            print("获取文件列表失败")

    def get_file(self):
        self.sockfd.send(b"G")
        file_name = input("请输入文件名:")
        self.sockfd.send(file_name.encode())
        msg = self.sockfd.recv(512).decode()
        print(msg)
        if msg == "开始下载文件":
            f = open(DOWNLOAD + file_name, "wb")
            while True:
                data = self.sockfd.recv(1024)
                if data == b'##':
                    print("...")
                    break
                f.write(data)
            f.flush()
            f.close()
            print("文件下载完成")

    def put_file(self):
        self.sockfd.send(b"P")
        file_path = input("请输入文件路径:")
        try:
            f = open(file_path, 'rb')
            file_name = input("请输入上传文件名:")
            self.sockfd.send(file_name.encode())
            msg = self.sockfd.recv(512).decode()
            print(msg)
            if msg == "开始上传":
                while True:
                    data = f.read(1024)
                    if not data:
                        sleep(0.01)
                        self.sockfd.send(b'##')
                        print("...")
                        break
                    self.sockfd.send(data)
                f.close()
                print(self.sockfd.recv(1024).decode())

        except:
            print("路径错误 或 没有该文件")

    def quit(self):
        self.sockfd.send(b'Q')
        print("成功退出客户端")


def main():
    s = socket()
    s.connect(ADDR)
    ftp = FtpClient(s)

    while True:
        try:
            print("----命令选项-----")
            print(">>  list      <<")
            print(">>  get file  <<")
            print(">>  put file  <<")
            print(">>  quit      <<")

            cmd = input(">>")
            if cmd == "list":
                ftp.do_list()
            elif cmd == "get file":
                ftp.get_file()
            elif cmd == "put file":
                ftp.put_file()
            elif cmd == "quit":
                ftp.quit()
                break
        except:
            ftp.quit()
            break


if __name__ == '__main__':
    main()
