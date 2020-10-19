# Echo client program
import socket
import sys

HOST = "192.168.0.31"     # The remote host
PORT = 50007              # The same port as used by the server
if len(sys.argv) == 3:
    HOST = sys.argv[1]
    PORT = int(sys.argv[2])
elif len(sys.argv) == 2:
    PORT = int(sys.argv[1])
s = None
try:
    #					IPv4             stream socket      tcp protocol
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)
	# given that the socket type is a stream, there is no need to specify the protocol*
except OSError as msg:
    s = None
try:
    s.connect((HOST,PORT))
except OSError as msg:
    s.close()
    s = None
if s is None:
    print('could not open socket')
    sys.exit(1)
with s:
    s.sendall(b'End')
    data = s.recv(1024)
print('Received', repr(data))
s.close()