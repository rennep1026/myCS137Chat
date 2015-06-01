from network import Handler, poll
import sys
from threading import Thread
from time import sleep
from view import *

host = raw_input('Enter an IP address: ')
port = int(raw_input('Enter port number: '))

view = View()
myname = raw_input('What is your name? ')
clientType = 'cust'
if myname.split()[0].lower() == 'agent':
    view = AgentView()
    clientType = 'agent'
else:
    view = CustView()
view.connect_view()

class Client(Handler):

    def on_close(self):
        quit()
    
    def on_msg(self, msg):
        if 'command' in msg:
            self.view.handleCommand(msg)
        elif 'msg' in msg:
            self.view.displayText(msg['txt'])

    def set_view(self, view):
        self.view = view
        
#host, port = 'localhost', 8888
client = Client(host, port)
client.set_view(view)
client.do_send({'join': myname, 'type': clientType, 'choice': view.get_choice()})

def periodic_poll():
    while 1:
        poll()
        sleep(0.05)  # seconds

thread = Thread(target=periodic_poll)
thread.daemon = True  # die when the main thread dies 
thread.start()

while True:
    mytxt = sys.stdin.readline().rstrip()
    if mytxt != '' and mytxt[0] == ':':
        view.handleLocal(mytxt)
    else:
        client.do_send({'msg': myname, 'txt': mytxt})

client.do_close()
