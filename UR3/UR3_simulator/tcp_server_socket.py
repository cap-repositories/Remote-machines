import socket
import sys
import multiprocessing as mp
import time

class tcp_servers:
    def __init__(self,host="192.168.0.31", port=50007):
        self.host = host
        self.port = port
        self.server_list_count = 0
        
    def start_server(self,event_obj=None):
        s = None
        try:
            #					IPv4             stream socket      tcp protocol
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)
            # given that the socket type is a stream, there is no need to specify the protocol*
        except OSError as msg:
            s = None	
        try:
            s.bind((self.host,self.port))
            s.listen(1)
            print("Server at {}:{} started".format(self.host,self.port))
        except OSError as msg:
            s.close()
            s = None

        if s is None:
            print('could not open socket')
            sys.exit(1)

        continue_listening = True
        while continue_listening:
            conn, addr = s.accept()
            with conn:
                print('Connected by', addr)
                while True:
                    data = conn.recv(1024)
                    if not data:
                        break
                    if data == b'End':
                        continue_listening = False
                    conn.send(data)
        s.close()
        print("Server at {}:{} closed".format(self.host,self.port))

        if event_obj:
            event_obj.set()
    
    def start_server_processes(self,ports=(50007,50008),event_obj=None,killevent_obj=None):
        server_list = []
        for port in ports:
            self.port = port
            p = mp.Process(target=self.start_server, args=(event_obj,), 
                            name="tcp://{}:{}".format(self.host,self.port))
            p.start()
            server_list.append(p)
        self.supervisor_server(event_obj,server_list,killevent_obj=killevent_obj)
    
    def supervisor_server(self,event_obj,server_list,killevent_obj=None):
        if event_obj:
            while server_list:
                try:
                    i = list(map(lambda x: x.is_alive(), server_list)).index(False)
                    server_list[i].close()
                    print("process {} closed".format(server_list[i].name))
                    server_list.pop(i)

                except ValueError:
                    event_obj.clear()
                    event_obj.wait(10)
                    time.sleep(1)
                    if killevent_obj and killevent_obj.is_set():
                        print("Kill event triggered")
                        for p in server_list:
                            if p.is_alive():
                                print("process {} killing".format(p.name))
                                p.terminate()
                                while p.is_alive():
                                    continue
                                p.close()
                                print("process {} closed".format(p.name))
                        server_list = []
            print("All processes finished")