from network import Listener, Handler, poll, get_my_ip

cust = {}  # map client handler to user name
agent = {}
queue = {}

class MyHandler(Handler):

    def on_open(self):
        pass
         
    def on_close(self):
        if self in cust:
            cust.pop(self)
        elif self in agent:
            agent.pop(self)
     
    def on_msg(self, msg):
        print msg
        if 'join' in msg:
            if msg['type']=='agent':
                if len(agent) >= 1:
                    self.do_send({"close": "An agent is already in the chat."})
                    self.do_close()
                else:
                    agent[self] = {'name': msg['join'], 'type': msg['type'], 'choice': msg['choice']}
                    if len(cust) > 0:
                        thisCust = cust.values()[0]
                        self.do_send({'command': 'option', 'val': thisCust['choice'], 'name': thisCust['name']})
            else:
                self.do_send({"msg": "", 'txt': "Please wait for an available agent."})
                queue[self] = msg
        elif 'msg' in msg:
            for c in cust:
                c.do_send({'msg': msg['msg'], 'txt': msg['msg']+": "+msg['txt']})
            for a in agent:
                a.do_send({'msg': msg['msg'], 'txt': msg['msg']+": "+msg['txt']})


def add_customer(self, msg):
    cust[self] = {'name': msg['join'], 'type': msg['type'], 'choice': msg['choice']}
    if len(agent) > 0:
        theAgent = agent.keys()[0]
        theAgent.do_send({'command': 'option', 'val': msg['choice'], 'name': msg['join']})
 
 
port = 8888
server = Listener(port, MyHandler)
print "IP Address: " + str(get_my_ip())
print "Port #: " + str(port)
while 1:
    if len(cust) == 0:
        if len(queue) > 0:
            newCust = queue.items()[0]
            add_customer(newCust[0], newCust[1])
            newCust[0].do_send({"msg": "", 'txt': "An agent is now available to assist."})
    poll(timeout=0.05) # in seconds
