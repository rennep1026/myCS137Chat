from network import Listener, Handler, poll, get_my_ip

cust = {}  # map client handler to user name
agent = {}

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
                agentCount = len(agent)
                if agentCount >= 1:
                    self.do_send({"close": "The chat is currently full. Please try again later."})
                    self.do_close()
                agent[self] = {'name': msg['join'], 'type': msg['type'], 'choice': msg['choice']}
                if len(cust) > 0:
                    thisCust = cust.values()[0]
                    self.do_send({'command': 'option', 'val': thisCust['choice'], 'name': thisCust['name']})
            else:
                custCount = len(cust)
                if custCount >= 1:
                    self.do_send({"close": "The chat is currently full. Please try again later."})
                    self.do_close()
                cust[self] = {'name': msg['join'], 'type': msg['type'], 'choice': msg['choice']}
                if len(agent) > 0:
                    theAgent = agent.keys()[0]
                    theAgent.do_send({'command': 'option', 'val': msg['choice'], 'name': msg['join']})
        elif 'msg' in msg:
            if len(cust) > 0:
                cust.keys()[0].do_send({'msg': msg['msg'], 'txt': msg['msg']+": "+msg['txt']})
            if len(agent) > 0:
                agent.keys()[0].do_send({'msg': msg['msg'], 'txt': msg['msg']+": "+msg['txt']})
 
 
port = 8888
server = Listener(port, MyHandler)
print "IP Address: " + str(get_my_ip())
print "Port #: " + str(port)
while 1:
    poll(timeout=0.05) # in seconds
