import socket, threading, SocketServer, sys, json


class Venue:

    def __init__(self, ip, DJ, message):
        self.ip = ip
        self.DJ = DJ
        self.message = message
        

zipVenueDict = {}

class ThreadedTCPRequestHandler(SocketServer.BaseRequestHandler):
        
    def handle(self):

        self.data = self.request.recv(1024).strip()
        self.data = json.loads(self.data)
        request = int(self.data["req"])
        zipCode = int(self.data["zip"])
        
        if request == 1:
            print 1
            self.request.send(self.nearbyToJSON(zipCode))
        if request == 2:
            print 2
            ip = self.data["ip"]
            DJ = self.data["DJ"]
            message = self.data["message"]
            self.addZipVenueDict(zipCode, ip, DJ, message)
            self.request.send(ip+" "+DJ+" "+message+" ")
            
    def addZipVenueDict(self, zipCode, ip, DJ, message):
        global zipVenueDict
        zipVenueDict[zipCode] = Venue(ip, DJ, message)
        
    def nearbyToJSON(self, zipCode):
        """Converts current playlist of songs to JSON"""
        thingsToSend = {"ips":[], "DJs":[], "messages":[]}
        #print "playlist is ", playlist
        for k,v in zipVenueDict.iteritems():
            if k == zipCode:
                thingsToSend["ips"].append(v.ip)
                thingsToSend["DJs"].append(v.dj)
                thingsToSend["messages"].append(v.message)
        return json.dumps(thingsToSend)

class ThreadedMainTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    pass

    
def initMainServer(HOST, PORT, zvdict):
    global zipVenueDict
    zipVenueDict = zvdict
    
    server =  ThreadedMainTCPServer((HOST, PORT), ThreadedTCPRequestHandler)
    ip, port = server.server_address
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.setDaemon(True)
    server_thread.start()
    print "Main Server loop running in thread:", server_thread.getName()



if __name__ == "__main__":
    from Song import *
    # Port 0 means to select an arbitrary unused port
    HOST, PORT = "localhost", 9993

    s = Venue("localhost", "DJ D", "Cool!")
    zipVenueDict = {19104 : s}
    initMainServer(HOST, PORT, {})
