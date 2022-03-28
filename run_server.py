import s
host,port,listen_number='192.168.31.110',3030,5
s.log.log_setup_msg(host,port,listen_number)
s.server.server_setup(host,port,listen_number)
s.server.server_run()