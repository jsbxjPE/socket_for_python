import tkinter
import tkinter.messagebox
import time

def server_setup_ok():
    host = server_host.get()
    port = server_port.get()
    listen_number = server_number.get()
    try:
        import server
        if server.setup(host,port,listen_number):
            tkinter.messagebox.showinfo(title = 'server setup info', message = 'setup ok !!!')
            server_exit.destroy()
            server_run.destroy()
            server_run_ma = tkinter.Button(server_tk, text=" run ", width=30, height=2, command = server_run_ok)
            server_run_ma.pack(side=tkinter.RIGHT)
            server_setup.destroy()
            server_setup_yes = tkinter.Button(server_tk, text="setup", width=30, height=2, state = tkinter.DISABLED)
            server_setup_yes.pack(side=tkinter.LEFT)
        else:
            tkinter.messagebox.showerror(title = 'server setup error', message = 'host or port or linsten_number error')
    except:
        tkinter.messagebox.showerror(title = 'server setup error', message = 'host or port or linsten_number error')

def server_run_ok():
    tkinter.messagebox.showinfo(title = 'server run info', message = 'run ok !!!')
    server_run.destroy()
    server_run_yes = tkinter.Button(server_tk, text=" run ", width=30, height=2, state = tkinter.DISABLED)
    server_run_yes.pack(side=tkinter.LEFT)
    server_tk.quit()
    return True

def server_exit_ok():
    server_tk.quit()
    return False

server_tk = tkinter.Tk()

server_tk.title('server')
server_tk.geometry('775x350')

server_msg = tkinter.Label(server_tk, text="server")
server_msg.pack()
server_ln = tkinter.Label(server_tk, text="\n")
server_ln.pack()

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

server_setup = tkinter.Button(server_tk, text="setup", width=30, height=2, command = server_setup_ok)
server_setup.pack(side=tkinter.LEFT)
server_exit = tkinter.Button(server_tk, text=" quit ", width=30, height=2, command = server_exit_ok)
server_exit.pack(side=tkinter.RIGHT)
server_run = tkinter.Button(server_tk, text=" run ", width=30, height=2, state = tkinter.DISABLED, command = server_run_ok)
server_run.pack(side=tkinter.RIGHT)

server_tk.mainloop()