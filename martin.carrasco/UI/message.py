import time
import sqlalchemy
import json

class Message:
    def __init__(self, data_type, data, sender, receiver, timestamp):
        self.data_type = data_type
        self.data = data
        self.sender = sender
        self.receiver = receiver
        self.timestamp = timestamp

    def get_data(self):
        return self.data
    def get_data_type(self):
        return self.data_type
    def get_sender(self):
        return self.sender
    def get_receiver(self):
        return self.receiver
    def get_timestamp(self):
        return self.timestamp

class Chat:
    def __init__(self, sender, receiver, time_created, last_activity, msgs):
        self.sender = sender
        self.receiver = receiver
        self.time_created = time_created
        self.last_activity = last_activity
        self.msgs = msgs

    def get_time_created(self):
        return self.time_created
    def get_last_act(self):
        return self.last_activity
    def get_sender(self):
        return self.sender
    def get_receiver(self):
        return self.receiver
    def get_messages(self):
        return self.msgs

    def save(self, connection):
        connection.execute("CREATE TABLE IF NOT EXISTS " + self.sender +"("+
            "id INTEGER PRIMARY KEY AUTO_INCREMENT,"+
            "sender TEXT(50), "+
            "receiver TEXT(50), "+
            "messages TEXT(5000), " +
            "last_activity BIGINT, "+
            "time_created BIGINT" +
            ")")

        str_list = []
        for msg in self.msgs:
            str_list.append(json.JSONEncoder.encode(msg))

        connection.execute("INSERT INTO " + self.sender + "(sender, receiver, messages, last_activity, time_created) " +
                           "VALUES(%s,%s,%s,%d,%d)" % (self.sender, self.receiver, ''.join(str_list), self.last_activity, self.time_created))
class ChatFactory:
    def __init__(self, sender, receiver):
        self.sender = sender
        self.receiver = receiver
        self.last_activity = time.time()
        self.time_created = time.time()
        self.msgs = []

    def sender(self, sender):
        self.sender = sender
        return self

    def receiver(self, receiver):
        self.receiver = receiver
        return self

    def time(self, time):
        self.time_created = time
        return self

    def last_a(self, time):
        self.last_activity = time
        return self

    def add_msg(self, msg):
        self.msgs.append(msg)
        return self
    def add_mult_msg(self, messages):
        for i in messages:
            self.msgs.append(i)
        return self
    def set_msgs(self, messages):
        self.msgs = messages
        return self
    def make(self):
        return Chat(self.sender, self.receiver, self.time_created, self.last_activity, self.msgs)




