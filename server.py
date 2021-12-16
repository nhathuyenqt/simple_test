import sys,os,socket
import tqdm

BUFFER_SIZE = 4096
SEPARATOR = "<SEPARATOR>"

address_host = 'localhost'
numero_port = 6688
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)
client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
client_socket.bind((address_host, numero_port))
client_socket.listen(socket.SOMAXCONN)

while 1:
	(new_connection, address) = client_socket.accept()
	print ("new connection depuis ", address)
	new_connection.sendall(b'Bienvenu\n')
	pid = os.fork()
	if (pid) :
		received = client_socket.recv(BUFFER_SIZE).decode()
		filename, filesize = received.split(SEPARATOR)
		print("receiving file ", filename, " with size ",filesize)
		filename = os.path.basename(filename)
		filesize = int(filesize)
		progress = tqdm.tqdm(range(filesize), f"Receiving {filename}", unit="B", unit_scale=True, unit_divisor=1024)
		with open(filename, "wb") as f:
		    while True:
		        # read 1024 bytes from the socket (receive)
		        bytes_read = client_socket.recv(BUFFER_SIZE)
		        if not bytes_read:    
		            # nothing is received
		            # file transmitting is done
		            break
		        # write to the file the bytes we just received
		        f.write(bytes_read)
		        # update the progress bar
		        progress.update(len(bytes_read))
		# while 1:
		# 	ligne = new_connection.recv(1000)
		# 	print ("<:", str(ligne,encoding='UTF-8'))
		# 	if not ligne: break
	else:
		while 1:
			clavier = input(':>')
			if not clavier: break
			new_connection.sendall(bytes(clavier, encoding='UTF-8'))
	new_connection.close()
client_socket.close()