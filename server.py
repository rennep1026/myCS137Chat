from network import Listener, Handler, poll
from view import CustView, AgentView

handlers = {}  # Key: Handler Object, Value: list(View, String(name))


class MyHandler(Handler):

    def on_open(self):
        pass
         
    def on_close(self):
        handlers.pop(self)
        pass
     
    def on_msg(self, msg):
        print msg
        if 'join' in msg:
            if msg['join'].split()[0] == 'Agent':
                handlers[self] = (AgentView(self), msg['join'])
            else:
                handlers[self] = (CustView(self), msg['join'])
                for h in handlers:
                    if h != self:
                        h.do_send(msg['join']+" has joined the chat.")
        elif 'txt' in msg:
            for h in handlers:
                handlers[h][0].pass_msg(msg['speak']+": "+msg['txt'])

port = 8990
server = Listener(port, MyHandler)
while 1:
    poll(timeout=0.05) # in seconds


