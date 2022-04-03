import tkinter
import socket
import ast

ip = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
ip.connect(('8.8.8.8', 80))
host = ip.getsockname()[0] # 设置ip地址
ip.close()
print(host)
port = 7794
listen_number = 100

s = socket.socket()
s.bind((str(host), int(port))) # 绑定ip和端口
s.listen(int(listen_number)) # 等待客户端连接
print(s)
join_run = True

server_uuid = dict()

while join_run:
    print(1)
    c, addr = s.accept()
    print(c)
    while join_run:
        print(2)
        try:
            name_name = 'name'
            host_name = 'host'
            port_name = 'port'
            data = ast.literal_eval(c.recv(8192).decode())
            if data['join']:
                server_uuid[data['uuid']] = dict(name_name = data['name'],hosr_name = data['host'],port_name = data['port'])
                print(server_uuid)
            elif not data['join']:
                server_uuid[data['uuid']] = dict(name_name = data['name'],hosr_name = None,port_name = None)
        except:
            break