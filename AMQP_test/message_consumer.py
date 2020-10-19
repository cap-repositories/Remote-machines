from __future__ import print_function, unicode_literals
from proton import Message
from proton.handlers import MessagingHandler
from proton.reactor import Container
import datetime

class MConsumer(MessagingHandler):
    def __init__(self, server, input_address, output_address):
        super(MConsumer, self).__init__()
        self.server = server
        self.input_address = input_address
        self.output_address = output_address
        self.received = 0

    def on_start(self, event):
        conn = event.container.connect(self.server)
        event.container.create_receiver(conn, self.input_address)

    def on_message(self, event):
        print("Incoming message")
        self.m = event.message.body
        print("[{}]>>> {}".format(self.received,self.m))
        self.received += 1
        if self.m == "close":
            print("closing connection")
            event.connection.close()
        else:
            event.container.create_sender(event.connection, self.output_address)
        
    def on_sendable(self, event):
        """
        This need to be improve:
            find the way to "flush/settle" the message
            to avoid creation of new senders
        """
        event.sender.send(Message(body="Received [{}]".format(datetime.datetime.now())))
        event.sender.close()
            
    

Container(MConsumer("127.0.0.1:5672", "InputQueue","OutputQueue")).run()