import math, copy, random, decimal, types, time

from cmu_112_graphics import *
from tkinter import *
from PIL import Image

class GameMode(Mode):
    def appStarted(mode):
        mode.player = Player(mode)
        mode.topObstacle = TopObstacle(mode)
        mode.bottomObstacle = BottomObstacle(mode)
        mode.obstaclePairs = []
        for i in range(-2, 3):
            topObstacle = TopObstacle(mode)
            bottomObstacle = BottomObstacle(mode)
            topObstacle.y += i*mode.height//10
            bottomObstacle.y += i*mode.height//10
            mode.obstaclePairs.append((topObstacle, bottomObstacle))
        mode.score = 0
        mode.timerDelay = 100
        mode.obstaclePairSelection = random.randint(0, 4)
    
    def timerFired(mode):
        mode.player.timerFired()
    
    def keyPressed(mode, event):
        mode.obstaclePairSelection = random.randint(0, 4) # temporary
        print(mode.obstaclePairSelection)
        
    def drawObstacle(mode, canvas):
        (top, bottom) = mode.obstaclePairs[mode.obstaclePairSelection]
        top.draw(canvas)
        bottom.draw(canvas)
        (top, bottom) = mode.obstaclePairs[(mode.obstaclePairSelection)]
        
    def redrawAll(mode, canvas):
        canvas.create_rectangle(0, 0, mode.width, mode.height, fill = "black")
        mode.player.draw(canvas)
        mode.drawObstacle(canvas)
        # mode.topObstacle.draw(canvas)
        # mode.bottomObstacle.draw(canvas)
        canvas.create_line(mode.width//2, 0, mode.width//2, mode.height, fill = "white")
        canvas.create_line(0, mode.height//2, mode.width, mode.height//2, fill = "white")

class Player(object):
    URL = "https://www.spriters-resource.com/resources/sheets/57/59894.png"
    sprites = []
    def __init__(self, mode):
        self.x = mode.width//2
        self.y = mode.height//2
        image = mode.loadImage(Player.URL)
        for i in range(0, 3):
            tempImage = image.crop((28*i, 512-28, 28*(i+1), 512))
            tempImage = mode.scaleImage(tempImage, 3)
            Player.sprites.append(tempImage)
        self.spriteSelection = 0
    
    def timerFired(self):
        self.spriteSelection += 1
        self.spriteSelection %= len(Player.sprites)

    def draw(self, canvas):
        sprite = Player.sprites[self.spriteSelection]
        canvas.create_image(self.x, self.y, image=ImageTk.PhotoImage(sprite))

class TopObstacle(object):
    URL = "https://www.spriters-resource.com/resources/sheets/57/59894.png"
    def __init__(self, mode):
        self.x = mode.width//2
        self.y = mode.height//100 - mode.height//8
        image = mode.loadImage(TopObstacle.URL)
        image = image.crop((56, 512 - 28 - 162, 56 + 28, 512 - 28))
        self.image = mode.scaleImage(image, 3)

    def draw(self, canvas):
        canvas.create_image(self.x, self.y, image=ImageTk.PhotoImage(self.image))

class BottomObstacle(TopObstacle):
    def __init__(self, mode):
        super().__init__(mode)
        image = mode.loadImage(TopObstacle.URL)
        image = image.crop((56+28, 512 - 28 - 162, 56 + 28 + 28, 512 - 28))
        self.image = mode.scaleImage(image, 3)
        self.y = 99*mode.height//100 + mode.height//8


class FlappyBird(ModalApp):
    def appStarted(app):
        #app.splashScreenMode = splashScreenMode()
        app.gameMode = GameMode()
        #app.helpMode = HelpMode()
        #app.gameOverMode = GameOverMode()
        app.setActiveMode(app.gameMode)

app = FlappyBird(width = 500, height = 700)