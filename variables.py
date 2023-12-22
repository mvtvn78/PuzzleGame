import random
class Variables:
    def __init__(self):
        #setting
        self.title= "Jigsaw Puzzle Game"
        self.FPS = 90
        self.WIDTH =800
        self.HEIGHT = 600
        #color
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.YELLOW = (255, 165, 0)
        self.BLUE = (51, 255, 255)
        self.RED = (255,0,0)
        self.GREEN =(0,204,0)
        #Game
        self.LIMITSIZE = 384
        self.LEVEL = 2
        self.MAXLEVEL = 7
        self.AUDIOFLAG = True
        self.ImgDF = {
        "Level 1" : "asset/lv1.png",
        "Level 2" : "asset/lv2.jpg",
        "Level 3" : "asset/lv3.png",
        "Level 5" : "asset/lv5.png",
        "Level 6" : "asset/lv6.png",
        "Background" : "asset/background.jpg",
        }
        self.ImgSet = {
        "Level 1" : "asset/lv1.png",
        "Level 2" : "asset/lv2.jpg",
        "Level 3" : "asset/lv3.png",
        "Level 4" : "asset/lv4.png",
        "Level 5" : "asset/lv5.png",
        "Level 6" : "asset/lv6.png",
        "Background" : "asset/background.jpg",
        }
        self.imgCurrent = self.ImgSet["Level 1"]
        self.imgBG = self.ImgSet["Background"]
    def SetImg(self,key,value):
        self.ImgSet[key]= value
    def SetDefaultIMG(self):
        self.ImgSet = {key: self.ImgDF[key] for key in self.ImgDF}
    def Update(self):
        # get real index current level
        realLv = self.LEVEL-2
        if realLv <= 5:
            for index,key in enumerate(self.ImgSet):
                if index == realLv and key != "Background":
                    self.imgCurrent= self.ImgSet[key]
                    break
        else:
            idx = random.randrange(0,5)
            for index,key in enumerate(self.ImgSet):
                if index == idx:
                    self.imgCurrent = self.ImgSet[key]
                    break
        self.imgBG = self.ImgSet["Background"]