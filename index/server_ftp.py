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