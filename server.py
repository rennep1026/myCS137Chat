from network import Listener, Handler, poll
from view import CustView, AgentView


handlers = []  # list of views
 
class MyHandler(Handler):
     
    def on_open(self):
        pass
         
    def on_close(self):
        pass
     
    def on_msg(self, msg):
        print msg
        if 'join' in msg:
            if msg['join'].split()[0] == 'Agent':
                handlers.append(AgentView(self, msg['join']))
            else:
                handlers.append(CustView(self, msg['join']))
                for h in handlers:
                    thisHandler = h.get_handler()
                    if thisHandler != self:
                        thisHandler.do_send(msg['join']+" has joined the chat.")
        elif 'txt' in msg:
            for h in handlers:
                thisHandler = h.get_handler()
                thisHandler.do_send(msg['speak']+": "+msg['txt'])

port = 8888
server = Listener(port, MyHandler)
while 1:
    poll(timeout=0.05) # in seconds


