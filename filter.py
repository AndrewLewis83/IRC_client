import re

#will also be used for handling messages from multiple servers
class message:
    def __init__(self, inmessage):
        self.__message = inmessage.split(" ")

    def getMessage(self):
        return self.__message

    def setMessage(self, msg):
        self.__message = msg

    def msg_to_string(self):
        outMsg = ""
        for x in self.__message:
            outMsg += x + " "
        return outMsg


class filter:
    # need to change how replacement is handled
    __replacement = ['grinch', 'oobleck', 'sneetches', 'skritz', 'zillow', 'thneeds', 'wocket', 'squitsch']

    def __init__(self):
        self.__fl = {}

    # adds a new word to be filtered
    def filterWord(self, fw):
        if len(self.__fl) > 0 and fw not in self.__fl:
            self.__fl[fw] = self.__replacement.pop(0)
        else:
            self.__fl[fw] = self.__replacement.pop(0)

    # checks the incomming message against the filter list
    def filterMsg(self, msg):
        i = 0
        for x in msg:
            tststr = x
            for y in self.__fl:
                regmsg = r".*" + y + ".*"
                result = re.match(regmsg, tststr, re.IGNORECASE)
                if result:
                    msg[i] = self.__fl[y]
                    #needs to also handle concatinating punctuation and other digets back to the word
            i = i + 1
        return msg


class Handler:

    def __init__(self):
        self.__numFiltered = 0
        self.filt = filter()

    # handles a incomming message
    def handle(self, msg):
        if type(msg) is str:
            args = msg.split(" ")
            if str(args[0]) == '/f':
                self.filt.filterWord(args[1])
            else:
                tMsg = message(msg)
                tMsg.setMessage(self.filt.filterMsg(tMsg.getMessage()))
                return tMsg.msg_to_string()
