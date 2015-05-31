class View():
    def __init__(self):
        self.options = ["Please enter the number of the issue you need assistance with today", "1: Ordering",
                        "2: Returns", "3: Technical Support", "4: Comlaints"]
        self.choice = 0

    def displayText(self, msg):
        print msg

    def handleCommand(self, command):
        pass

    def get_choice(self):
        return self.choice

    def handleLocal(self, command):
        pass

    # override
    def connect_view(self):
        pass


class CustView(View):
    def connect_view(self):
        for s in self.options:
            print s
        choice = 0
        while choice < 1 or choice > 4:
            choice = raw_input("Option number? ")
            try:
                choice = int(choice)
            except ValueError:
                choice = 0
        self.choice = choice
        print "An agent will assist you shortly"


class AgentView(View):
    def connect_view(self):
        print "Please wait for a customer to join and/or choose an option."

    def handleCommand(self, c):
        if c['command'] == 'option':
            option = int(c['val'])
            print c['name'] + " needs assistance with the following: "
            print self.options[option]
