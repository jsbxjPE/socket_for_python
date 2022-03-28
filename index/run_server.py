import s
host,port,listen_number='127.0.0.1',3030,5
s.log.log_setup_msg(host,port,listen_number)
s.server.server_setup(host,port,listen_number)
s.server.server_run()