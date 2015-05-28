from network import Handler, poll
import sys
from threading import Thread
from time import sleep

transcript = "What is your name?\n"
client_name = raw_input('What is your name? ')
transcript += client_name+"\n"
client_type = "customer"
if client_name.split()[0] == 'Agent':
    client_type = "Agent"


class Client(Handler):

    def on_close(self):
        pass
    #TODO Fix option choosing
    def on_msg(self, msg):
        if msg['type'] == 'text':
            self.transcript += msg['txt']+"\n"
            print msg['txt']
        elif msg['type'] == 'topic':
            self.transcript += msg['txt']+"\n"
            print msg['txt']
            choice = ""
            while not is_num(choice) or (int(choice) < 1 or int(choice) > 4):
                self.transcript += "Enter a choice number\n"
                choice = raw_input("Enter a choice number: ")
            self.do_send({"type": "choice", "txt": choice})


    def set_transcript(self, transcript):
        self.transcript = transcript

    def add_to_transcript(self, msg):
        self.transcript += msg+"\n"

host, port = 'localhost', 8990
client = Client(host, port)
client.set_transcript(transcript)
client.do_send({'type': 'join', 'join': client_name, 'cust_type': client_type})


def periodic_poll():
    while 1:
        poll()
        sleep(0.05)  # seconds

thread = Thread(target=periodic_poll)
thread.daemon = True  # die when the main thread dies 
thread.start()


def get_input(client):
    mytxt = sys.stdin.readline().rstrip()
    client.add_to_transcript(mytxt)
    return mytxt


def is_num(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

while 1:
    mytxt = get_input(client)
    client.do_send({'type': 'text', 'speak': client_name, 'txt': mytxt})
    sleep(0.08)
