from irc import *
import os
import random
import threading


def outgoing():
    while True:
        global stop_threads
        message = input(f"{nickname} > ")

        # broke up the message into whitespace, with the 1st element being put into a variable called cmd
        if len(message) != 0:
            cmd = message.split()[0]

        # if any of these commands are recognized it performs them, otherwise just sends the message.
        if message:
            # only changed which variable is being compared to string "exit"
            if cmd == "exit":
                irc.close()
                stop_threads = True
            # command for blocking a user. Assumes the user to be blocked is the 2nd argument of the message
            elif cmd == "/block":
                global blocklist
                blocklist[message.split()[1]] = True
            # command for unblocking a user. Assumes the blocked user is the 2nd argument of the message
            elif cmd == "/unblock":
                blocklist[message.split()[1]] = False
            else:
                irc.send(channel, message)
        if stop_threads:
            break


def incoming():
    while True:
        global stop_threads
        global blocklist
        blocked = False
        text = irc.get_text()
        if text != None:
            # the message is always after the : symbol
            message = text.split(':')
            # user is always before the ! symbol
            user = text.split('!')
        user[0].strip()

        # if no mention of a blocked user in message, prints the message.
        if not blocklist[user[0]]:
            print("\n", user[0], ": ", message[len(message) - 1])

        if stop_threads:
            break


blocklist = {}  # list of blocked users
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
