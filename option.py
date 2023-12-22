import pygame 
import sys 
from tkinter import *
from tkinter import filedialog
from sprite import *
class Option:
    def __init__(self,obj) :
        self.obj = obj
        if not pygame.get_init():
            pygame.init()
        if not pygame.mixer.get_init():
            pygame.mixer.init()
        if not pygame.font.get_init():
            pygame.font.init()
        self.ImageCustom = ["Level 1","Level 2","Level 3","Background"]
        self.screen = pygame.display.set_mode((self.obj.WIDTH, self.obj.HEIGHT))
        #Button Arrow
        self.btnArrow = pygame.image.load("asset/arrow.png")
        self.rectbtnArrow = self.btnArrow.get_rect(center=(self.obj.WIDTH/2,self.obj.HEIGHT/2))
        self.rectbtnArrow.y= 165
        #Button InputDF Filedialog
        self.btnInputDF = pygame.image.load("asset/btnInputImage.png")
        self.btnInputSC = pygame.image.load("asset/btnsuccessInput.png")
        self.rectInput = self.btnInputDF.get_rect(center=(self.obj.WIDTH/2,self.obj.HEIGHT/2))
        #Button Audio
        self.btnaudio = pygame.image.load("asset/btnaudio.png")
        self.btnunadio = pygame.image.load("asset/btnnoaudio.png")
        self.rectbtnAudio = self.btnaudio.get_rect(center=(self.obj.WIDTH/2,self.obj.HEIGHT/2))
        self.rectbtnAudio.y = 75
        #Button Refresh
        self.btnRefund = pygame.image.load("asset/btnrefund.png")
        self.rectbtnRefund = self.btnRefund.get_rect()
        self.rectbtnRefund.x =640
        self.rectbtnRefund.y = 15
        #Button Home
        self.btnHome= pygame.image.load("asset/btnhome.png")
        self.rectbtnHome = self.btnHome.get_rect()
        self.rectbtnHome.x=80
        self.rectbtnHome.y=10
        #Title
        self.optionLabel = LabelSelf("asset/font.otf",80,"Change Image",self.obj.WHITE,self.obj)
        self.optionLabel.rect.y =0
        #Label
        self.labelSuccess= LabelSelf("asset/font.otf",20,"Success",self.obj.GREEN,self.obj)
        self.labelError= LabelSelf("asset/font.otf",20,"Error",self.obj.RED,self.obj)
        self.labelDefault = LabelSelf("asset/font.otf",20,"Default",self.obj.WHITE,self.obj)
        self.labelSuccess.rect.x =self.rectInput.right
        self.labelError.rect.x = self.rectInput.right
        self.labelDefault.rect.x = self.rectInput.right
        #Flag quit
        self.quitOpt = False
        #Label choices
        self.thingchoice = LabelSelf("asset/font.otf",80,self.ImageCustom[0],self.obj.WHITE,self.obj)
        self.thingchoice.rect.y = 150
        #index choices
        self.size_text = 0
        
    def HandleEvent(self):
        self.thingchoice.text= self.ImageCustom[self.size_text]
        self.rectbtnArrow.x = self.thingchoice.rect.right + 180
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEMOTION:
                if self.rectbtnHome.collidepoint(event.pos) or self.rectbtnRefund.collidepoint(event.pos) or self.rectbtnAudio.collidepoint(event.pos) or self.rectbtnArrow.collidepoint(event.pos):
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                else:
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.rectbtnHome.collidepoint(event.pos):
                    self.quitOpt=True
                    print(self.obj.ImgSet)
                if self.rectbtnAudio.collidepoint(event.pos):
                    self.obj.AUDIOFLAG=not self.obj.AUDIOFLAG
                    if not self.obj.AUDIOFLAG:
                        pygame.mixer.music.stop()
                    else:
                        pygame.mixer.music.play(-1)
                if self.rectbtnRefund.collidepoint(event.pos):
                    self.obj.SetDefaultIMG()
                if self.rectInput.collidepoint(event.pos):
                    filepath = filedialog.askopenfilename(title="Select file image .jpg or .png")
                    if filepath[-3:len(filepath)] in ("png","jpg"):
                        #File
                        self.obj.SetImg(self.thingchoice.text,filepath)
                    elif filepath == "":
                        #default
                        self.obj.SetImg(self.thingchoice.text,self.obj.ImgDF[self.thingchoice.text])
                    else:
                        #Error
                        self.obj.SetImg(self.thingchoice.text,"")
                if self.rectbtnArrow.collidepoint(event.pos):
                    self.size_text +=1
                    if self.size_text >= len(self.ImageCustom):
                        self.size_text=0
    def draw(self):
        self.screen.fill(self.obj.BLUE)
        #Caption
        self.optionLabel.draw(self.screen)
        self.screen.blit(self.btnHome,self.rectbtnHome)
        self.screen.blit(self.btnRefund,self.rectbtnRefund)
        if self.obj.AUDIOFLAG:
            self.screen.blit(self.btnaudio,self.rectbtnAudio)
        else:
            self.screen.blit(self.btnunadio,self.rectbtnAudio)
        if self.obj.ImgSet[self.thingchoice.text]==self.obj.ImgDF[self.thingchoice.text]:
            self.screen.blit(self.btnInputDF,self.rectInput)
            self.labelDefault.draw(self.screen)
        elif self.obj.ImgSet[self.thingchoice.text]!="":
            self.screen.blit(self.btnInputSC,self.rectInput)
            self.labelSuccess.draw(self.screen)
        else:
            self.screen.blit(self.btnInputDF,self.rectInput)
            self.labelError.draw(self.screen)
        self.thingchoice.draw(self.screen)
        self.screen.blit(self.btnArrow,self.rectbtnArrow)
        pygame.display.update()