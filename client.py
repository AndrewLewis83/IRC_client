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
                blocklist.append(message.split()[1])
            # command for unblocking a user. Assumes the blocked user is the 2nd argument of the message
            elif cmd == "/unblock":
                blocklist.remove(message.split()[1])
                # command for filtering
            elif cmd == "/f":
                handle.handle(message)
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
        # checks if any mention of a blocked user is in the message. If so blocks the message.
        # this approach is overkill, and I will narrow it down to only messages sent by blocked users
        for i in blocklist:
            if i in user[0]:
                blocked = True
        # if no mention of a blocked user in message, prints the message.
        if not blocked:

            message = handle.handle(message[len(message) - 1])
            print("\n", user[0], ": ", message )

        if stop_threads:
            break

handle = filter.Handler()
blocklist = []  # list of blocked users
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
