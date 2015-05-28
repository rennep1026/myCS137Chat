from network import Listener, Handler, poll
from view import CustView, AgentView

handlers = {}  # Key: Handler Object, Value: list(View, String(name))
waiting = {}

class MyHandler(Handler):

    def on_open(self):
        pass
         
    def on_close(self):
        handlers.pop(self)
     
    def on_msg(self, msg):
        print msg
        if msg['type'] == 'join':
            if msg['cust_type'] == 'Agent':
                handlers[self] = (AgentView(self), msg['join'], msg['cust_type'])
            else:
                handlers[self] = (CustView(self), msg['join'], msg['cust_type'])
                for h in handlers:
                    if h != self:
                        handlers[h][0].pass_msg({'type': 'text', 'txt': msg['join']+" has joined the chat."})
        elif msg['type'] == 'text':
            for h in handlers:
                handlers[h][0].pass_msg({'type': 'text', 'txt': msg['speak']+": "+msg['txt']})
        elif msg['type'] == 'choice':
            for h in handlers:
                if handlers[h][2] == 'Agent':
                    handlers[h][0].pass_msg({'type': 'text', 'txt': "Customer needs help with option "+msg['txt']})

port = 8990
server = Listener(port, MyHandler)
while 1:
    poll(timeout=0.05) # in seconds


