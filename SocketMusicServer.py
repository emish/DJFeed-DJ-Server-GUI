import socket, threading, SocketServer, sys, json


playlist = {}

class ThreadedTCPRequestHandler(SocketServer.BaseRequestHandler):
        
    

    def handle(self):
        print "handlinga"
        self.data = self.request.recv(1024).strip()
        self.data = json.loads(self.data)
        request = int(self.data["req"])
        print len(playlist)
        if request in [1,2,3]:
            song = playlist[int(self.data["id"])]
        
        
        if request == 1: #Vote
            song.upVote()
            self.request.send("ack")
        elif request == 2: #ThumbsUp
            song.upThumbsUp()
            self.request.send("ack")
        elif request == 3: #ThumbsDown
            song.upThumbsDown()
            self.request.send("ack")
        elif request == 4: #Update
            print "attempting to send playlist"
            self.request.send(self.playlistToJSON())
        elif request == 5: #NowPlaying TODO!
            self.request.send(self.playlistToJSON())
        #elif request == 6:
            

    def playlistToJSON(self):
        """Converts current playlist of songs to JSON"""
        songsToSend = {"songs":[]}
        print "playlist is ", playlist
        for k,v in playlist.iteritems():
            songsToSend["songs"].append((v.title, v.artist))
        return json.dumps(songsToSend)

class ThreadedMusicTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    pass
    
def initMusicServer(HOST, PORT, pl):
    global playlist
    playlist = pl
    try:
        server =  ThreadedMusicTCPServer((HOST, PORT), ThreadedTCPRequestHandler)
        ip, port = server.server_address
        server_thread = threading.Thread(target=server.serve_forever)
        server_thread.setDaemon(True)
        server_thread.start()
        print "Server loop running in thread:", server_thread.getName()
        #server_thread.join()
    except KeyboardInterrupt, e:
        return



if __name__ == "__main__":
    from Song import *
    # Port 0 means to select an arbitrary unused port
    HOST, PORT = "localhost", 9999

    s = Song("Across the Universe", "Fiona Apple", "PleasantVille")
    s.id = 10
    playlist = {10 : s}
    initMusicServer(HOST, PORT, playlist)
    print "end of main"
