import socket
import ast
import threading

global s
global msg_server_run
global intranet_ip
global command_run

msg_server_run = False

def start_ftp_server(host,port,user,password,path):
    from pyftpdlib.handlers import FTPHandler
    from pyftpdlib.servers import FTPServer
    from pyftpdlib.authorizers import DummyAuthorizer

    authorizer = DummyAuthorizer()
    authorizer.add_user(user,password,path,perm='elradfmwM')
    handler = FTPHandler
    handler.authorizer = authorizer

    server = FTPServer((host,port), handler)
    server.serve_forever()

def setup(host,port,listen_number):
    global s
    global msg_server_run
    global intranet_ip

    # 获取内网地址
    ip = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    ip.connect(('8.8.8.8', 80))
    intranet_ip = ip.getsockname()[0] # 设置ip地址
    ip.close()

    s = socket.socket()
    s.bind((str(host), int(port))) # 绑定ip和端口
    s.listen(int(listen_number)) # 等待客户端连接
    msg_server_run = True
    return True

def run(tk_setup):
    global s
    global msg_server_run
    global command_run
    if not tk_setup:
        print('server setup !!!')
    else:
        print('server run !!!')
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
                    server_path = data['server_path']
                    command_run = data['command_run']

                    if msg_instructions == 'stop server' and receive_ip == 'server': # 停止服务器
                        msg_server_run = False
                        msg_data = {'send_ip':'server','receive_ip':'everyone','msg':'the server is about to stop','system':'server system','instructions':'the server requests the user to exit','command':None,'command_run':None}
                        print('{} request server stop'.format(send_ip))
                        c.send(str(msg_data).encode('utf-8'))
                    elif msg_instructions == 'user exit' and receive_ip == 'server': # 用户退出
                        msg_data = {'send_ip':'server','receive_ip':'everyone','msg':send_ip + '已退出服务器','system':'server system','instructions':'msg','command':None,'command_run':None}
                        print('{} request to exit the server'.format(send_ip))
                        c.send(str(msg_data).encode('utf-8'))
                    elif msg_instructions == 'cmd' and receive_ip == 'server': # 打开命令
                        msg_data = {'send_ip':'server','receive_ip':'everyone','msg':send_ip + '已开启命令行','system':'server system','instructions':'msg','command':None,'command_run':None}
                        print('{} open command line'.format(send_ip))
                        c.send(str(msg_data).encode('utf-8'))
                    elif msg_instructions == 'stop cmd' and receive_ip == 'server': # 关闭命令
                        msg_data = {'send_ip':'server','receive_ip':'everyone','msg':send_ip + '已关闭命令行','system':'server system','instructions':'msg','command':None,'command_run':None}
                        print('{} close command line'.format(send_ip))
                        c.send(str(msg_data).encode('utf-8'))
                    elif msg_instructions == 'command':
                        if command == 'close': # 执行命令者
                            msg_data = {'send_ip':send_ip,'receive_ip':receive_ip,'msg':send_ip + ' 没有开启命令行','system':system,'instructions':'command','command':'close','command_run':None}
                            print('{} wants {} to execute the command {}, but {} does not open the command line'.format(send_ip,receive_ip,command,send_ip))
                            c.send(str(msg_data).encode('utf-8'))
                        elif 'ok' == command: # 执行命令者
                            print('{} wants {} to execute the command {}, {} say "ok" ... {}'.format(receive_ip,send_ip,command,send_ip,command_run))
                            msg_data = {'send_ip':send_ip,'receive_ip':receive_ip,'msg':send_ip + ' 命令执行成功','system':system,'instructions':'command','command':'ok','command_run':command_run}
                            c.send(str(msg_data).encode('utf-8'))
                        elif command or command == None: # 发送命令者
                            msg_data = {'send_ip':send_ip,'receive_ip':receive_ip,'msg':send_ip + ' 没有键入命令','system':system,'instructions':'command','command':'no','command_run':None}
                            print('{} no output command'.format(send_ip))
                            c.send(str(msg_data).encode('utf-8'))
                        elif command == 'error': # 执行命令者
                            msg_data = {'send_ip':send_ip,'receive_ip':receive_ip,'msg':send_ip + ' 执行命令时错误','system':system,'instructions':'command','command':'error','command_run':None}
                            print('{} error executing command'.format(send_ip))
                            c.send(str(msg_data).encode('utf-8'))
                        elif not (command or command == None): # 发送命令者
                            msg_data = {'send_ip':send_ip,'receive_ip':receive_ip,'msg':'','system':system,'instructions':'command','command':'.','command_run':command_run}
                            print('{} wants {} to execute the command {}'.format(receive_ip,send_ip,command))
                            c.send(str(msg_data).encode('utf-8'))
                    elif msg_instructions == '_ftp' and receive_ip == 'server': # servre开启ftp
                        global intranet_ip
                        print(server_path)
                        from random import randint
                        from uap import user
                        from uap import password
                        u = user(4)
                        p = password(9)
                        po = randint(3000,8000)
                        msg_data = {'send_ip':'server','receive_ip':send_ip,'msg':'ftp://{}:{}   user : {}   password : {}'.format(intranet_ip,po,u,p),'system':system,'instructions':'msg','command':None,'command_run':None}
                        print('{} ... ftp://{}:{}  user : {}  password : {}'.format(send_ip,intranet_ip,po,u,p))
                        c.send(str(msg_data).encode('utf-8'))
                        t1 = threading.Thread(target=start_ftp_server, args=(intranet_ip,po,u,p,server_path,))
                        t1.start()
                    elif msg_instructions == 'msg': # 发送消息
                        msg_data = {'send_ip':send_ip,'receive_ip':receive_ip,'msg':msg,'system':system,'instructions':'msg','command':None,'command_run':None}
                        print(msg_data)
                        print('{} to {} : {}'.format(send_ip,receive_ip,msg))
                        c.send(str(msg_data).encode('utf-8'))
                    elif msg_instructions == 'msg' and receive_ip == 'server':
                        print('{} to server : {}'.format(send_ip,msg))
                except Exception as e:
                    print(repr(e))
                    #print(repr(e)) # 输出错误信息
                    #print(str(e)) # 输出错误信息
                    break
