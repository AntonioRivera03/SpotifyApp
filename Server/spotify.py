class Song():
    def __init__(self, song='', playstate='', artist='', cover=''):
        self.song = song
        self.playstate = playstate
        self.artist = artist
        self.albumCover = cover
        
        

    

    #BEGIN GETTER METHODS

    @property
    def song(self):
        return self._song

    @property
    def playstate(self):
        return self._playstate

    @property
    def artist(self):
        return self._artist

    @property
    def albumCover(self):
        return self._albumCover
    


    #END GETTER METHODS

    #BEGIN SETTER METHODS
    @song.setter
    def song(self, param: str):
        
        self._song = param

    @artist.setter
    def artist(self, param: str):
        
        self._artist = param

    @albumCover.setter
    def albumCover(self, param: str):
        
        self._albumCover = param
    
    @playstate.setter        
    def playstate(self, param: str):
        
        self._playstate = param

    #END SETTER METHODS

    