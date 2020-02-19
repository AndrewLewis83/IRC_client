import re

#will also be used for handling messages from multiple servers
class Message:
    def __init__(self, inmessage):
        self.__message = inmessage.split(" ")

    def get_message(self):
        return self.__message

    def set_message(self, msg):
        self.__message = msg

    def msg_to_string(self):
        out_msg = ""
        for word in self.__message:
            out_msg += word + " "
        return out_msg


class Filter:
    # need to change how replacement is handled
    __replacement = ['grinch', 'oobleck', 'sneetches', 'skritz', 'zillow', 'thneeds', 'wocket', 'squitsch']

    def __init__(self):
        self.__fl = {}

    # adds a new word to be filtered
    def filter_word(self, filter_word):
        if len(self.__fl) > 0 and filter_word not in self.__fl:
            self.__fl[filter_word] = self.__replacement.pop(0)
        else:
            self.__fl[filter_word] = self.__replacement.pop(0)

    # checks the incomming message against the filter list
    def filter_msg(self, msg):
        counter = 0
        for incomming_text in msg:
            tststr = incomming_text
            for filter_text in self.__fl:
                regmsg = r".*" + filter_text + ".*"
                result = re.match(regmsg, tststr, re.IGNORECASE)
                if result:
                    msg[counter] = self.__fl[filter_text]
                    #needs to also handle concatinating punctuation and other digets back to the word
            counter = counter + 1
        return msg


class Handler:

    def __init__(self):
        self.filt = Filter()

    # handles a incomming message
    def handle(self, msg):
        if type(msg) is str:
            args = msg.split(" ")
            if str(args[0]) == '/f':
                self.filt.filter_word(args[1])
            else:
                temp_message = Message(msg)
                temp_message.set_message(self.filt.filter_msg(temp_message.get_message()))
                return temp_message.msg_to_string()
