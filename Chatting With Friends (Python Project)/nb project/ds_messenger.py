
import socket
import json
import time

class ServerConnectionError(BaseException):

    def __init__(self, reason="Failed to connect server"):
        self.reason = reason
        
    def __str__(self):
        return self.reason

class JSONParseError(BaseException):

    def __init__(self, reason):
        self.reason = "Failed to parse the JSON message from server: " + reason
        
    def __str__(self):
        return self.reason
        
class DirectMessage:

    def __init__(self, recipient = None, message = None, timestamp = None):
        self.recipient = recipient
        self.message = message
        self.timestamp = timestamp
        
    def __str__(self):
        return f"from: {self.recipient}, message: {self.message}, time: {self.timestamp}"
    
class DirectMessenger:

    def __init__(self, dsuserver=('168.235.86.101', 2021), username=None, password=None):
        """Inits DirectMessenger
        
        dsuserver could be a turple or string(ip:port)
        """
        self.keypair = ''
        for _ in range(88):
            self.keypair = self.keypair + username + password
 
        self.public_key = self.keypair[:44]
        self.private_key = self.keypair[44:88]
        
        self.username = username
        self.password = password
 
        if isinstance(dsuserver, str):
            dsuserver = dsuserver.split(':')
        self.server = dsuserver[0]
        self.port = dsuserver[1]
 
    def connect_server(self):
        self.client = socket.socket() 
        try:
            self.client.connect((self.server, self.port))
            self.sendw = self.client.makefile('w')
            self.recv = self.client.makefile('r')
        except:
            raise ServerConnectionError(f'failed to connect {self.server} on port {self.port}') 
    
    def join_server(self):
        # join
        try:
            joinValue = { }
            joinValue['username'] = self.username
            joinValue['password'] = self.password
            joinValue['token'] = self.public_key
            join_msg = json.dumps({'join':joinValue})
        
            print(join_msg)
            self.sendw.write(join_msg + '\r\n')
            self.sendw.flush()
            
            # get token
            resp = self.recv.readline()
            print(resp)
            try:
                json_obj = json.loads(resp)
                messageType = json_obj['response']['type']
                responseMsg = json_obj['response']['message']
            except json.JSONDecodeError as e:
                raise JSONParseError(e.__str__())
            
            if messageType == 'error':
                raise ServerConnectionError(responseMsg) 

            self.server_public_key = json_obj['response']['token']
        except BaseException as e:
            raise ServerConnectionError(e.__str__()) 
            
    def send(self, message:str, recipient:str) -> bool:
        # returns true if message successfully sent, false if send failed.
        try:
            self.connect_server()
            self.join_server()

            # post
            token = self.public_key
            postValue = { }
            postValue['entry'] = message
            postValue['recipient'] = recipient
            postValue['timestamp'] = time.time()
            post_msg = json.dumps({'token':token, 'directmessage':postValue})
            print(post_msg)
            self.sendw.write(post_msg + '\r\n')
            self.sendw.flush()    
        
            # get result of post
            resp = self.recv.readline()
            print(resp)
            try:
                json_obj = json.loads(resp)
                messageType = json_obj['response']['type']
                responseMsg = json_obj['response']['message']
            except json.JSONDecodeError as e:
                raise JSONParseError(e.__str__())
            
            if messageType == 'error':
                raise ServerConnectionError(responseMsg) 

            return True
        except BaseException as e:
            print(e.__str__())
            return False
        
    def retrieve_new(self) -> list:
        # returns a list of DirectMessage objects containing all new messages
        result = []
        try:
            self.connect_server()
            self.join_server()

            # post
            token = self.public_key
            post_msg = json.dumps({'token':token, 'directmessage':'new'})
            print(post_msg)
            self.sendw.write(post_msg + '\r\n')
            self.sendw.flush()    
        
            # get result of post
            resp = self.recv.readline()
            print(resp)
            try:
                json_obj = json.loads(resp)
                messageType = json_obj['response']['type']
                if messageType == 'ok':
                    responseMsgs = json_obj['response']['messages']
                    for m in responseMsgs:
                        result.append(DirectMessage(m['from'], m['message'], m['timestamp']))
            except json.JSONDecodeError as e:
                raise JSONParseError(e.__str__())

        except BaseException as e:
            print(e.__str__())

        return result
 
    def retrieve_all(self) -> list:
        # returns a list of DirectMessage objects containing all messages
        result = []
        try:
            self.connect_server()
            self.join_server()

            # post
            token = self.public_key
            post_msg = json.dumps({'token':token, 'directmessage':'all'})
            print(post_msg)
            self.sendw.write(post_msg + '\r\n')
            self.sendw.flush()    
        
            # get result of post
            resp = self.recv.readline()
            print(resp)
            try:
                json_obj = json.loads(resp)
                messageType = json_obj['response']['type']
                if messageType == 'ok':
                    responseMsgs = json_obj['response']['messages']
                    for m in responseMsgs:
                        result.append(DirectMessage(m['from'], m['message'], m['timestamp']))
            except json.JSONDecodeError as e:
                raise JSONParseError(e.__str__())

        except BaseException as e:
            print(e.__str__())

        return result
 