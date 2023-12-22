from game import *
from option import *
from variables import *
def GameRun(obj):
    game = Game(obj)
    game.New()
    while game.playing:
        game.HandleEvents()
        game.update()
        game.draw()
        game.FPS()
def RunOption(obj):
    opt = Option(obj)
    while  not opt.quitOpt:
        opt.HandleEvent()
        opt.draw()
def main():
    pygame.init()
    pygame.font.init()
    pygame.mixer.init()
    #Variales
    gameVars = Variables()
    #Init file
    icon = pygame.image.load("asset/icon.jpg")
    pygame.display.set_icon(icon)
    pygame.mixer_music.load("asset/music.ogg")
    pygame.mixer.music.play(-1) 
    menuBackground = pygame.image.load("asset/background.jpg")
    btnPlay = LabelSelf("asset/font.otf",100,"PLAY",gameVars.WHITE,gameVars,gameVars.YELLOW)
    btnPlay.rect.y -=150
    btnOps = LabelSelf("asset/font.otf",100,"OPTION",gameVars.WHITE,gameVars,gameVars.YELLOW)
    btnQuit = LabelSelf("asset/font.otf",100,"QUIT",gameVars.WHITE,gameVars,gameVars.YELLOW)
    btnQuit.rect.y +=150
    screen = pygame.display.set_mode((gameVars.WIDTH,gameVars.HEIGHT))
    pygame.display.set_caption("MENU")
    menuQuit = False
    while not  menuQuit:
        menuBackground = pygame.image.load(gameVars.imgBG)
        gameVars.Update()
        mX,mY = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                menuQuit = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                if btnPlay.rect.collidepoint(mX,mY) :
                    GameRun(gameVars)
                if btnOps.rect.collidepoint(mX,mY) :
                    RunOption(gameVars)
                if btnQuit.rect.collidepoint(mX,mY):
                    menuQuit= True  
            if event.type == pygame.MOUSEMOTION:
                if btnPlay.rect.collidepoint(mX,mY) or btnOps.rect.collidepoint(mX,mY) or btnQuit.rect.collidepoint(mX,mY):
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                else:
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
            screen.fill(gameVars.WHITE)
            screen.blit(menuBackground,(0,0))
            btnPlay.draw(screen)
            btnOps.draw(screen)
            btnQuit.draw(screen)
            pygame.display.update()
    pygame.quit()
if __name__ == "__main__":
    main()