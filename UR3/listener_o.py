# -*- coding: utf-8 -*-
"""
Created on Fri Jun 19 15:50:37 2020

@author: Juan
"""

import socket
import sys

HOST = '192.168.0.108'	# Symbolic name meaning all available interfaces
PORT = 8888	# Arbitrary non-privileged port

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print('Socket created')

try:
	s.bind((HOST, PORT))
except socket.error as err:
	print('Bind failed. Error Code : ' + str(err))
	sys.exit()
	
print("Socket bind complete")

s.listen(10)
print("Socket now listening")

#wait to accept a connection - blocking call
conn, addr = s.accept()

#display client information
print( 'Connected with ' + addr[0] + ':' + str(addr[1]))