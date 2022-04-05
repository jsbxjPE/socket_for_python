import socket
import os
import platform
from subprocess import run
import ast
import tkinter

global cmd_open
global intranet_ip
global system
global msg_client_run
global c
global msg_tk
global receive_ip

receive_ip = '127.0.0.1'

msg_tk = tkinter.Tk()
msg_tk.title('msg')

msg_client_run = False
cmd_open = False

def setup(host,port):
    global intranet_ip
    global system
    global c
    global msg_client_run

    # 获取内网地址
    ip = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    ip.connect(('8.8.8.8', 80))
    intranet_ip = ip.getsockname()[0] # 设置ip地址
    ip.close()

    # 获取系统信息
    system = platform.platform()
    
    # 创建socket
    c = socket.socket()
    c.connect((host, port)) # 绑定host and port

    msg_client_run = True

def run():
    global c
    global intranet_ip
    global system
    global msg_client_run
    global receive_ip
    # print('run client !!!')
    while msg_client_run:
        msg_input = input('msg : ')
        if msg_input == '/server_stop':
            msg_data = {'send_ip':intranet_ip,'receive_ip':'server','msg':'','system':system,'instructions':'stop server','command':None}
            c.send(str(msg_data).encode('utf-8'))
            import os
            print('server stop ...')
            os._exit(0)
        elif msg_input == '/exit':
            msg_data = {'send_ip':intranet_ip,'receive_ip':'server','msg':'','system':system,'instructions':'user exit','command':None}
            c.send(str(msg_data).encode('utf-8'))
            import os
            print('msg stop ...')
            os._exit(0)
        elif msg_input == '/rcmd':
            msg_data = {'send_ip':intranet_ip,'receive_ip':'server','msg':'','system':system,'instructions':'cmd','command':None}
            c.send(str(msg_data).encode('utf-8'))
            print('open command line ...')
        elif msg_input == '/scmd':
            msg_data = {'send_ip':intranet_ip,'receive_ip':'server','msg':'','system':system,'instructions':'stop cmd','command':None}
            c.send(str(msg_data).encode('utf-8'))
            print('close command line ...')
        elif '/run ' == msg_input:
            msg_data = {'send_ip':intranet_ip,'receive_ip':receive_ip,'msg':'','system':system,'instructions':'run','command':msg_input.split('/run ')}
            c.send(str(msg_data).encode('utf-8'))
            print('close command line ...')
        else:
            msg_data = {'send_ip':intranet_ip,'receive_ip':receive_ip,'msg':msg_input,'system':system,'instructions':None,'command':None}
            c.send(str(msg_data).encode('utf-8'))