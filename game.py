import pygame,sys
from queue import PriorityQueue
from copy import  deepcopy
import random
from sprite import *
from variables import *
import threading
#FUNCTION OPERATOR
def Swap(arr,tuple1,tuple2):
    x,y = tuple1
    m,n = tuple2
    arr[x][y] ,arr[m][n] = arr[m][n],arr[x][y]
#DECLARE NODE
class Node:
    def __init__(self,value,x,y,lv,par =None, g=0, h=0,way='') :
        self.value= deepcopy(value)
        self.par=par
        self.x= x
        self.y =y
        self.g=g
        self.h=h
        self.Level = lv
        self.way =way
    def CanRight(self):
        return self.x < self.Level
    def CanLeft(self):
        return self.x > 0
    def CanUp(self):
        return self.y > 0
    def CanDown(self):
        return self.y < self.Level
    def Right(self):
        vl = deepcopy(self.value)
        Swap(vl,(self.y,self.x),(self.y,self.x+1))
        return vl
    def Left(self):
        vl = deepcopy(self.value)
        Swap(vl,(self.y,self.x),(self.y,self.x-1))
        return vl
    def Up(self):
        vl = deepcopy(self.value)
        Swap(vl,(self.y,self.x),(self.y-1,self.x))
        return vl
    def Down(self):
        vl = deepcopy(self.value)
        Swap(vl,(self.y,self.x),(self.y+1,self.x))
        return vl
    def __lt__(self, other):
        if other == None:
            return False
        return self.g + self.h < other.g + other.h
#Heurictis declaration
def Heurictis(arrr2d):
    S =0
    for row,value in enumerate(arrr2d):
        for col, vl  in enumerate(value):
            if arrr2d[row][col] != (row,col):
                S+=1
    return S 
# DECLARE GAME OBJECT
class Game:
    def __init__(self,obj) :
        if not pygame.get_init():
            pygame.init()
        if not pygame.mixer.get_init():
            pygame.mixer.init()
        if not pygame.font.get_init():
            pygame.font.init()
        self.obj =obj
        self.path_image = self.obj.imgCurrent
        self.screen=pygame.display.set_mode((self.obj.WIDTH,self.obj.HEIGHT))
        pygame.display.set_caption(self.obj.title)
        self.clock = pygame.time.Clock()
        self.playing = True
         # Position Begin
        self.y = 100
        self.x = int(self.obj.WIDTH/2 - 384 /2)
        #Track Positon missing image
        self.misIMGpostion_X = self.obj.LEVEL -1
        self.misIMGpostion_Y = self.obj.LEVEL -1
        #Hint 
        self.hintGame= []
        self.hintGameRV =[]
        self.HintFl = False
        self.hintLength=0
        #Max state
        self.MAXSTATE = 2500
    def RandGame(self):
        try:
            maxstep = random.randrange(35,45)
            for i in range(0,maxstep):
                K=random.randrange(0,4)
                if K==0 :
                    self.Up()
                elif K==1:
                    self.Right()
                elif K ==2 :
                    self.Down()
                elif K==3 :
                    self.Left()
            return True
        except IndexError as e:
            return False
    def createGame(self):
        grid= [[(row,col) for col in range(self.obj.LEVEL)] for row in range(self.obj.LEVEL)]
        return grid
    def New(self):
        #home button
        self.btnHome = pygame.image.load("asset/btnhome.png")
        self.rectbtnHome = self.btnHome.get_rect(center=(self.obj.WIDTH/2,self.obj.HEIGHT/2))
        self.rectbtnHome.x= 10
        self.rectbtnHome.y= 10
        #Refresh button
        self.btnpass = pygame.image.load("asset/pass.png")
        self.rectbtnpass = self.btnpass.get_rect(center=(self.obj.WIDTH/2,self.obj.HEIGHT/2))
        self.rectbtnpass.x= self.obj.WIDTH- (self.rectbtnpass.width +10 )
        self.rectbtnpass.y= 10
        #Hint button
        self.btnHint = pygame.image.load("asset/hint.png")
        self.rectbtnHint = self.btnHint.get_rect(center=(self.obj.WIDTH/2,self.obj.HEIGHT/2))
        self.rectbtnHint.y=10
        #Level Label
        self.lvLabel = LabelSelf("asset/font.otf",35,f"Level {self.obj.LEVEL - 1}",self.obj.BLACK,self.obj)
        self.lvLabel.rect.y =20
        self.rectbtnHint.x= self.lvLabel.rect.right +15
        #needed thing
        self.all_sprites= pygame.sprite.Group()
        self.tiles_grid = self.createGame()
        self.RandGame()
        self.tiles_grid_completed= self.createGame()
        self.CheckComplete = False
        self.obj.Update()
        self.path_image = self.obj.imgCurrent
        #finish image
        self.finishedImage = pygame.image.load(self.path_image)
        self.finishedImage = pygame.transform.scale(self.finishedImage,(self.obj.LIMITSIZE,self.obj.LIMITSIZE))
        self.rectfinishedImg= self.finishedImage.get_rect()
        self.rectfinishedImg.x=self.x
        self.rectfinishedImg.y=self.y
        #button left
        self.btnLArrow = pygame.image.load("asset/arrow_left.png")
        self.rectbtnLArrow = self.btnLArrow.get_rect(center=(self.obj.WIDTH/2,self.obj.HEIGHT/2))
        self.rectbtnLArrow.x = 250
        self.rectbtnLArrow.y= 495
        #button right
        self.btnRArrow = pygame.image.load("asset/arrow.png")
        self.rectbtnRArrow = self.btnRArrow.get_rect(center=(self.obj.WIDTH/2,self.obj.HEIGHT/2))
        self.rectbtnRArrow.y= 495
        self.rectbtnRArrow.x = 500
        #step label
        self.stepLB = LabelSelf("asset/font.otf",80,f"0",self.obj.BLACK,self.obj)
        self.stepLB.rect.y = 480
        self.draw_tiles()
    def draw_tiles(self):
        self.tiles= []
        for row , x in enumerate(self.tiles_grid):
            self.tiles.append([])
            for col, tuple in enumerate(x):
                self.tiles[row].append(Tile(self,col,row,tuple,self.obj,self.path_image))
    def FPS(self):
        # self.clock.tick(self.obj.FPS)
        pass
    def update(self):
        self.all_sprites.update()
        if self.tiles_grid== self.tiles_grid_completed:
            self.CheckComplete=True
        else:
            self.CheckComplete=False
        if threading.active_count()>1:
            print("Second Flow")
    def draw_grid(self):
        if not self.CheckComplete:
            # thickness
            indexthickness = 4
            #draw Y
            for col in range(self.x,self.obj.LIMITSIZE+self.x+1,int(self.obj.LIMITSIZE/self.obj.LEVEL)):
                pygame.draw.line(self.screen,self.obj.WHITE,(col,self.y),(col,self.obj.LIMITSIZE+self.y),indexthickness)
            # draw X
            for row in range(self.y,self.obj.LIMITSIZE+100+1,int(self.obj.LIMITSIZE/self.obj.LEVEL)):
                pygame.draw.line(self.screen,self.obj.WHITE,(self.x,row),(self.obj.LIMITSIZE+self.x,row),indexthickness)
        else:
            pass
    def draw(self):
        self.screen.fill(self.obj.WHITE)
        self.all_sprites.draw(self.screen)
        self.draw_grid()
        self.screen.blit(self.btnpass,self.rectbtnpass)
        if self.HintFl:
            self.screen.blit(self.btnLArrow,self.rectbtnLArrow)
            self.screen.blit(self.btnRArrow,self.rectbtnRArrow)
            self.stepLB.draw(self.screen)
        else:
            self.screen.blit(self.btnHome,self.rectbtnHome)
            self.screen.blit(self.btnHint,self.rectbtnHint)
        self.lvLabel.draw(self.screen)
        if self.CheckComplete:
            self.screen.blit(self.finishedImage,self.rectfinishedImg)
        pygame.display.update()
    def ChuanHoa(self):
        for value in self.hintGame:
            if value =='u':
                self.hintGameRV.append('d')
            elif value=='d':
                self.hintGameRV.append('u')
            elif value == 'r':
                self.hintGameRV.append('l')
            elif value== 'l':
                self.hintGameRV.append('r')
    def OperatorGame(self,indx,flag=True):
        if flag==True:
            if self.hintGame[indx] =='u':
                self.Up()
            elif self.hintGame[indx]=='d':
                self.Down()
            elif self.hintGame[indx]=='l':
                self.Left()
            elif self.hintGame[indx] == 'r':
                self.Right()
        else:
            if self.hintGameRV[indx] =='u':
                self.Up()
            elif self.hintGameRV[indx]=='d':
                self.Down()
            elif self.hintGameRV[indx]=='l':
                self.Left()
            elif self.hintGameRV[indx] == 'r':
                self.Right()
    def LeftArrow(self):
        if self.hintLength != 0:
            self.OperatorGame(self.hintLength-1,False)
            self.hintLength -=1
            self.draw_tiles()
        self.stepLB.text= str(self.hintLength)
    def RightArrow(self):
        if self.hintLength != len(self.hintGame): 
            self.OperatorGame(self.hintLength)
            self.draw_tiles()
            self.hintLength+=1
        self.stepLB.text= str(self.hintLength)
    def HandleEvents(self):
        try:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEMOTION:
                    mouseX,mouseY = pygame.mouse.get_pos()
                    if (self.x <= mouseX <= self.x + self.obj.LIMITSIZE and self.y <= mouseY<= self.y + self.obj.LIMITSIZE) or (self.rectbtnHome.collidepoint(event.pos) and not self.HintFl) or self.rectbtnpass.collidepoint(event.pos) or (self.rectbtnHint.collidepoint(event.pos) and not self.HintFl) or (self.HintFl and (self.rectbtnLArrow.collidepoint(event.pos) or self.rectbtnRArrow.collidepoint(event.pos))):                    
                        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                    else:
                        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
                if event.type == pygame.KEYDOWN :
                    if event.key in (pygame.K_UP,pygame.K_w):
                        if not self.HintFl:                    
                            self.Up()
                    if event.key in (pygame.K_DOWN,pygame.K_s):
                        if not self.HintFl:
                            self.Down()
                    if event.key  in (pygame.K_LEFT,pygame.K_a):
                        if not self.HintFl:                    
                            self.Left()
                        else:
                            self.LeftArrow()
                    if event.key  in (pygame.K_RIGHT,pygame.K_d):
                        if not self.HintFl:                        
                            self.Right()
                        else:
                            self.RightArrow()
                    self.draw_tiles()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouseX,mouseY = pygame.mouse.get_pos()
                    if self.rectbtnHome.collidepoint(event.pos) and not self.HintFl:
                        self.playing= False
                    if self.rectbtnHint.collidepoint(event.pos) and not self.HintFl:
                        self.Hint()
                    if self.rectbtnLArrow.collidepoint(event.pos) and self.HintFl:
                        self.LeftArrow()
                    if self.rectbtnRArrow.collidepoint(event.pos) and self.HintFl:
                        self.RightArrow()
                    if self.rectbtnpass.collidepoint(event.pos):
                        if self.CheckComplete:
                            #Reset and update
                            self.stepLB.text='0'
                            self.HintFl = False
                            self.hintLength =0
                            self.hintGame.clear()
                            self.hintGameRV.clear()
                            self.obj.LEVEL+=1
                            self.tiles_grid = self.createGame()
                            self.misIMGpostion_X = self.obj.LEVEL -1
                            self.misIMGpostion_Y = self.obj.LEVEL -1
                            self.RandGame()
                            self.tiles_grid_completed= self.createGame()
                            self.lvLabel.text = f"LEVEL {self.obj.LEVEL -1}"
                            self.obj.Update()
                            self.path_image = self.obj.imgCurrent
                            #finish image
                            self.finishedImage = pygame.image.load(self.path_image)
                            self.finishedImage = pygame.transform.scale(self.finishedImage,(self.obj.LIMITSIZE,self.obj.LIMITSIZE))
                            self.rectfinishedImg= self.finishedImage.get_rect()
                            self.rectfinishedImg.x=self.x
                            self.rectfinishedImg.y=self.y
                            self.draw_tiles()
                        else:
                            print("Not Finished")
                    for row , tls in enumerate(self.tiles):
                        for col,tile in enumerate(tls):
                            if tile.click(mouseX, mouseY) and not self.HintFl:
                                #Left
                                if (row<=self.obj.LEVEL-1 and col <self.obj.LEVEL-1) and self.tiles_grid[row][col + 1] == (self.obj.LEVEL-1,self.obj.LEVEL-1):
                                    self.Left()
                                #Right
                                if (row<=self.obj.LEVEL-1 and col >0) and self.tiles_grid[row][col - 1] == (self.obj.LEVEL-1,self.obj.LEVEL-1):
                                    self.Right()
                                #Down
                                if (row>0 and col <=self.obj.LEVEL-1) and self.tiles_grid[row - 1][col] == (self.obj.LEVEL-1,self.obj.LEVEL-1):
                                    self.Down()
                                #Up
                                if (row <self.obj.LEVEL-1 and col <=self.obj.LEVEL-1) and self.tiles_grid[row + 1][col] == (self.obj.LEVEL-1,self.obj.LEVEL-1):
                                    self.Up()
                                self.draw_tiles()
                                # print(f"Matrix Loading{self.tiles_grid}")
        except Exception as ex:
            print(ex)
    def Up(self):
        if(self.misIMGpostion_Y>0):
            Swap(self.tiles_grid,(self.misIMGpostion_Y,self.misIMGpostion_X),(self.misIMGpostion_Y-1,self.misIMGpostion_X))
            self.misIMGpostion_X = self.misIMGpostion_X
            self.misIMGpostion_Y = self.misIMGpostion_Y-1
    def Right(self):
        if (self.misIMGpostion_X<self.obj.LEVEL -1):
            Swap(self.tiles_grid,(self.misIMGpostion_Y,self.misIMGpostion_X),(self.misIMGpostion_Y,self.misIMGpostion_X+1))
            self.misIMGpostion_X = self.misIMGpostion_X+1
            self.misIMGpostion_Y = self.misIMGpostion_Y
    def Down(self):
        if (self.misIMGpostion_Y<self.obj.LEVEL -1):
            Swap(self.tiles_grid,(self.misIMGpostion_Y,self.misIMGpostion_X),(self.misIMGpostion_Y+1,self.misIMGpostion_X))
            self.misIMGpostion_X = self.misIMGpostion_X
            self.misIMGpostion_Y = self.misIMGpostion_Y+1
    def Left(self):
        if (self.misIMGpostion_X> 0):
            Swap(self.tiles_grid,(self.misIMGpostion_Y,self.misIMGpostion_X),(self.misIMGpostion_Y,self.misIMGpostion_X-1))
            self.misIMGpostion_X = self.misIMGpostion_X-1
            self.misIMGpostion_Y = self.misIMGpostion_Y
    def Hint(self):
        self.HintFl = True
        p1 = threading.Thread(target=self.AStar).start()
    #Get path
    def getPath(self,O=Node):
        if O.way !='':
            self.hintGame.append(O.way)
        if O.par != None:
            self.getPath(O.par)
        else:
            self.hintGame.reverse()
        return
    def AStar(self):
        Start = Node(self.tiles_grid,self.misIMGpostion_X,self.misIMGpostion_Y,self.obj.LEVEL-1)
        Open = PriorityQueue()
        CLosed = PriorityQueue()
        Open.put(Start)
        i=1
        while True:
            if Open.empty():
                print("EMpty")
                return
            u = Open.get()
            print(f"Trang thai {i}  Chi Phi {u.g} {u.h}")
            i+=1
            if i == self.MAXSTATE:
                print("GIOI HAN")
                self.HintFl=False
                return
            CLosed.put(u)
            if u.value == self.tiles_grid_completed:
                print("Thanh cong")
                self.getPath(u)
                print(self.hintGame)
                self.ChuanHoa()
                return
            if u.CanUp():
                value = u.Up()
                h = Heurictis(value)
                v = Node(value,deepcopy(u.x),deepcopy(u.y-1),u.Level,u,u.g+1,h,'u')
                if v  not  in (CLosed.queue):
                    Open.put(v)
            if u.CanDown():
                value = u.Down()
                h = Heurictis(value)
                v = Node(value,deepcopy(u.x),deepcopy(u.y+1),u.Level,u,u.g+1,h,'d')
                if v  not  in (CLosed.queue):
                    Open.put(v)
            if u.CanRight():
                value = u.Right()
                h = Heurictis(value)
                v = Node(value,deepcopy(u.x+1),deepcopy(u.y),u.Level,u,u.g+1,h,'r')
                if v  not  in (CLosed.queue):
                    Open.put(v)
            if u.CanLeft():
                value = u.Left()
                h = Heurictis(value)
                v = Node(value,deepcopy(u.x-1),deepcopy(u.y),u.Level,u,u.g+1,h,'l')
                if v  not  in (CLosed.queue):
                    Open.put(v)
# v= Variables()
# game = Game(v)
# game.New()
# while game.playing:
#     game.HandleEvents()
#     game.update()
#     game.draw()
#     game.FPS()
