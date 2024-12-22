class User():
    def __init__(self, name, email, password, fav_music,gender, avatar):
        self.name = name
        self.email = email
        self.password = password
        self.gender = gender
        self.fav_music = fav_music
        self.avatar = avatar

    def __str__(self):
        return f"name: {self.name}, email: {self.email}, password: {self.password}, gender: {self.gender}, fav_music: {self.fav_music}, avatar: {self.avatar}"