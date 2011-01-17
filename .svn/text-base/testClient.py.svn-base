
import socket, json, sys

HOST = 'localhost'
PORT = 9999

class Client:
    def __init__(self, host, port):
        self.host = host 
        self.port = port
        self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
    def get_data(self):
        data = []
        while 1:
            d = self.conn.recv(1024)
            data.extend(d)
            if len(d) < 1024: break
        return "".join(data)
    
    def connect_to_server(self):
        try:
            self.conn.connect((self.host, self.port))
            return 1
        except socket.error, e:
            print >>sys.stderr, "Cant connect to remote host", str(e)
            return 0
        
    def testRequest(self, req, id):
        #req = 1
        #id = 10
        if not c.connect_to_server():
            print "brublem"
            sys.exit(1)
        sampleMsg = json.dumps({"req":str(req),
                     "id": str(id)})
        self.conn.send(sampleMsg)
        print self.get_data()
        self.conn.close()
        

        
if __name__ == "__main__":
    c = Client(HOST, PORT)
    
    c.testRequest(2, 10)
    c.testRequest(1, 10)
