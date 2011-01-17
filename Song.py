

class Song:
    
    def __init__(self, title="", artist="", album="", requested = False):
        self.title = title
        self.artist = artist
        self.album = album
        self.ID = None

        #Number of total votes and total thumbsUp feedbacks
        self.votes = 0
        self.thumbsUp = 0
        
        self.isFuture = 0
        self.requested = requested
        self.requests = 0
        
    def __getitem__(self, key):

        if key == 0:
            return self.title
        elif key == 1:
            return self.artist
        elif key == 2 and not self.requested:
            return self.votes
        elif key == 2 and self.requested:
            return self.requests

    def __cmp__(self, other):

        if self.title == other.title and self.artist == other.artist:
            return 0
        else:
            return cmp(self.title, other.title)
        
    def upThumbsUp(self):
        self.thumbsUp +=1
        
    def upThumpsDown(self):
        self.thumbsUp -=1

    def upVote(self):
        self.votes +=1
        

    
