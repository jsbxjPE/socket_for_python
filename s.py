from re import S
import socket
import sys

global msg_server_run
global log_name
global file_name
global log_name_debug
global log_mode
global s
global img_name

msg_server_run = True
log_mode = False

# 日志
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

# 消息指令
class instructions():
    def stop_server(data,a_ip):
        global log_mode
        global msg_server_run
        print('{} stop server'.format(a_ip))
        if log_mode:
            log.log_info_msg(data)
            log.log_info_msg('{} stop server'.format(a_ip))
        stop = False
        sys.exit('{} stop server'.format(a_ip))
    def start_cmd(data,a_ip,c):
        global log_mode
        c.send('\n{} start cmd for {}'.format(a_ip,data.split('/*operating system*/')[1]).encode('utf-8'))
        c.send('\n{}|||{}|||{}'.format('msg_server',a_ip,data.split('/*operating system*/')[1]).encode('utf-8'))
        print('\n{} start cmd for {}'.format(a_ip,data.split('/*operating system*/')[1]))
        if log_mode:
            log.log_info_msg(data)
            log.log_info_msg('{} start cmd for {}'.format(a_ip,data.split('/*operating system*/')[1]))
    def not_cmd(data,a_ip,c):
        global log_mode
        c.send('{} stop cmd for {}'.format(a_ip,data.split('/*operating system*/')[1]).encode('utf-8'))
        c.send('{}|||{}|||{}'.format('msg_server',a_ip,data.split('/*operating system*/')[1]).encode('utf-8'))
        print('{} stop cmd for {}'.format(a_ip,data.split('/*operating system*/')[1]))
        if log_mode:
            log.log_info_msg(data)
            log.log_info_msg('{} stop cmd for {}'.format(a_ip,data.split('/*operating system*/')[1]))
    def user_exit(data,a_ip,c):
        global log_mode
        c.send('{} exit'.format(a_ip).encode('utf-8'))
        print('{} exit'.format(a_ip))
        if log_mode:
            log.log_info_msg(data)
            log.log_info_msg('{} exit'.format(a_ip))
    def run_cmd_instructions(data,a_ip,b_ip,c,msg):
        global log_mode
        msgdata = ('{}|||{}|||{} '.format(a_ip, b_ip, msg)).encode('utf-8')
        print('{}让{}执行 : {}'.format(a_ip,b_ip,msg.split('/*run*/')[1]))
        c.send(msgdata)
        if log_mode:
            log.log_info_msg(data)
            log.log_info_msg('{}让{}执行 : {}'.format(a_ip,b_ip,msg.split('/*run*/')[1]))
    def msg_to_msg(data,a_ip,b_ip,c,msg):
        global log_mode
        msgdata = ('{}|||{}|||{} '.format(a_ip, b_ip, msg)).encode('utf-8')
        print('{}向{}发送 : {}'.format(a_ip,b_ip,msg))
        c.send(msgdata)
        if log_mode:
            log.log_info_msg(data)
            log.log_info_msg('{}向{}发送 : {}'.format(a_ip,b_ip,msg))
    def file_download(a_ip,b_ip,c,msg):
        global log_mode
        global file_name
        file_name = msg.split('/*download*/')[1]
        print(msg)
        msgdata = ('{}|||{}|||{} '.format(a_ip, b_ip, msg)).encode('utf-8')
        print('{}请求下载{}路径 "{}" 的数据'.format(a_ip,b_ip,file_name))
        c.send(msgdata)
        if log_mode:
            log.log_info_msg(msg)
            log.log_info_msg('{}请求下载{}路径 "{}" 的数据'.format(a_ip,b_ip,file_name))
    def file_transmission_server(a_ip,b_ip,c,msg):
        global log_mode
        global file_name
        msgdata = ('{}|||{}|||{} '.format(a_ip, b_ip, msg)).encode('utf-8')
        c.send(msgdata)
        if log_mode:
            log.log_info_msg(msg)
            log.log_info_msg('{}发送数据"{}"给{}'.format(a_ip,msg.split('/*file*/')[1],b_ip))
    #def screen(a_ip,b_ip,msg,c):
    #    global s
    #    print('{}想要截取{}的屏幕'.format(a_ip,b_ip))
    #    msgdata = ('{}|||{}|||{} '.format(a_ip, b_ip, msg)).encode('utf-8')
    #    print(msgdata)
    #    c.send(msgdata)
    #    log.log_info_msg(msg)
    #    log.log_info_msg('{}想要截取{}的屏幕'.format(a_ip,b_ip))

# 服务器    
class server():
    def server_setup(host,port,listen_number):
        global s
        s = socket.socket()
        s.bind((str(host), int(port))) # 绑定ip和端口
        s.listen(listen_number) # 等待客户端连接
    def server_run():
        global msg_server_run
        global file_name
        global log_mode
        print('run server !!!')
        while msg_server_run:
            c, addr = s.accept() # 建立客户端连接
            print(c)
            if log_mode:
                log.log_info_msg(str(c))
            while msg_server_run:
                try:
                    data = c.recv(8192).decode() # 接收客户端信息
                    a_ip, b_ip = data.split('/*ip*/')[0], data.split('/*ip*/')[1] # 通过分割获取发送者ip和接收者ip分别赋值给a_ip和b_ip   (String)
                    msg = data.split("/*ip*/")[2]
                    if data == '':
                        break
                    elif '/*stop server*/' == msg:
                        msg_server_run = False
                        instructions.stop_server(data,a_ip)
                    elif '/*cmd*/' == msg:
                        instructions.start_cmd(data,a_ip,c)
                    elif '/*not cmd*/' == msg:
                        instructions.not_cmd(data,a_ip,c)
                    elif '/*exit*/' == msg:
                        instructions.user_exit(data,a_ip,c)
                    elif '/*run*/' in msg:
                        instructions.run_cmd_instructions(data,a_ip,b_ip,c,msg)
                    elif '/*download*/' in msg:
                        instructions.file_download(a_ip,b_ip,c,msg)
                    elif '/*file*/' in msg:
                        instructions.file_transmission_server(a_ip,b_ip,c,msg)
                    #elif '/*screen*/' == msg:
                    #    instructions.screen(a_ip,b_ip,msg,c)
                    else:
                        instructions.msg_to_msg(data,a_ip,b_ip,c,msg)
                except Exception as e:
                    if log_mode:
                         log.log_debug_server(repr(e))
                    break

'''
导入s.py文件函数
import s

如果要使用log,则:
s.log.log_setup_msg(host,port,listen_number) # host {String},port {Int},listen_number {Int}
不要则不执行

如果要打开服务器,则:
s.server.server_setup(host,port,listen_number) # host {String},port {Int},listen_number {Int}
s.server.server_run()
不要则不执行

服务器日志存储在./server_log文件夹下
'''