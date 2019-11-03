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
        randomInt = random.randint(0,4)
        mode.obstaclesVisible = []
        mode.obstaclesVisible.append(mode.obstaclePairs[randomInt])
        mode.score = 0
        mode.timerDelay = 300
        mode.obstaclePairSelection = random.randint(0, 4)
        mode.scrollX  = - mode.width // 2

    @staticmethod
    def checkPlayerBounds(mode):
        playerBounds = mode.player.getPlayerBounds(mode)
        for obstacle in mode.obstaclesVisible:
            topObstacleBounds = obstacle[0].getObstacleBounds(mode)
            bottomObstacleBounds = obstacle[1].getObstacleBounds(mode)
            if GameMode.boundsIntersect(mode, playerBounds, topObstacleBounds): return True
            elif GameMode.boundsIntersect(mode, playerBounds, bottomObstacleBounds): return True
        return False

    @staticmethod
    def boundsIntersect(mode, bound1, bound2):
        (ax0, ay0, ax1, ay1) = bound1
        (bx0, by0, bx1, by1) = bound2
        return (((ax0 < bx0 < ax1) and (ay0 < by0 < ay1)) or ((ax0 < bx1 < ax1) and (ay0 < by0 < ay1)) or 
                ((ax0 < bx0 < ax1) and (ay0 < by1 < ay1)) or ((ax0 < bx1 < ax1) and (ay0 < by1 < ay1)) or 
                ((bx0 < ax0 < ax1 < bx1) and (ay0 < by0 < ay1)) or (( bx0 < ax0 < ax1 < bx1) and (ay0 < by1 < ay1)) or
                ((ax0 < bx0 < ax1) and (by0 < ay0 < ay1 < by1)) or ((ax0 < bx1 < ax1) and (by0 < ay0 < ay1 < by1)))

    
    def timerFired(mode):
        mode.player.timerFired()
        mode.scrollX += 10
        for (obstacle, bottom) in mode.obstaclesVisible:
            if (obstacle.x - mode.scrollX) < (- obstacle.width):
                mode.obstaclePairSelection = random.randint(0, 4) # temporary
                mode.obstaclesVisible.pop()
                # randomInt = random.randint(0,4)
                mode.obstaclesVisible.append(mode.obstaclePairs[mode.obstaclePairSelection])
                mode.scrollX = -mode.width//2
        if GameMode.checkPlayerBounds(mode) == True:
            mode.app.setActiveMode(mode.app.gameOverMode)
        
    
    def keyPressed(mode, event):
        # mode.obstaclePairSelection = random.randint(0, 4) # temporary
        print(mode.obstaclePairSelection)
        if event.key == "Space":
            mode.player.jump(mode)
        
    def drawObstacle(mode, canvas):
        (top, bottom) = mode.obstaclePairs[mode.obstaclePairSelection]
        top.draw(mode, canvas)
        bottom.draw(mode, canvas)
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
        self.width = 28 * 3
        self.dy = 5
        self.jumpY = - 40

    def getPlayerBounds(self, mode):
        return (self.x - self.width // 2, self.y - self.width // 2, self.x + self.width // 2, self.y + self.width // 2)


    def jump(self, mode):
        self.y += self.jumpY
    
    def timerFired(self):
        self.spriteSelection += 1
        self.spriteSelection %= len(Player.sprites)
        self.y += self.dy

    def draw(self, canvas):
        sprite = Player.sprites[self.spriteSelection]
        canvas.create_image(self.x, self.y, image=ImageTk.PhotoImage(sprite))

class TopObstacle(object):
    URL = "https://www.spriters-resource.com/resources/sheets/57/59894.png"
    def __init__(self, mode):
        self.mode = mode
        self.x = mode.width//2
        self.y = mode.height//100 - mode.height//8
        self.width = 28
        image = mode.loadImage(TopObstacle.URL)
        image = image.crop((56, 512 - 28 - 162, 56 + 28, 512 - 28))
        self.image = mode.scaleImage(image, 3)
    
    def getObstacleBounds(self, mode):
        return (self.x - self.mode.scrollX , 0, self.x  - self.mode.scrollX, self.y +mode.obstaclesVisible[0][0].y)
        
            # return (self.x - self.mode.scrollX - self.width // 2, 0, self.x + self.width // 2  - self.mode.scrollX, self.y + (162))

    def draw(self, mode, canvas):
        canvas.create_image(self.x - self.mode.scrollX, self.y, image=ImageTk.PhotoImage(self.image))
        canvas.create_oval(self.x - self.mode.scrollX -20, self.y-20, self.x   - self.mode.scrollX+20, self.y+20, fill='red')

class BottomObstacle(TopObstacle):
    def __init__(self, mode):
        super().__init__(mode)
        image = mode.loadImage(TopObstacle.URL)
        image = image.crop((56+28, 512 - 28 - 162, 56 + 28 + 28, 512 - 28))
        self.image = mode.scaleImage(image, 3)
        self.y = 99*mode.height//100 + mode.height//8

class GameOverMode(Mode):
    def redrawAll(mode, canvas):
        canvas.create_text(mode.width //2 , 10, text = "Game Over")

class FlappyBird(ModalApp):
    def appStarted(app):
        #app.splashScreenMode = splashScreenMode()
        app.gameMode = GameMode()
        #app.helpMode = HelpMode()
        app.gameOverMode = GameOverMode()
        app.setActiveMode(app.gameMode)

app = FlappyBird(width = 500, height = 700)
