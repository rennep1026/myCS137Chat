class View():

    def __init__(self, handler):
        self.handler = handler
        self.connect_view()

    def get_handler(self):
        return self.handler

    # override
    def connect_view(self):
        pass

class CustView(View):

    def connect_view(self):
        self.handler.do_send("Welcome to our chat system! Please hold for an agent")

class AgentView(View):

    def connect_view(self):
        self.handler.do_send("Please wait for a customer to join.")
