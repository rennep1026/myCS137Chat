class View():

    def __init__(self, handler):
        self.handler = handler
        self.connect_view()

    def pass_msg(self, msg):
        self.handler.do_send(msg)

    # override
    def connect_view(self):
        pass


class CustView(View):

    def connect_view(self):
        self.handler.do_send({"type": "text", "txt": "Welcome to our chat system!"})
        self.handler.do_send({"type": "text", "txt": "Please enter the number of what you need help with."})
        self.handler.do_send({"type": "text", "txt": "1: Ordering"})
        self.handler.do_send({"type": "text", "txt": "2: Returns"})
        self.handler.do_send({"type": "text", "txt": "3: Technical Support"})
        self.handler.do_send({"type": "text", "txt": "4: Complaints"})


class AgentView(View):

    def connect_view(self):
        self.handler.do_send({"type": "text", "txt": "Please wait for a customer to join."})
