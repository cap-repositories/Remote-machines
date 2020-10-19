# -*- coding: utf-8 -*-
"""
Created on Mon Oct 21 13:35:04 2019

@author: jamuj
"""

# Echo client program
import socket
import time
import struct
import codecs
HOST = "192.168.15.15" # The remote host
PORT_30003 = 30003

#print "Starting Program"

count = 0
home_status = 0
program_run = 0

while (True):
     if program_run == 0:
         try:
             s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
             s.settimeout(10)
             s.connect((HOST, PORT_30003))
             time.sleep(1.00)
             #print ""
             packet_1 = s.recv(4)
             packet_2 = s.recv(8)
             packet_3 = s.recv(48)
             packet_4 = s.recv(48)
             packet_5 = s.recv(48)
             packet_6 = s.recv(48)
             packet_7 = s.recv(48) 
             packet_8 = s.recv(48)
             packet_9 = s.recv(48)
             packet_10 = s.recv(48)
             packet_11 = s.recv(48)
            
             packet_12 = s.recv(8)
             x = struct.unpack('!d',packet_12)[0]
             print ("X = ", x * 1000)
            
             packet_13 = s.recv(8)
             y = struct.unpack('!d', packet_13)[0]
             print ("Y = ", y * 1000)
            
             packet_14 = s.recv(8)
             z = struct.unpack('!d', packet_14)[0]
             print ("Z = ", z * 1000)
            
             packet_15 = s.recv(8)
             Rx = struct.unpack('!d', packet_15)[0]
             print ("Rx = ", Rx)
            
             packet_16 = s.recv(8)
             Ry = struct.unpack('!d', packet_16)[0]
             print ("Ry = ", Ry)
            
             packet_17 = s.recv(8)
             Rz = struct.unpack('!d', packet_17)[0]
             print ("Rz = ", Rz)
            
             home_status = 1
             program_run = 0
             s.close()
         except socket.error as socketerror:
             print("Error: ", socketerror)
print ("Program finish")