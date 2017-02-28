# play.py
# Du Chen (dc784) and Alan Pascual (ap835)
# 12/4/2016
"""Subcontroller module for Breakout

This module contains the subcontroller to manage a single game in the Breakout App. 
Instances of Play represent a single game.  If you want to restart a new game, you are 
expected to make a new instance of Play.

The subcontroller Play manages the paddle, ball, and bricks.  These are model objects.  
Their classes are defined in models.py.

Most of your work on this assignment will be in either this module or models.py.
Whether a helper method belongs in this module or models.py is often a complicated
issue.  If you do not know, ask on Piazza and we will answer."""
from constants import *
from game2d import *
from models import *


# PRIMARY RULE: Play can only access attributes in models.py via getters/setters
# Play is NOT allowed to access anything in breakout.py (Subcontrollers are not
# permitted to access anything in their parent. To see why, take CS 3152)

class Play(object):
    """An instance controls a single game of breakout.
    
    This subcontroller has a reference to the ball, paddle, and bricks. It animates the 
    ball, removing any bricks as necessary.  When the game is won, it stops animating.  
    You should create a NEW instance of Play (in Breakout) if you want to make a new game.
    
    If you want to pause the game, tell this controller to draw, but do not update.  See 
    subcontrollers.py from Lecture 25 for an example.
    
    INSTANCE ATTRIBUTES:
        _paddle [Paddle]: the paddle to play with 
        _bricks [list of Brick]: the list of bricks still remaining 
        _ball   [Ball, or None if waiting for a serve]:  the ball to animate
        _tries  [int >= 0]: the number of tries left 
    
    As you can see, all of these attributes are hidden.  You may find that you want to
    access an attribute in class Breakout. It is okay if you do, but you MAY NOT ACCESS 
    THE ATTRIBUTES DIRECTLY. You must use a getter and/or setter for any attribute that 
    you need to access in Breakout.  Only add the getters and setters that you need for 
    Breakout.
    
    You may change any of the attributes above as you see fit. For example, you may want
    to add new objects on the screen (e.g power-ups).  If you make changes, please list
    the changes with the invariants.
                  
    LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY
        _powerup    [Powerup or None]: the powerup currently on screen or None
        _power      [a string or None]: String of active power, None otherwise
        _extraball  [a list of Ball]: the list of extra balls from powerup
    """
    
    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    
    # INITIALIZER (standard form) TO CREATE PADDLES AND BRICKS
    def __init__(self):
        """Initializer: Creates Paddles and Bricks"""
        
        self._bricks = []
        for i in range(BRICK_ROWS):
            top = GAME_HEIGHT-BRICK_Y_OFFSET - (BRICK_HEIGHT + BRICK_SEP_V)*i
            if i % 10 == 0 or i % 10 == 1:
                color = colormodel.RED
            elif i % 10 == 2 or i % 10 == 3:
                color = colormodel.ORANGE
            elif i % 10 == 4 or i % 10 == 5:
                color = colormodel.YELLOW
            elif i % 10 == 6 or i % 10 == 7:
                color = colormodel.GREEN
            elif i % 10 == 8 or i % 10 == 9:
                color = colormodel.CYAN
            for k in range(BRICKS_IN_ROW):
                left = BRICK_SEP_H/2 + (BRICK_WIDTH + BRICK_SEP_H)*k
                brick = Brick(left=left,top=top,width=BRICK_WIDTH,
                height=BRICK_HEIGHT,linecolor=color,fillcolor=color)
                self._bricks.append(brick)
        self._paddle = Paddle(x=GAME_WIDTH/2,bottom=PADDLE_OFFSET,
        width=PADDLE_WIDTH,height=PADDLE_HEIGHT,linewidth=1,
        linecolor=colormodel.WHITE,fillcolor=colormodel.BLACK)
        self._extraball = []
        self._powerup = None
        self._power = None
    
    # UPDATE METHODS TO MOVE PADDLE, SERVE AND MOVE THE BALL
    def updatePaddle(self, input):
        """Updates the position of the paddle
        
        Parameter input: The user input
        Precondition: input must be an instance of GInput"""
        assert isinstance(input, GInput)
        self._paddle.movePaddle(input)
    
    def serveBall(self):
        """Creates and serves a ball"""
        color = random.choice([colormodel.RED,colormodel.BLUE,colormodel.GREEN])
        sy=GAME_HEIGHT-BRICK_Y_OFFSET-(BRICK_HEIGHT+BRICK_SEP_V)*BRICK_ROWS-50
        self._ball = Ball(x=GAME_WIDTH/2,y=sy,width=BALL_DIAMETER,
        height=BALL_DIAMETER,linewidth=1,linecolor=colormodel.WHITE,
        fillcolor=color)
    
    def updateBall(self):
        """Updates the position of the ball"""
        self._ball.moveBall()
        self._ball.bounce()
        self.moveMulti()
        self.collisions()
        self.finPowerP()
        self.finMulti()

    # DRAW METHOD TO DRAW THE PADDLES, BALL, AND BRICKS
    def drawBricks(self, view):
        """Draws Bricks
        
        Parameter view: The window to draw bricks to
        Precondition: view is a GView object"""
        assert isinstance(view, GView)
        for i in self._bricks:
            i.draw(view)
        
    def drawPaddle(self, view):
        """Draws paddle
        
        Parameter view: The window to draw paddle to
        Precondition: view is a GView object"""
        assert isinstance(view, GView)
        self._paddle.draw(view)
    
    def drawBall(self, view):
        """Draws ball
        
        Parameter view: The window to draw paddle to
        Precondition: view is a GView object"""
        assert isinstance(view, GView)
        self._ball.draw(view)
    
    # HELPER METHODS FOR PHYSICS AND COLLISION DETECTION
    def collisions(self):
        """This detects collisions for ball and adjusts velocity accordingly.
        If collides with brick, removes brick"""
        self._paddle.collides(self._ball)
        for i in self._bricks:
            if i.collides(self._ball,self._power) == True:
                if self._powerup == None and self._power == None:
                    chance = random.random()
                    if chance >= 0.2:
                        x = i.x
                        y = i.y
                        power = random.choice(["P","B"])
                        if power == "P":
                            color = colormodel.GREEN
                        elif power == "B":
                            color = colormodel.CYAN
                        self._powerup = Powerup(x=x,y=y,text=power,
                        font_name="Times.ttf",font_size=10,fillcolor=color,
                        width=20,height=10)
                self._bricks.remove(i)
            for k in self._extraball:
                self._paddle.collides(k)
                if i.collides(k,None) == True:
                    if i in self._bricks:
                        self._bricks.remove(i)
    
    def checkHitBottom(self):
        """Returns True if ball hits bottom boundary"""
        if self._ball.bottom <= 0:
            return True
    
    # ADD ANY ADDITIONAL METHODS (FULLY SPECIFIED) HERE
    def centerPaddle(self):
        """Recenters the paddle"""
        self._paddle.x = GAME_WIDTH/2
        self._paddle.y = PADDLE_OFFSET
    
    def noBricks(self):
        """Returns True if no bricks left"""
        if self._bricks == []:
            return True
    
    def updatePowerup(self):
        """"""
        if self._powerup != None:
            self._powerup.movePowerup()
            self.collisionPowerup()
    
    def collisionPowerup(self):
        """"""
        if self._paddle.paddlePower(self._powerup):
            self._power = self._powerup.text
            self.resetPowerup()
            if self._power == "B":
                self.createMulti()
        elif self._powerup.bottom <= 0:
            self.resetPowerup()
            
    def drawPowerup(self, view):
        """"""
        assert isinstance(view, GView)
        if self._powerup != None:
            self._powerup.draw(view)
            
    def resetPowerup(self):
        """"""
        self._powerup = None
    
    def resetPower(self):
        """"""
        if self._power == "B":
            self._extraball = []
        self._power = None
    
    def finPowerP(self):
        """"""
        if self._power == "P":
            if self._ball.top >= GAME_HEIGHT:
                self._power = None
    
    def createMulti(self):
        """"""
        x = self._ball.x
        y = self._ball.y
        color = colormodel.BLACK
        for i in range(5):
            exball = Ball(x=x,y=y,fillcolor=color,height=BALL_DIAMETER,
            width=BALL_DIAMETER,linewidth=1,linecolor=colormodel.WHITE)
            exball.setvx(random.uniform(1.0,5.0)*random.choice([-1, 1]))
            exball.setvy(random.uniform(3.0,5.0)*random.choice([-1,1]))
            self._extraball.append(exball)
    
    def moveMulti(self):
        """"""
        for i in self._extraball:
            i.moveBall()
            i.bounce()
    
    def drawMulti(self, view):
        """"""
        assert isinstance(view, GView)
        for i in self._extraball:
            i.draw(view)
    
    def finMulti(self):
        """"""
        for i in self._extraball:
            if i.bottom <= 0:
                self._extraball.remove(i)
        if self._extraball == [] and self._power == "B":
            self.resetPower()