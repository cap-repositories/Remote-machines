# -*- coding: utf-8 -*-
"""
Created on Fri Jun 19 16:01:02 2020

@author: Juan
"""

from robotmongodb import robotdbcontrol



robotdb = robotdbcontrol("student", "letmegetin")




def tx(s):
    #codificar string y mandar por puerto serial
    data = str.encode(s)+b"\n"
    return data


    
co =  tx("movej([-1.95, -1.58, 1.16, -1.15, -1.55, 1.18], a=0.5, v=0.5)") #este es un ejemplo, se deben enviar los comandos sengun URScript
   
data = robotdb.sendDB(2, co)