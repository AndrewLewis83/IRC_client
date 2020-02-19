import socket
#import tools
import sys

class IRC:

	irc = socket.socket()
	
	def __init__(self):  
		self.irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		
	def send(self, chan, msg):
		
		cmd = "PRIVMSG {}".format(chan)
		msg = ":" + msg
		cmd = "{} {}\r\n".format(cmd, msg)
		self.irc.send(cmd.encode("utf-8"))
	
	def connect(self, server, channel, nickname):
		#defines the socket
		print ("connecting to:"+server)
		self.irc.connect((server, 6667))                    #connects to the server
		
		setnickname = "NICK " + nickname + "\n"
		setnickname = setnickname.encode("utf-8")
		self.irc.send(setnickname)
			
		userAuth = "USER " + nickname + " " + nickname +" " + nickname + " :This is a fun bot!\n"
		userAuth = userAuth.encode("utf-8")
		self.irc.send(userAuth) #user authentication
		
		joinchannel = "JOIN " + channel + "\n"
		joinchannel = joinchannel.encode("utf-8")
		
		self.irc.send(joinchannel) #join the channel
	
	def get_text(self):
		text=self.irc.recv(2040)  #receive the text
		text = text.decode("ASCII", errors='ignore')
		
		if text.find('PING') != -1:
			response = 'PONG ' + text.split() [1] + 'rn'
			response = response.encode("utf-8")
			self.irc.send(response)
			return
		
		return text
	
	def close(self):
		self.irc.shutdown(socket.SHUT_RDWR)

