import socket                   # Import socket module
import time 
import sys
import subprocess
import os

port = 6009
port2 = 2009          # Reserve a port for your service.
s = socket.socket()             # Create a socket object
host = socket.gethostname()     # Get local machine name
s.bind((host, port))            # Bind to the port
s.listen(5)    

udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp.bind((host, port2))

while True:
	conn, addr = s.accept()     # Establish connection with client.
	arg = conn.recv(1024)
	with open("history_server", 'a') as f:
		f.write(arg)
		f.write('\n')
	f.close()
	
	if  "IndexGet shortlist" in arg:
		m=arg.split( )
		if(len(m) != 4 or len(m[2]) != 13 or len(m[3]) != 13 or m[2][8]!= 'T' or m[3][8] != 'T' ):

			Error = "ERROR:In giving arguments \nFormat: IndexGet shortlist <starttime>YYYYMMDDTHHMM <endtime>YYYYMMDDTHHMM"
			conn.send(Error)

		else:
			bashcomm = "find . -newermt "+m[2]+" -not  -newermt "+m[3]
			proce=subprocess.Popen(bashcomm.split(),stdout=subprocess.PIPE)
			op=proce.communicate()[0]
			conn.send(op)

	elif  arg =="IndexGet longlist" :
		bashcomm = "ls -l"
		proce=subprocess.Popen(bashcomm.split(),stdout=subprocess.PIPE)
		op=proce.communicate()[0]
		conn.send(op)
	elif "IndexGet regex" in arg :
		m = arg.split( )
		if len(m) != 3 :
			Error = "ERROR:In giving arguments \nFormat: IndexGet regex <regexarg>"
			conn.send(Error)
		else: 
			
			proce=subprocess.Popen("find . -regex '" + m[2] + "'", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
			op=proce.communicate()[0]
			conn.send(op)
	elif "FileHash verify" in arg:
		m=arg.split( )
		if len(m) != 3 :
			Error = "ERROR:In giving arguments \nFormat: FileHash verify <file_name>"
			conn.send(Error)
		elif not  os.path.isfile('./'+m[2])  :
			Error = "ERROR:File name does not exist"
			conn.send(Error)
		else: 
			bashcomm = "md5sum"+" "+m[2]
			proce=subprocess.Popen(bashcomm.split(),stdout=subprocess.PIPE)
			op1=proce.communicate()[0]
			bashcomm = "stat "+m[2]
			proce=subprocess.Popen(bashcomm.split(),stdout=subprocess.PIPE)
			opf=proce.communicate()[0]
			op2 = opf.split()
			op1=op1.strip('\n')
			op = op1+"\t"+op2[-8]
			conn.send(op)
	elif  arg=="FileHash checkall":
		bashcomm = "ls"
		proce=subprocess.Popen(bashcomm.split(),stdout=subprocess.PIPE)
		op=proce.communicate()[0]
		opl = op.split()
		for f in opl:
			bashcomm = "md5sum"+" "+f
			proce=subprocess.Popen(bashcomm.split(),stdout=subprocess.PIPE)
			op1=proce.communicate()[0]
			op1=op1.strip('\n')
			bashcomm = "stat "+f
			proce=subprocess.Popen(bashcomm.split(),stdout=subprocess.PIPE)
			opf=proce.communicate()[0]
			op2 = opf.split()
			opans = op1+"\t"+op2[-8]
			conn.send(opans)

	elif "FileDownload" in arg:
		if '"' in arg:
			cote = arg.split('"')
			m = cote[0].split()
			m.append(cote[1])
			cot=cote[2][1:]
			m.append(cot)


		else:
			m=arg.split()

		print m
		print m[2]

		if len(m) != 3 :
			Error = "ERROR:In giving arguments \nFormat: FileDownload <file_name> <TCP/UDP>"
			conn.send(Error)
		
		elif m[2] != 'TCP'  and m[2] != 'UDP':
			print "ok"
			Error = "ERROR:In giving arguments \nFormat: FileDownload <file_name> <TCP/UDP>"
			conn.send(Error)
		
		elif not os.path.isfile('./'+m[1]) :
			Error = "ERROR:File name does not exist"
			conn.send(Error)
 

		else:
			filename= m[1]

			bashcomm = "md5sum"+" "+m[1]
			proce=subprocess.Popen(bashcomm.split(),stdout=subprocess.PIPE)
			op1=proce.communicate()[0]
			bashcomm = "stat "+m[1]
			proce=subprocess.Popen(bashcomm.split(),stdout=subprocess.PIPE)
			opf=proce.communicate()[0]
			op2 = opf.split()
			op1=op1.strip('\n')
			op = op1+"\t"+op2[3]+"\t"+op2[-8]
			conn.send(op)

			if m[2] == 'TCP':
				f = open(filename,'rb')
				l = f.read(1024)
				while (l):
				   conn.send(l)
				   l = f.read(1024)
				f.close()
			elif m[2] == 'UDP':
				data, addr = udp.recvfrom(1024)
				print data
				f = open(filename,'rb')
				l = f.read(1024)
				while (l):
					udp.sendto(l, addr)
					l = f.read(1024)
				f.close()
				end = "END"
				udp.sendto(end,addr)
			print "filesent"

	else:
		err = "ERROR:Give the suitable arguments \n[FileDownload <filename> <TCP/UDP> ,FileHash <arg2>, IndexGet <arg1> ;\n{arg1|shortlist,longlist,regex} {arg2|verify,checkall}]"
		conn.send(err)


	conn.close()
		
		
			

	
		
		
		
		
	
		

		
	    
		
		
	
				
    
	   