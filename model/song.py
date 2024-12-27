class Song:
    def __init__(self, id, name, album_name, playcount, artist_names):
        self.id = id
        self.name = name
        self.album_name = album_name
        self.playcount = playcount
        self.artist_names = artist_names
        
    def __str__(self):
        return f"{self.name} - {self.artist_names} - {self.album_name} - {self.playcount}"
    
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "album_name": self.album_name,
            "playcount": self.playcount,
            "artist_names": self.artist_names
        }
