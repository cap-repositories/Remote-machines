"""
Visual studio c++ build tools is needed:
    https://visualstudio.microsoft.com/es/visual-cpp-build-tools/
    (20-07-2020) select: Windows 10 SDK
    (20-07-2020) select: MSVC v140 - VS 2015 C++ Build Tools (v14.00)
    (20-07-2020) if you have the error -> LINK : fatal error LNK1158: no se puede ejecutar 'rc.exe',
        copy "rc.exe" and "rcdll.dll" from the appropiate subfolder of C:\Program Files (x86)\Windows Kits
        and paste in C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\BIN\{appropiate folder}
Install qpid proton (AMQP client):
    pip install python-qpid-proton
Tutorial:
    http://qpid.apache.org/releases/qpid-proton-0.31.0/proton/python/docs/tutorial.html
"""


from __future__ import print_function, unicode_literals
from proton import Message, EventType
from proton.handlers import MessagingHandler
from proton.reactor import Container
import http.server
import socketserver
import json
import threading, queue

class MessageReceiverHTTP(http.server.BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path == "/" or self.path == "":
            self.send_response(200)
            self.send_header("Content-type","text/plain")
            self.send_header("Access-Control-Allow-Origin","*")
            self.end_headers()
            if 'Content-Length' in self.headers:
                #print(type(self.headers.get('Content-Length')))
                #print(self.headers['Content-Length'])
                payload = json.loads(self.rfile.read(int(self.headers['Content-Length'])).decode("utf8"))
                #print(">>> {}".format(self.rfile.read(int(self.headers['Content-Length'])).decode("utf8")))
                print("[http]>>> {}".format(payload))
                self.server.comm_q.put(payload)
                #for c in self.server.Containers_list:
                #    c.push_event.push_event(event,EventType("get_message"))
                
                #game_config = self.server.parent.add_user(id_name["userId"],id_name["name"])
                #self.wfile.write(json.dumps(game_config).encode("utf8"))
            self.wfile.write("Received".encode("utf8"))

class RequestGetter(http.server.HTTPServer):
    def __init__(self, comm_q, Containers_list, server_address, RequestHandlerClass):
        super().__init__(server_address, RequestHandlerClass)
        self.comm_q = comm_q
        self.Containers_list = Containers_list

def start_http_server():
    global http_handler
    print("HTTP serving at port", PORT)
    http_handler.serve_forever()

class MSender(MessagingHandler):
    def __init__(self, server, input_address, output_address, comm_queue):
        super(MSender, self).__init__()
        self.server = server
        self.input_address = input_address
        self.output_address = output_address
        self.comm_queue = comm_queue
    
    def on_get_message(self,event,conn=None):
        #self.m = input("Mensaje: ")
        """
        ToDo: make this function run without blockings
        """
        try:
            payload = self.comm_queue.get()
            #event.container.push_event(event,EventType("prueba"))
            if "message" in payload:
                print("Mensaje ",payload["message"])
                self.m = payload["message"]
            else:
                print("Message ",payload)
                self.m = str(payload)
            if self.m == "":
                print("closing connection")
                event.connection.close()
            else:
                if conn:
                    event.container.create_sender(conn, self.output_address)
                else:
                    event.container.create_sender(event.connection, self.output_address)
        except queue.Empty:
            print("timeout")
            event.container.push_event(event,EventType("get_message"))

    def on_prueba(self,event):
        print(event)

    def on_start(self, event):
        conn = event.container.connect(self.server)
        #event.container.push_event(event,EventType("get_message"))
        self.on_get_message(event,conn)
        print("out")

    def on_message(self, event):
        m = event.message.body
        print(">>> {}".format(m))
        event.receiver.close()
        #event.container.push_event(event,EventType("get_message"))
        self.on_get_message(event)
        
    def on_sendable(self, event):
        """
        This need to be improve:
            find the way to "flush/settle" the message
            to avoid creation of new senders
        """
        event.sender.send(Message(body=self.m))
        event.sender.close()
    
    def on_settled(self, event):
        #print("on_settled")
        """
        self.m = input("Mensaje: ")
        event.container.create_sender(event.connection, self.address)
        """
        event.container.create_receiver(event.connection, self.input_address)
    
    def on_reactor_init(self, event):
        super(MSender, self).on_reactor_init(event)
        #print("--- reactor init ---")



if __name__ == "__main__":
    """
    javascript code:
        const Http = new XMLHttpRequest();
        const url='http://localhost:8011/';
        Http.open("POST", url);
        Http.send('{"message":""}'); //shutdown the sender
        //Http.open("POST", url);
        //Http.send('{"message":"close"}'); //shutdown the receiver
    """
    global http_handler
    PORT = 8011
    q = queue.Queue()
    Containers_list = []
    http_handler = RequestGetter(q,Containers_list, ("", PORT), MessageReceiverHTTP)
    http_daemon = threading.Thread(target=start_http_server, daemon=True)
    http_daemon.start()
    #q.get()
    #httpd.shutdown()
    try:
        c = Container(MSender("127.0.0.1:5672", "OutputQueue","InputQueue",q))
        Containers_list.append(c)
        c.run()
    finally:
        http_handler.shutdown()
        if http_daemon.is_alive():
            http_daemon.join()