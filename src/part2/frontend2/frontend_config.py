process_id = 2 # client starts from 3. 1, and 2 are frontend servers

cluster_info = {
        '1':('127.0.0.1', 8005,),
        '2':('127.0.0.1', 8006,),

        '3':('127.0.0.1', 8100,),
		'4':('127.0.0.1', 8101,),
		'5':('127.0.0.1', 8102,),
		'6':('127.0.0.1', 8103,)
		}

server_ip = '127.0.0.1'
server_port = 8000

win_per_num_request = 100
