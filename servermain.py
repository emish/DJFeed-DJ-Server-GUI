
import socket, json, threading

conn = None
HOST = 'localhost'
PORT = 9997

class UserHandler:
    def __init__(self):
        self.handlerMap = {}
        self.handlerLock = threading.Lock()
        
    def registerHandler(self, handler):
        self.handlerLock.acquire()
        self.handlerMap[handler.id] = handler
        self.handlerLock.release()

class SocketHandler(threading.Thread):
    """Handles all socket connections and message passing"""
    def __init__(self, sock, playlist):
        self.playlist = playlist
        self.sock = sock
        
    class RequestHandleThread(threading.Thread):
        """The thread that manages a received message"""
        def __init__(self, parent, data, conn, addr):
            self.parent = parent
            self.data = data
            self.conn = conn
            self.addr = addr
            threading.Thread.__init__(self)
            
        def playlistToJSON(self):
            """Converts current playlist of songs to JSON"""
            songsToSend = {"songs":[]}
            print "playlist is ", self.parent.playlist
            for k,v in self.parent.playlist.iteritems():
                songsToSend["songs"].append((v.title, v.artist))
            return json.dumps(songsToSend)
                
        def run(self):
            print "Handling a request"
            self.data = json.loads(self.data)
            request = int(self.data["req"])
            song = self.parent.playlist[int(self.data["id"])]
            if request == 1: #Vote
                song.upVote()
                self.conn.send("ack")
            elif request == 2: #ThumbsUp
                song.upThumbsUp()
                self.conn.send("ack")
            elif request == 3: #ThumbsDown
                song.upThumbsDown()
                self.conn.send("ack")
            elif request == 4: #Update
                print "attempting to send playlist"
                self.conn.send(self.playlistToJSON())
            elif request == 5: #NowPlaying TODO!
                self.conn.send("ack")
                
            # TODO: Switch on request type
            
    def start(self):
        """Starts the socket handling"""
        while 1:
            try:
                self.conn, self.addr = self.sock.accept()
                print "New connection from: ", self.addr
                # Create a new receive thread to handle this
                slaveThread = self.RequestHandleThread(self, self.getData(), self.conn, self.addr)
                slaveThread.start()
                
            except socket.error, e:
                print >>sys.stderr, "Got an error in accept: ", str(e)
                break
            except KeyboardInterrupt:
                print "Exiting..."
                break
        self.sock.close()
        
    def getData(self):
        """If the connection goes down, returns 0 length string. Otherwise
        buffers the data and returns it as a string. All requests are 
        JSON packets"""
        data = []
        while 1:
            d = self.conn.recv(1024)
            data.extend(d)
            if len(d) < 1024: break
        return "".join(data)
                
    

class DJServer:
    def __init__(self, host, port, playlist):
        self.port = port
        self.host = host
        self.handlerId = 0
        self.playlist = playlist
        
    def start(self):
        print "DJ Server Started, " + self.host + ":" + str(self.port)
        
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            sock.bind((self.host,self.port))
            sock.listen(5)
        except socket.error, e:
            print "Socket Error: Unable to Bind to port", self.port
            return
        sock_handler = SocketHandler(sock, self.playlist)
        sock_handler.start()
        
        
if __name__ == "__main__":
    from Song import *
    s = Song("Across the Universe", "Fiona Apple", "PleasantVille")
    playlist = {10 : s}
    DJServer(HOST, PORT, playlist).start()
        # Start GUI stuff here
        
        # Start server stuff
        
#class DJServerHandler(BaseHTTPRequestHandler):
#    
#    def do_POST():
#        pass
#
#s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#
#s.bind((HOST, PORT))
#
#s.listen(1)
#conn, addr = s.accept()
#
#print("Connected by", addr)
#
#while True:
#    data = conn.recv(1024)
#    if not data:
#        break
#    conn.send(data)
#com.close()
#
#json.dumps(data, separators = (",", ":"))
