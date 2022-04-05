import tkinter
import tkinter.messagebox
import os
import threading
from unicodedata import name
import uuid
import socket

global server_run_ma
global server_exit_ma
global servername
global host
global port
global tk_setup

def server_setup_ok():
    global server_tk
    global server_host
    global server_port
    global server_number
    global server_setup
    global server_exit
    global server_run
    global server_run_ma
    global server_exit_ma
    global host
    global port
    global servername
    global tk_setup
    servername = server_name.get()
    host = server_host.get()
    port = server_port.get()
    listen_number = server_number.get()
    print([servername,host,port,listen_number])
    try:
        import server
        if '7794' == port:
            tkinter.messagebox.showinfo(title = 'server setup error', message = 'port error !!!')
        elif server.setup(host,port,listen_number):
            tkinter.messagebox.showinfo(title = 'server setup info', message = 'setup ok !!!')
            server_setup.destroy()
            server_setup_yes = tkinter.Button(server_tk, text="setup", width=20, height=2, state = tkinter.DISABLED)
            server_setup_yes.pack()
            server_run.destroy()
            server_run_ma = tkinter.Button(server_tk, text=" run ", width=20, height=2, command = server_run_ok)
            server_run_ma.pack()
            server_exit.destroy()
            server_exit_ma = tkinter.Button(server_tk, text=" quit ", width=20, height=2, command = server_exit_ok)
            server_exit_ma.pack()
            tk_setup = True
        else:
            tkinter.messagebox.showerror(title = 'server setup error', message = 'host or port or linsten_number error')
    except Exception as e:
        print(str(e))
        tkinter.messagebox.showerror(title = 'server setup error', message = 'host or port or linsten_number error')

def server_run_tk(tk_setup):
    import server
    server.run(tk_setup)

"""
def server_run_join(sahi,servername,host,port,server_host):
    print('server join ...')
    c = socket.socket()
    c.connect((server_host, 7749))
    print(c)
    uid = hash(uuid.uuid5(uuid.NAMESPACE_DNS,"{}".format(hash(sahi))))
    print(uid)
    msg = str({'join':True,'uuid':uid,'name':servername,'host':host,'port':port})
    print(msg)
    c.send(msg.encode('utf-8'))
"""

"""
def server_exit_tk(exit):
    print('server exit tk start ...')
    root = tkinter.Tk()
    root.title('server quit')
    root_exit = tkinter.Button(root, text=exit, width=20, height=2, command = server_exit_tk)
    root_exit.pack()
    root.mainloop()
def server_exit_tk():
    sys.exit('quit for tk')
"""

def server_run_ok():
    global server_run_ma
    global server_exit_ma
    global host
    global port
    global tk_setup
    global servername
    server_run_ma.destroy()
    server_run_yes = tkinter.Button(server_tk, text=" run ", width=20, height=2, state = tkinter.DISABLED)
    server_run_yes.pack()
    server_exit_ma.destroy()
    server_exit_yes = tkinter.Button(server_tk, text=" quit ", width=20, height=2, command = server_exit_ok)
    server_exit_yes.pack()
    tkinter.messagebox.showinfo(title = 'server run info', message = 'run ok !!!')
    sahi = 'DSaj3#@$RTHuiyu32dFG4@#$@eiuSDFRqydgiu#$?>DG<"Fger]fd[fdGR}dfg{r"Srt23rggrerG'
    server_host = '192.168.43.174'
    t1 = threading.Thread(target=server_run_tk, args=(tk_setup,))
    #t2 = threading.Thread(target=server_run_join, args=(sahi,servername,host,port,server_host,))
    #t3 = threading.Thread(target=server_exit_tk, args=('exit',))
    #t2.start()
    #t3.start()
    t1.start()

def server_exit_ok():
    os._exit(0)

server_tk = tkinter.Tk()

server_tk.title('server')
server_tk.geometry('240x390')
server_msg = tkinter.Label(server_tk, text="server")
server_msg.pack()
server_ln = tkinter.Label(server_tk, text="")
server_ln.pack()

server_lname = tkinter.Label(server_tk, text="name:")
server_lname.pack()
server_name = tkinter.Entry(server_tk, show=None, font=('Arial', 14))
server_name.pack()

server_lhost = tkinter.Label(server_tk, text="host:")
server_lhost.pack()
server_host = tkinter.Entry(server_tk, show=None, font=('Arial', 14))
server_host.pack()

server_lport = tkinter.Label(server_tk, text="port:")
server_lport.pack()
server_port = tkinter.Entry(server_tk, show=None, font=('Arial', 14))
server_port.pack()

server_lnum = tkinter.Label(server_tk, text="listen number:")
server_lnum.pack()
server_number = tkinter.Entry(server_tk, show=None, font=('Arial', 14))
server_number.pack()

server_setup = tkinter.Button(server_tk, text="setup", width=20, height=2, command = server_setup_ok)
server_setup.pack()
server_run = tkinter.Button(server_tk, text=" run ", width=20, height=2, state = tkinter.DISABLED, command = server_run_ok)
server_run.pack()
server_exit = tkinter.Button(server_tk, text=" quit ", width=20, height=2, command = server_exit_ok)
server_exit.pack()

server_tk.mainloop()
