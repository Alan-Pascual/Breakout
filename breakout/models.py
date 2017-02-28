# models.py
# Du Chen (dc784) and Alan Pascual (ap835)
# 12/4/2016
"""Models module for Breakout

This module contains the model classes for the Breakout game. That is anything that you
interact with on the screen is model: the paddle, the ball, and any of the bricks.

Technically, just because something is a model does not mean there has to be a special 
class for it.  Unless you need something special, both paddle and individual bricks could
just be instances of GRectangle.  However, we do need something special: collision 
detection.  That is why we have custom classes.

You are free to add new models to this module.  You may wish to do this when you add
new features to your game.  If you are unsure about whether to make a new class or 
not, please ask on Piazza."""
import random # To randomly generate the ball velocity
from constants import *
from game2d import *


# PRIMARY RULE: Models are not allowed to access anything except the module constants.py.
# If you need extra information from Play, then it should be a parameter in your method, 
# and Play should pass it as a argument when it calls the method.


class Paddle(GRectangle):
    """An instance is the game paddle.
    
    This class contains a method to detect collision with the ball, as well as move it
    left and right.  You may wish to add more features to this class.
    
    The attributes of this class are those inherited from GRectangle.
    
    LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY
    """
    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    
    # INITIALIZER TO CREATE A NEW PADDLE
    def __init__(self,**keywords):
        """**Constructor: Creates paddle object.
            
            :param keywords: dictionary of keyword arguments
            **Precondition**: See below.
        
        To use the constructor for this class, you should provide it with a 
        list of keyword arguments that initialize various attributes. Ensure 
        ensure that attributes linecolor and fillcolor are the same. For 
        example , to create a black paddle centered at (0,0), use the 
        constructor call:
        
            Paddle(x=0,y=0,width=10,height=10,fillcolor=colormodel.BLACK, 
            linecolor=colormodel.BLACK)"""
        
        self._defined = False
        GRectangle.__init__(self,**keywords)
        self._reset()
        self._defined = True
    
    # METHODS TO MOVE THE PADDLE AND CHECK FOR COLLISIONS
    def movePaddle(self, input):
        """Moves paddle with input
        
        Parameter input: The user input
        Precondition: input must be an instance of GInput"""
        assert isinstance(input, GInput)
        pos = self.x
        if input.is_key_down('right'):
            pos += 10
            self.x = min(GAME_WIDTH-PADDLE_WIDTH/2, pos)
        elif input.is_key_down('left'):
            pos -= 10
            self.x = max(0+PADDLE_WIDTH/2, pos)
    
    def collides(self,ball):
        """Returns: True if the ball collides with the paddle
        
        Parameter ball: The ball to check
        Precondition: ball is of class Ball"""
        assert isinstance(ball,Ball)
        bottom = ball.bottom
        left = ball.left
        right = ball.right
        x = ball.x
        if self.contains(left,bottom) or self.contains(right,bottom):
            ball.setvy(abs(ball.getvy()))
            if x == self.x:
                ball.setvx(0)
            elif x < self.x:
                ball.setvx((x-self.x)/5)
            elif x > self.x:
                ball.setvx((x-self.x)/5)
            return True
    
    # ADD MORE METHODS (PROPERLY SPECIFIED) AS NECESSARY
    def paddlePower(self,powerup):
        """Returns: True if the powerup collides with the paddle
        
        Parameter powerup: The powerup to check
        Precondition: powerup is of class Powerup"""
        assert isinstance(powerup,Powerup)
        bottom = powerup.bottom
        left = powerup.left
        right = powerup.right
        if self.contains(left,bottom) or self.contains(right,bottom):
            return True


class Brick(GRectangle):
    """An instance is the game paddle.
    
    This class contains a method to detect collision with the ball.  You may wish to 
    add more features to this class.
    
    The attributes of this class are those inherited from GRectangle.
    
    LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY
    """
    
    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    
    # INITIALIZER TO CREATE A BRICK
    def __init__(self,**keywords):
        """**Constructor: Creates brick object.
            
            :param keywords: dictionary of keyword arguments
            **Precondition**: See below.
        
        To use the constructor for this class, you should provide it with a 
        list of keyword arguments that initialize various attributes. Ensure 
        ensure that attributes linecolor and fillcolor are the same. For 
        example , to create a red brick centered at (0,0), use the constructor 
        call:
        
            Brick(x=0,y=0,width=10,height=10,fillcolor=colormodel.RED, linecolor
            =colormodel.RED)"""
        
        self._defined = False
        GRectangle.__init__(self,**keywords)
        self._reset()
        self._defined = True
        
    # METHOD TO CHECK FOR COLLISION
    def collides(self,ball,power):
        """Returns: True if the ball collides with this brick
        
        Parameter ball: The ball to check
        Precondition: ball is of class Ball
        
        Parameter power: The power to check
        Precondition: power is a str or None"""
        assert isinstance(ball,Ball)
        assert power == None or isinstance(power,str)
        top = ball.top
        bottom = ball.bottom
        left = ball.left
        right = ball.right
        y = ball.y
        y3v4 = ball.y + ball.width/2
        y1v4 = ball.y - ball.width/2
        if self.contains(left,top) and not self.contains(left,y):
            if power != "P":
                ball.setvy(abs(ball.getvy())*-1)
        elif self.contains(right,top) and not self.contains(right,y):
            if power != "P":
                ball.setvy(abs(ball.getvy())*-1)
        elif self.contains(left,bottom) and not self.contains(left,y):
            if power != "P":
                ball.setvy(abs(ball.getvy()))
        elif self.contains(right,bottom) and not self.contains(right,y):
            if power != "P":
                ball.setvy(abs(ball.getvy()))
        elif (self.contains(left,y3v4) or self.contains(left,y) or 
        self.contains(left,y1v4) or self.contains(left,bottom)):
            if power != "P":
                ball.setvx(abs(ball.getvx()))
        elif (self.contains(right,y3v4) or self.contains(right,y) or 
        self.contains(right,y1v4) or self.contains(right,bottom)):
            if power != "P":
                ball.setvx(abs(ball.getvx())*-1)
        else:
            return False
        return True
        
          
    # ADD MORE METHODS (PROPERLY SPECIFIED) AS NECESSARY


class Ball(GEllipse):
    """Instance is a game ball.
    
    We extend GEllipse because a ball must have additional attributes for velocity.
    This class adds this attributes and manages them.
    
    INSTANCE ATTRIBUTES:
        _vx [int or float]: Velocity in x direction 
        _vy [int or float]: Velocity in y direction 
    
    The class Play will need to look at these attributes, so you will need
    getters for them.  However, it is possible to write this assignment with no
    setters for the velocities.
    
    How? The only time the ball can change velocities is if it hits an obstacle
    (paddle or brick) or if it hits a wall.  Why not just write methods for these
    instead of using setters?  This cuts down on the amount of code in Gameplay.
    
    NOTE: The ball does not have to be a GEllipse. It could be an instance
    of GImage (why?). This change is allowed, but you must modify the class
    header up above.
    
    LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY
    """
    
    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    def getvx(self):
        """Returns the value of vx"""
        return self._vx
        
    def getvy(self):
        """Returns the value of vy"""
        return self._vy
        
    def setvx(self, val):
        """sets a new value for x velocity
        
        Parameter val: val is the velocity in x direction
        Precondition: val is an int or float"""
        assert isinstance(val, int) or isinstance(val, float)
        self._vx = val
    
    def setvy(self, val):
        """sets a new value for y velocity
        
        Parameter val: val is the velocity in y direction
        Precondition: val is an int or float"""
        assert isinstance(val, int) or isinstance(val, float)
        self._vy = val
    
    # INITIALIZER TO SET RANDOM VELOCITY
    def __init__(self,**keywords):
        """**Constructor**: Creates a new ball
        
            :param keywords: dictionary of keyword arguments 
            **Precondition**: See below.
        
        To use the constructor for this class, you should provide it with a list
        of keyword arguments that initialize various attributes. For example, to
        create a ball centered at (0,0), use the constructor call
        
            GEllipse(x=0,y=0,width=10,height=10,fillcolor=colormodel.RED,
            linecolor=colormodel.RED)
        
        This class supports the all same keywords as `GRectangle`."""
        self._defined = False
        self._vx = random.uniform(1.0,5.0) 
        self._vx = self._vx * random.choice([-1, 1])
        self._vy = -5.0
        GEllipse.__init__(self,**keywords)
        self._reset()
        self._defined = True
    
    # METHODS TO MOVE AND/OR BOUNCE THE BALL
    def moveBall(self):
        """Moves Ball with vx and vy"""
        self.x += self._vx
        self.y += self._vy
    
    def bounce(self):
        """Detects if ball hits game bounderies and reverses velocity according 
        to boundary
        
        If ball hits top, vy is negated. If ball hits left or right boundary,
        vx is negated."""
        if self.top >= GAME_HEIGHT:
            self._vy = abs(self.getvy())*-1
        if self.left <= 0:
            self._vx = abs(self.getvx())
        elif self.right >= GAME_WIDTH:
            self._vx = abs(self.getvx())*-1
    
    # ADD MORE METHODS (PROPERLY SPECIFIED) AS NECESSARY

    
# IF YOU NEED ADDITIONAL MODEL CLASSES, THEY GO HERE
class Powerup(GLabel):
    """Instance is a game powerup
    
    We extend GLabel because a powerup must have an additional attribute for
    velocity. This class adds this attribute and manages it.
    
    INSTANCE ATTRIBUTES:
        _vy [int or float]: velocity in the y direction
    
    """
    
    # GETTERS AND SETTERS
    
    # INITIALIZER
    def __init__(self,**keywords):
        """"""
        self._defined = False
        self._vy = -2.0
        GLabel.__init__(self,**keywords)
        self._reset()
        self._defined = True
    
    # METHODS TO MOVE THE POWERUP
    def movePowerup(self):
        """"""
        self.y += self._vy