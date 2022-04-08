# 即时通讯软件

## start(开始)

```sh
python pip_install.py
```
```sh
python3 pip_install.py
```

### server(服务器端)

## 导入server文件

```python
import server
```

## server.setup (服务器端初始化)

```python
server.setup('host',port,number)
```

### setup参数介绍

host是server(服务器端)的IP地址  {Str}
port是server(服务器端)的端口  {Int}
number是server(服务器端)的客户端最大连接数  {Int}

## server.run (运行服务器)

```python
server.run(1)
```

### run函数中 servre(服务器端)一直接收客户端的消息

server接收的信息要转化成字典,使用 ast.literal_eval() 转化成字典

### 以字典得出

send_ip是字典的send_ip
receive_ip是字典的receive_ip
msg是字典的msg
system是字典的system
msg_instructions是字典的instructions
command是字典的command
server_path是字典的server_path
command_run是字典的command_run

### 当msg_instructions是

stop server (且接收人是server   停止服务器)
user exit (且接收人是server   用户退出)
cmd (且接收人是server   开启命令行)
stop cmd (且接收人是server   关闭命令行)
_ ftp (且接收人是server   通过ftp协议,开启server_path的ftp)
msg   (发送消息给指定用户(receive_ip)说是他(send_ip)发的)

|          接           |
|          下           |
|          面           |
|          话           |

### 当msg_instructions是command,则当command是

close   指定用户没有开启命令行
ok   指定用户命令执行成功
error   指定用户命令执行错误

### client(客户端)

## 导入client文件

```python
import client
```

## client.setup (客户端初始化)

```python
client.setup('host',port)
```

### setup参数介绍

host是server(服务器端)的IP地址  {Str}
port是server(服务器端)的端口  {Int}


## client.run (运行客户端)

```python
client.run()
```

## input输入

/server_stop (停止服务器)
/exit (用户退出)
/rcmd (开启命令行)
/scmd (关闭命令行)
/run {xxx} (指定用户执行基础的命令)(只有开启命令行时才行)
/ftp_server {./ or / or c:\ or xxx ...} (通过ftp协议,开启server端路径的ftp)
以上都不是则直接发送信息

## 接收服务器端消息
通过服务器端消息来执行命令或输出消息

# over
