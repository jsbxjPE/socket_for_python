import socket
import os
import platform
import subprocess
import ast
import tkinter
import threading

global cmd_open
global intranet_ip
global system
global msg_client_run
global c
global receive_ip

receive_ip = '192.168.31.110'

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
    # print(intranet_ip)

    # 获取系统信息
    system = platform.platform()
    
    # 创建socket
    c = socket.socket()
    c.connect((host, port)) # 绑定host and port

    msg_client_run = True

def run():
    global c
    global system
    global msg_client_run
    global receive_ip
    global cmd_open
    global intranet_ip
    print('run client !!!')
    while msg_client_run:
        msg_input = input('msg : ')
        if msg_input == '/server_stop':
            msg_data = {'send_ip':intranet_ip,'receive_ip':'server','msg':'','system':system,'instructions':'stop server','command':None,'server_path':None,'command_run':None}
            c.send(str(msg_data).encode('utf-8')) #发送信息
            import os
            print('server stop ...')
            os._exit(0)
        elif msg_input == '/exit':
            msg_data = {'send_ip':intranet_ip,'receive_ip':'server','msg':'','system':system,'instructions':'user exit','command':None,'server_path':None,'command_run':None}
            c.send(str(msg_data).encode('utf-8')) #发送信息
            import os
            print('msg stop ...')
            os._exit(0)
        elif msg_input == '/rcmd':
            msg_data = {'send_ip':intranet_ip,'receive_ip':'server','msg':'','system':system,'instructions':'cmd','command':None,'server_path':None,'command_run':None}
            c.send(str(msg_data).encode('utf-8')) #发送信息
            print('open command line ...')
            cmd_open = True
            print(cmd_open)
        elif msg_input == '/scmd':
            msg_data = {'send_ip':intranet_ip,'receive_ip':'server','msg':'','system':system,'instructions':'stop cmd','command':None,'server_path':None,'command_run':None}
            c.send(str(msg_data).encode('utf-8')) #发送信息
            print('close command line ...')
            cmd_open = False
            print(cmd_open)
        elif '/run ' in msg_input:
            msg_data = {'send_ip':intranet_ip,'receive_ip':receive_ip,'msg':'','system':system,'instructions':'command','command':msg_input.split('/run ')[1],'server_path':None,'command_run':None}
            c.send(str(msg_data).encode('utf-8')) #发送信息
        elif '/ftp_server ' in msg_input:
            msg_data = {'send_ip':intranet_ip,'receive_ip':'server','msg':'','system':system,'instructions':'_ftp','command':None,'server_path':msg_input.split('/ftp_server ')[1],'command_run':None}
            c.send(str(msg_data).encode('utf-8')) #发送信息
        else:
            msg_data = {'send_ip':intranet_ip,'receive_ip':receive_ip,'msg':msg_input,'system':system,'instructions':'msg','command':None,'server_path':None,'command_run':None}
            c.send(str(msg_data).encode('utf-8')) #发送信息

        data = ast.literal_eval(c.recv(8192).decode()) #接收信息
        a_ip = data['send_ip']
        b_ip = data['receive_ip']
        msg = data['msg']
        msg_system = data['system']
        msg_instructions = data['instructions']
        msg_command = data['command']
        msg_command_run = data['command_run']
        if not (msg_command_run == None or ''):
            if msg_instructions == 'command' and msg_command == '.':
                if cmd_open == True:
                    try:
                        computet_command_run_end = subprocess.run(str(msg_command_run),shell = True)
                        print(computet_command_run_end)
                        msg_data = {'send_ip':intranet_ip,'receive_ip':receive_ip,'msg':'','system':system,'instructions':'command','command':'ok','server_path':None,'command_run':computet_command_run_end}
                        c.send(str(msg_data).encode('utf-8')) #发送信息
                    except:
                        msg_data = {'send_ip':intranet_ip,'receive_ip':receive_ip,'msg':'','system':system,'instructions':'command','command':'error','server_path':None,'command_run':computet_command_run_end}
                        c.send(str(msg_data).encode('utf-8')) #发送信息
                else:
                    msg_data = {'send_ip':intranet_ip,'receive_ip':receive_ip,'msg':'','system':system,'instructions':'command','command':'close','server_path':None,'command_run':computet_command_run_end}
                    c.send(str(msg_data).encode('utf-8')) #发送信息
        elif msg_instructions == 'msg':
            if b_ip == intranet_ip or b_ip =='server' or b_ip =='everyone':
                print('{} to you : {}'.format(a_ip,msg))