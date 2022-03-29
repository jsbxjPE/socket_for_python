import socket

def setup(host,port,listen_number):
    s = socket.socket()
    s.bind((str(host), int(port))) # 绑定ip和端口
    s.listen(listen_number) # 等待客户端连接
    print(s)
    return s