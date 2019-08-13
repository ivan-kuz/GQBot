import random

class Game():
    def __init__(self):
        self.frameTime = 1
        self.startSize = 4
        self.snake = [(2,5),(3,5),(4,5),(5,5)]
        self.xVect = 1
        self.yVect = 0
        self.apple = (5,5)
        self.bSize = 11
        self.running = True
        self.plantApple()
        self.render()
    
    def update(self):
        if not self.running:
            return
        self.snake.append((self.snake[-1][0]+self.xVect, self.snake[-1][1]+self.yVect))
        snake = self.snake[-1]
        if self.snake[-1] in self.snake[:-1] or snake[0] >= self.bSize or snake[1] >= self.bSize or snake[0] < 0 or snake[1] < 0:
            self.running = False
            self.snake.pop(0)
            return
        if not self.apple in self.snake:
            self.snake.pop(0)
        else:
            self.plantApple()
        self.render()
    
    def plantApple(self):
        while self.apple in self.snake:
            self.apple = (random.randint(0,self.bSize-1), random.randint(0,self.bSize-1))
    
    def render(self):
        self.renderString = ""
        for i in range(self.bSize+2):
            self.renderString += "$ "
        self.renderString+="\n"
        for y in range(self.bSize):
            self.renderString += "$ "
            for x in range(self.bSize):
                self.renderString += "@ " if self.apple == (x,y) else ("# " if (x,y) in self.snake else "  ")
            self.renderString += "$\n"
        for i in range(self.bSize+2):
            self.renderString += "$ "
