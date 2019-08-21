from threading import Thread
from poller import Poller 

def handler(name, hostname, username, password, timeout, port):
    _poller = Poller(name, hostname, username, password, timeout, port)
    if _poller.open():
        thread = Thread(target= _poller.read)
    else:
        #todo

if __name__ == "__main__":
    name = input("Name: ")
    hostname = input("Hostname: ")
    username = input("username: ")
    password = input("Password: ")
    timeout = input("Timeout: ")
    port = input("Port: ")

    