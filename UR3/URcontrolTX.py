# -*- coding: utf-8 -*-
"""
Created on Mon Oct 21 11:55:53 2019

@author: jamuj
"""

#from robotmongodb import robotdbcontrol
import socket
HOST = "192.168.15.15" # ip del robot
PORT = 30003 # puerto en el que el robot recibe

#robotdb = robotdbcontrol("student", "letmegetin")


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #crear un socket

s.connect((HOST, PORT)) #iniciar la comunicacion

def tx(s):
    #codificar string y mandar por puerto serial
    data = str.encode(s)+b"\n"
    return data

#data = robotdb.readDB(1)
#print(data)
    
#co =  tx("movej([-1.95, -1.58, 1.16, -1.15, -1.55, 1.18], a=0.5, v=0.5)") #este es un ejemplo, se deben enviar los comandos sengun URScript
   
#s.send(data["f"])
#data = s.recv(1024)
#s.close()

s.send ("movej([-1.95, -1.58, 1.16, -1.15, -1.55, 1.18], a=1.0, v=0.1)" + "\n")
s.close()
#"movej(p[0.00, 0.3, 0.4, 2.22, -2.22, 0.00], a=1.0, v=0.1)"