import socket                   # Import socket module
				   # Reserve a port for your service.


while True:

	s = socket.socket()
	udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)             # Create a socket object
	host = socket.gethostname()     # Get local machine name
	port = 6009
	port2 = 2009
	s.connect((host, port))
	g=raw_input(">> ")
	s.send(g)

	with open("history_client", 'a') as f:
		f.write(g)
		f.write('\n')
	f.close()


	if g =='exit':
		s.close()
		break
	if "FileDownload" in g:
		fil = g.split()
		ans = s.recv(1024)
		print ans

		if not 'ERROR' in ans:
			if fil[2] == 'TCP':
			
				with open('tmp'+fil[1], 'wb') as f:
					print 'Downloaded'
					while True:
						data = s.recv(1024)
						if not data:
							break
						f.write(data)
				f.close()

			elif fil[2]== 'UDP' :
				udp.sendto("connect", (host, port2))

				with open('tmp'+fil[1], 'wb') as f:
					print 'Downloaded'
					while True:
						data, x = udp.recvfrom(1024)
						if data == "END":
							break
						f.write(data)
				f.close()

		

	else:
		while True:
				
				ans = s.recv(1024)
				print ans
				if not ans:
					break
	s.close()		


