import socket
import sys

HOST = "192.168.0.31"     # IP/domain to bind
PORT = 50007
s = None

try:
	#					IPv4             stream socket      tcp protocol
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)
	# given that the socket type is a stream, there is no need to specify the protocol*
except OSError as msg:
	s = None	
try:
	s.bind((HOST,PORT))
	s.listen(1)
except OSError as msg:
	s.close()
	s = None

if s is None:
    print('could not open socket')
    sys.exit(1)

conn, addr = s.accept()
with conn:
    print('Connected by', addr)
    while True:
        data = conn.recv(1024)
        if not data: break
        conn.send(data)