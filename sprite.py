import pygame
class Tile(pygame.sprite.Sprite):
    def __init__(self,game,x,y,tuple,obj,path_image ="asset/lv1.jpg",) :
        self.obj = obj
        self.x ,self.y =x,y
        self.tuple = tuple
        self.image_source = pygame.image.load(path_image)
        self.image_source = pygame.transform.scale(self.image_source,(self.obj.LIMITSIZE,self.obj.LIMITSIZE))
        self.groups = game.all_sprites
        #Constructor
        pygame.sprite.Sprite.__init__(self,self.groups)
        self.game= game
        #Surface
        self.image= pygame.Surface((int(self.obj.LIMITSIZE/self.obj.LEVEL),int(self.obj.LIMITSIZE/self.obj.LEVEL)))
        #Subsurface from imgsoucre
        self.image_crop = self.image_source.subsurface(self.tuple[1]  * int(self.obj.LIMITSIZE/self.obj.LEVEL) ,self.tuple[0] * int(self.obj.LIMITSIZE/self.obj.LEVEL),int(self.obj.LIMITSIZE/self.obj.LEVEL) ,int(self.obj.LIMITSIZE/self.obj.LEVEL))
        self.rect = self.image_crop.get_rect()
        if self.tuple != (self.obj.LEVEL-1,self.obj.LEVEL-1):
            self.image.blit(self.image_crop,(0,0))
        else :
            self.image.fill(self.obj.WHITE)
            img= pygame.transform.scale(self.image_source,(int(self.obj.LIMITSIZE/self.obj.LEVEL)-15,int(self.obj.LIMITSIZE/self.obj.LEVEL)-15))
            img_rect = img.get_rect(center=(int(self.obj.LIMITSIZE/self.obj.LEVEL)/2,int(self.obj.LIMITSIZE/self.obj.LEVEL)/2))
            self.image.blit(img,(img_rect.x,img_rect.y))
    def update(self):
        self.rect.x = self.x  * int(self.obj.LIMITSIZE/self.obj.LEVEL) + self.game.x
        self.rect.y = self.y  * int(self.obj.LIMITSIZE/self.obj.LEVEL) + self.game.y
    def click(self,mouse_x,mouse_y):
        return self.rect.left <= mouse_x <= self.rect.right and self.rect.top<= mouse_y<= self.rect.bottom
class LabelSelf():
    def __init__(self,pathfont,sizefont,text,colortext,obj,BG=None) :
        self.obj = obj
        self.size= sizefont
        self.font = pygame.font.Font(pathfont,self.size)
        self.text = text
        self.colortext= colortext
        if BG is None:
            self.label = self.font.render(text,True,colortext)
        else :
            self.label = self.font.render(text,True,colortext,BG)
        self.rect = self.label.get_rect(center=(self.obj.WIDTH/2,self.obj.HEIGHT/2))
    def draw(self,screen):
        self.label=self.font.render(self.text,True,self.colortext)
        screen.blit(self.label,self.rect)
