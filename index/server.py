from distutils.ccompiler import gen_lib_options
from glob import glob
import socket
import ast

global s
global msg_server_run

msg_server_run = False

def setup(host,port,listen_number):
    global s
    global msg_server_run
    s = socket.socket()
    s.bind((str(host), int(port))) # 绑定ip和端口
    s.listen(listen_number) # 等待客户端连接
    msg_server_run = True

def run():
    global s
    global msg_server_run
    # print('run server !!!')
    while msg_server_run:
        c, addr = s.accept() # 建立客户端连接
        while msg_server_run:
            try:
                data = ast.literal_eval(c.recv(8192).decode()) # 接收客户端信息
                send_ip = data['send_ip']
                receive_ip = data['receive_ip']
                msg = data['msg']
                system = data['system']
                msg_instructions = data['instructions']
                command = data['command']

                if msg_instructions == 'stop server':
                    msg_server_run = False
                    msg_data = {'send_ip':'server','receive_ip':'everyone','msg':'the server is about to stop','system':'server system','instructions':'the server requests the user to exit','command':None}
                    print('{} request server stop'.format(send_ip))
                    c.send(str(msg_data).encode('utf-8'))
                elif msg_instructions == 'user exit':
                    msg_data = {'send_ip':'server','receive_ip':'everyone','msg':send_ip + '已退出服务器','system':'server system','instructions':'msg','command':None}
                    print('{} request to exit the server'.format(send_ip))
                    c.send(str(msg_data).encode('utf-8'))
                elif msg_instructions == 'cmd':
                    msg_data = {'send_ip':'server','receive_ip':'everyone','msg':send_ip + '已开启命令行','system':'server system','instructions':'msg','command':None}
                    print('{} open command line'.format(send_ip))
                    c.send(str(msg_data).encode('utf-8'))
                elif msg_instructions == 'stop cmd':
                    msg_data = {'send_ip':'server','receive_ip':'everyone','msg':send_ip + '已关闭命令行','system':'server system','instructions':'msg','command':None}
                    print('{} close command line'.format(send_ip))
                    c.send(str(msg_data).encode('utf-8'))
                elif msg_instructions == 'command':
                    if command == 'close': # 执行命令者
                        msg_data = {'send_ip':send_ip,'receive_ip':receive_ip,'msg':send_ip + ' 没有开启命令行','system':system,'instructions':'command','command':'close'}
                        print('{} wants {} to execute the command {}, but {} does not open the command line'.format(send_ip,receive_ip,command,send_ip))
                        c.send(str(msg_data).encode('utf-8'))
                    elif command == 'ok': # 执行命令者
                        msg_data = {'send_ip':send_ip,'receive_ip':receive_ip,'msg':send_ip + ' 命令执行成功','system':system,'instructions':'command','command':'ok'}
                        print('{} wants {} to execute the command {}, {} say "ok"'.format(receive_ip,send_ip,command,send_ip))
                        c.send(str(msg_data).encode('utf-8'))
                    elif command or command == None: # 发送命令者
                        msg_data = {'send_ip':send_ip,'receive_ip':receive_ip,'msg':send_ip + ' 没有键入命令','system':system,'instructions':'command','command':'no'}
                        print('{} no output command'.format(send_ip))
                        c.send(str(msg_data).encode('utf-8'))
                    elif command == 'error': # 执行命令者
                        msg_data = {'send_ip':send_ip,'receive_ip':receive_ip,'msg':send_ip + ' 执行命令时错误','system':system,'instructions':'command','command':'error'}
                        print('{} error executing command'.format(send_ip))
                        c.send(str(msg_data).encode('utf-8'))
                elif msg_instructions == 'msg':
                    msg_data = {'send_ip':send_ip,'receive_ip':receive_ip,'msg':msg,'system':system,'instructions':'msg','command':None}
                    print('{} to {} : {}'.format(send_ip,receive_ip,msg))
                    c.send(str(msg_data).encode('utf-8'))
            except Exception as e:
                print(repr(e))