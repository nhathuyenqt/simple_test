import os,socket,sys
import tqdm

SEPARATOR = "<SEPARATOR>"
BUFFER_SIZE = 4096 
filename = "garbled-euclidean.txt"
filesize = os.path.getsize(filename)

address_server = 'localhost'
numero_port = 6688
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try: s.connect((address_server, numero_port))
except:
	print ("problem of connection")
	sys.exit(1)
pid = os.fork()


if (pid) :
	s.sendall(f"{filename}{SEPARATOR}{filesize}".encode())
	progress = tqdm.tqdm(range(filesize), f"Sending {filename}", unit="B", unit_scale=True, unit_divisor=1024)
	while 1:
		bytes_read = f.read(BUFFER_SIZE)
		if not bytes_read:
            # file transmitting is done
			break
		s.sendall(bytes_read)
		progress.update(len(bytes_read))
		# coming_msg = my_socket.recv(1000)
		# print (str(coming_msg,encoding='UTF-8'))
		# if not coming_msg: break
else:
	while 1:
		msg = input(':>')
		if not msg: break
		my_socket.sendall(bytes(msg+'\n',encoding='UTF-8'))
my_socket.close()