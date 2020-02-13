from irc import *
import os
import random
import threading

def outgoing():
	while True:
		global stop_threads
		message = input(f"{nickname} > ")
		if message:
			if message == "exit":
				irc.close()
				stop_threads = True
			else:    
				irc.send(channel, message)
		if stop_threads:
			break
    
def incoming():

	while True:
		global stop_threads
		text = irc.get_text()
		print("\n", text)
		
		if stop_threads:
			break
	

channel = input("Enter channel name:> ")
server = "irc.freenode.net"
nickname = input("Enter Nick:> ")
stop_threads = False

irc = IRC()
irc.connect(server, channel, nickname)

# creating threads
outgoingThread = threading.Thread(target=outgoing, name='outgoingThread')
incomingThread = threading.Thread(target=incoming, name='incomingThread')

outgoingThread.start()
incomingThread.start()

outgoingThread.join()
incomingThread.join()

print("Goodbye!")