import socket
import sys
import ast

global log_name
global log_name_debug
global log_mode
global msg_server_run
global s

msg_server_run = False
log_mode = False

class log():
    def log_setup_msg(host,port,listen_number):
        global log_name
        global log_name_debug
        global log_mode
        import time
        localtime = time.asctime(time.localtime(time.time()))
        log_name = str('./server_log/{}.log'.format(str(localtime))).replace(':','-')
        log_name_debug = str('./server_log/{} debug.log'.format(str(localtime))).replace(':','-')
        print('log path : {}'.format(log_name))
        print('log path : {}'.format(log_name_debug))
        with open(log_name,'a') as log_msg:
            log_msg.write('log:')
            log_msg.write('\n')
            log_msg.write(str(localtime))
            log_msg.write('start server for host:{} port:{} listen_number:{}'.format(host,port,listen_number))
            log_msg.write('\n')
        with open(log_name_debug,'a') as log_msg:
            log_msg.write('debug log:')
            log_msg.write('\n')
            log_msg.write(str(localtime))
            log_msg.write('start server for host:{} port:{} listen_number:{}'.format(host,port,listen_number))
            log_msg.write('\n')
        log_mode = True
    def log_info_msg(data):
        global log_name
        import time
        localtime = time.asctime(time.localtime(time.time()))
        with open(log_name,'a') as log_msg:
            log_msg.write(str(localtime))
            log_msg.write(' : \n')
            log_msg.write('[INFO] ')
            log_msg.write(data)
            log_msg.write('\n\n')
    def log_debug_server(bug_msg):
        global log_name_debug
        import time
        localtime = str(time.asctime(time.localtime(time.time())))
        with open(log_name_debug,'a') as log_msg:
            log_msg.write(str(localtime))
            log_msg.write(' : \n')
            log_msg.write('[DEBUG] ')
            log_msg.write(bug_msg)
            log_msg.write('\n\n')

class instructions():
    def stop_server(data,a_ip):
        global log_mode
        global msg_server_run
        print('{} stop server'.format(a_ip))
        if log_mode:
            log.log_info_msg(data)
            log.log_info_msg('{} stop server'.format(a_ip))
    def start_cmd(c,data,a_ip,operating_system):
        global log_mode
        c.send('\n{} start cmd for {}'.format(a_ip,operating_system).encode('utf-8'))
        print('\n{} start cmd for {}'.format(a_ip,operating_system))
        if log_mode:
            log.log_info_msg(data)
            log.log_info_msg('{} start cmd for {}'.format(a_ip,operating_system))
    def stop_cmd(c,data,a_ip,operating_system):
        global log_mode
        c.send('{} stop cmd for {}'.format(a_ip,operating_system).encode('utf-8'))
        c.send('{}|||{}|||{}'.format('msg_server',a_ip,operating_system).encode('utf-8'))
        print('{} stop cmd for {}'.format(a_ip,operating_system))
        if log_mode:
            log.log_info_msg(data)
            log.log_info_msg('{} stop cmd for {}'.format(a_ip,operating_system))
    def user_exit(data,a_ip,c):
        global log_mode
        c.send('{} exit'.format(a_ip).encode('utf-8'))
        print('{} exit'.format(a_ip))
        if log_mode:
            log.log_info_msg(data)
            log.log_info_msg('{} exit'.format(a_ip))
    def run_cmd_instructions(data,a_ip,b_ip,c,run_msg):
        global log_mode
        msgdata = ('{}|||{}|||{} '.format(a_ip, b_ip, '/*run*/{}'.format(run_msg))).encode('utf-8')
        print('{}让{}执行 : {}'.format(a_ip,b_ip,run_msg))
        c.send(msgdata)
        if log_mode:
            log.log_info_msg(data)
            log.log_info_msg('{}让{}执行 : {}'.format(a_ip,b_ip,run_msg))
    def msg_to_msg(data,a_ip,b_ip,c,msg):
        global log_mode
        msgdata = ('{}|||{}|||{} '.format(a_ip, b_ip, msg)).encode('utf-8')
        print('{}向{}发送 : {}'.format(a_ip,b_ip,msg))
        c.send(msgdata)
        if log_mode:
            log.log_info_msg(data)
            log.log_info_msg('{}向{}发送 : {}'.format(a_ip,b_ip,msg))

class server():
    def server_setup(host,port,listen_number):
        global s
        s = socket.socket()
        s.bind((str(host), int(port))) # 绑定ip和端口
        s.listen(listen_number) # 等待客户端连接
    def server_run():
        global s
        global msg_server_run
        global log_mode
        msg_server_run = True
        print('run server !!!')
        while msg_server_run:
            c, addr = s.accept() # 建立客户端连接
            print(c)
            if log_mode:
                log.log_info_msg(str(c))
            while msg_server_run:
                try:
                    data = ast.literal_eval(c.recv(8192).decode()) # 接收客户端信息
                    a_ip, b_ip = data['a_ip'], data['b_ip'] # 通过分割获取发送者ip和接收者ip分别赋值给a_ip和b_ip   (String)
                    msg = data['msg']
                    msg_instructions = data['instructions']
                    operating_system = data('operating_system')
                    if data == '':
                        break
                    elif msg_instructions == 'stop_server':
                        msg_server_run = False
                        instructions.stop_server(data,a_ip)
                    elif msg_instructions == 'cmd':
                        instructions.start_cmd(c,data,a_ip,operating_system)
                    elif msg_instructions == 'not_cmd':
                        instructions.stop_cmd(c,data,a_ip,operating_system)
                    elif msg_instructions == 'user_exit':
                        instructions.user_exit(data,a_ip,c)
                    elif msg_instructions == 'run_cmd':
                        run_msg = data['run_cmd']
                        instructions.run_cmd_instructions(data,a_ip,b_ip,c,run_msg)
                    else:
                        instructions.msg_to_msg(data,a_ip,b_ip,c,msg)
                except Exception as e:
                    if log_mode:
                         log.log_debug_server(repr(e))
                    break