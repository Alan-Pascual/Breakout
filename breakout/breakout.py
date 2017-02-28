# breakout.py
# Du Chen (dc784) and Alan Pascual (ap835)
# 12/4/2016

# Used subcontroller.py, animation.py, arrows.py, touch.py, and state.py as reference
# Disclaimer: I do not claim ownership of any of the soundtrack or images
# Credit to Walker White for the amazing background photo!
# Credit for background music 1: Astley, Rick. "Never Gonna Give You Up"
# Credit for background music 2: Fabulous Secret Powers - created by Ryan Haines & Jay Allen, 2005, SLACKCiRCUS youtu.be/FR7wOGyAzpw
# Credit for background music 3: user daniwell. "Nyanyanyanyanyanyanya!"
# Credit for background music 4: Armstrong Louis. "What a Wonderful World"
# Credit for background music 5: 
# Credit for background music 6: SunStroke Project. "Run Away"
# Joe Biden picture was found on http://www.today.com/money/photo-sad-joe-biden-staring-out-window-sparks-hilarious-memes-1D80342655
# Michael Jordan picture was found on http://www.npr.org/sections/thetwo-way/2016/03/31/472330783/the-evolution-of-the-michael-jordan-crying-face-meme

"""Primary module for Breakout application

This module contains the main controller class for the Breakout application. There is no
need for any any need for additional classes in this module.  If you need more classes, 
99% of the time they belong in either the play module or the models module. If you 
are ensure about where a new class should go, 
post a question on Piazza."""
from constants import *
from game2d import *
from play import *


# PRIMARY RULE: Breakout can only access attributes in play.py via getters/setters
# Breakout is NOT allowed to access anything in models.py

class Breakout(GameApp):
    """Instance is the primary controller for the Breakout App
    
    This class extends GameApp and implements the various methods necessary for processing 
    the player inputs and starting/running a game.
    
        Method start begins the application.
        
        Method update either changes the state or updates the Play object
        
        Method draw displays the Play object and any other elements on screen
    
    Because of some of the weird ways that Kivy works, you SHOULD NOT create an
    initializer __init__ for this class.  Any initialization should be done in
    the start method instead.  This is only for this class.  All other classes
    behave normally.
    
    Most of the work handling the game is actually provided in the class Play.
    Play should have a minimum of two methods: updatePaddle(input) which moves
    the paddle, and updateBall() which moves the ball and processes all of the
    game physics. This class should simply call that method in update().
    
    The primary purpose of this class is managing the game state: when is the 
    game started, paused, completed, etc. It keeps track of that in an attribute
    called _state.
    
    INSTANCE ATTRIBUTES:
        view    [Immutable instance of GView; it is inherited from GameApp]:
                the game view, used in drawing (see examples from class)
        input   [Immutable instance of GInput; it is inherited from GameApp]:
                the user input, used to control the paddle and change state
        _state  [one of STATE_INACTIVE, STATE_COUNTDOWN, STATE_PAUSED, STATE_ACTIVE]:
                the current state of the game represented a value from constants.py
        _game   [Play, or None if there is no game currently active]: 
                the controller for a single game, which manages the paddle, ball, and bricks
        _mssg   [GLabel, or None if there is no message to display]
                the currently active message
    
    STATE SPECIFIC INVARIANTS: 
        Attribute _game is only None if _state is STATE_INACTIVE.
        Attribute _mssg is only None if  _state is STATE_ACTIVE or STATE_COUNTDOWN.
    
    For a complete description of how the states work, see the specification for the
    method update().
    
    You may have more attributes if you wish (you might need an attribute to store
    any text messages you display on the screen). If you add new attributes, they
    need to be documented here.
    
    LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY
        _timeframe      [an int >=0]:
                        Keeps track of time as frames
        _lives          [an int >=0]:
                        The amount of lives the player has
        _temptime       [an int]:
                        A temporary time keeper, in frames, can be negative
        _background     [a GImage]:
                        The attribute for the background of the game
        _backgroundlst  [a list of GImages]:
                        list of backgrounds to cycle through
        _cyclecount     [an int >=0]:
                        a counter to keep track of what cycle game on
        _tracknum       [an int >=0]:
                        stores current track number for the game
        _backtracklst   [a list of Sound objects]:
                        list of background tracks wav files to cycle through
        _soundtoggle    [a boolean]:
                        True if music on False for off
        _prev_space     [a boolean]:
                        True if 'spacebar' key was pressed, else False
        _prev_p         [a boolean]:
                        True if 'p' key was pressed, else False
    """
    
    # DO NOT MAKE A NEW INITIALIZER!
    
    # THREE MAIN GAMEAPP METHODS
    def start(self):
        """Initializes the application.
        
        This method is distinct from the built-in initializer __init__ (which you 
        should not override or change). This method is called once the game is running. 
        You should use it to initialize any game specific attributes.
        
        This method should make sure that all of the attributes satisfy the given 
        invariants. When done, it sets the _state to STATE_INACTIVE and create a message 
        (in attribute _mssg) saying that the user should press to play a game."""
        # IMPLEMENT ME
        self._state = STATE_INACTIVE
        self._game = None
        self._GLabelmssg("WARNING!\nPlay if you dare!\nThis game is KANCER!\n" +
        "Press any key to play\nToggle music: space\nPause: p\nPress ESC to exit")
        self._timeframe = 0
        self._lives = NUMBER_TURNS
        self._temptime = -30
        self._backgroundlst = [GImage(x=GAME_WIDTH/2,y=GAME_HEIGHT/2,
        source="walker.png",height=GAME_HEIGHT,width=GAME_WIDTH), 
        GImage(x=GAME_WIDTH/2,y=GAME_HEIGHT/2, source="biden.png",
        height=GAME_HEIGHT,width=GAME_WIDTH), 
        GImage(x=GAME_WIDTH/2,y=GAME_HEIGHT/2, source="jordan.png",
        height=GAME_HEIGHT,width=GAME_WIDTH)]
        self._cyclecount = 0
        self._background = self._backgroundlst[self._cyclecount]
        self._backtracklst = [Sound("Kancer.wav"), Sound("heman.wav"),
        Sound("nyan.wav"), Sound("wonderful.wav"), Sound("wonderful.wav"), 
        Sound("saxguy.wav")]
        self._tracknum = 5
        self._soundtoggle = True
        self._prev_space = False
        self._prev_p = False
        
    def update(self,dt):
        """Animates a single frame in the game.
        
        It is the method that does most of the work. It is NOT in charge of playing the
        game.  That is the purpose of the class Play.  The primary purpose of this
        game is to determine the current state, and -- if the game is active -- pass
        the input to the Play object _game to play the game.
        
        As part of the assignment, you are allowed to add your own states.  However, at
        a minimum you must support the following states: STATE_INACTIVE, STATE_NEWGAME,
        STATE_COUNTDOWN, STATE_PAUSED, and STATE_ACTIVE.  Each one of these does its own
        thing, and so should have its own helper.  We describe these below.
        
        STATE_INACTIVE: This is the state when the application first opens.  It is a 
        paused state, waiting for the player to start the game.  It displays a simple
        message on the screen.
        
        STATE_NEWGAME: This is the state creates a new game and shows it on the screen.  
        This state only lasts one animation frame before switching to STATE_COUNTDOWN.
        
        STATE_COUNTDOWN: This is a 3 second countdown that lasts until the ball is 
        served.  The player can move the paddle during the countdown, but there is no
        ball on the screen.  Paddle movement is handled by the Play object.  Hence the
        Play class should have a method called updatePaddle()
        
        STATE_ACTIVE: This is a session of normal gameplay.  The player can move the
        paddle and the ball moves on its own about the board.  Both of these
        should be handled by methods inside of class Play (NOT in this class).  Hence
        the Play class should have methods named updatePaddle() and updateBall().
        
        STATE_PAUSED: Like STATE_INACTIVE, this is a paused state. However, the game is
        still visible on the screen.
        
        The rules for determining the current state are as follows.
        
        STATE_INACTIVE: This is the state at the beginning, and is the state so long
        as the player never presses a key.  In addition, the application switches to 
        this state if the previous state was STATE_ACTIVE and the game is over 
        (e.g. all balls are lost or no more bricks are on the screen).
        
        STATE_NEWGAME: The application switches to this state if the state was 
        STATE_INACTIVE in the previous frame, and the player pressed a key.
        
        STATE_COUNTDOWN: The application switches to this state if the state was
        STATE_NEWGAME in the previous frame (so that state only lasts one frame).
        
        STATE_ACTIVE: The application switches to this state after it has spent 3
        seconds in the state STATE_COUNTDOWN.
        
        STATE_PAUSED: The application switches to this state if the state was 
        STATE_ACTIVE in the previous frame, the ball was lost, and there are still
        some tries remaining.
        
        You are allowed to add more states if you wish. Should you do so, you should 
        describe them here.
        
        Parameter dt: The time in seconds since last update
        Precondition: dt is a number (int or float)
        """
        # IMPLEMENT ME
        self._checktoggle()
        if self._state == STATE_INACTIVE:
            self._checkstartgame()
            self._temptime -= 1
        elif self._state == STATE_NEWGAME:
            self._state = STATE_COUNTDOWN
        elif self._state == STATE_COUNTDOWN:
            self._game.updatePaddle(self.input)
            self._checktimeserve()
            self._timeframe += 1
        elif self._state == STATE_ACTIVE:
            self._game.updatePaddle(self.input)
            self._game.updateBall()
            self._game.updatePowerup()
            self._checkpaused()
            self._checkpausedgame()
            self._timeframe += 1
            self._zoom()
        elif self._state == STATE_PAUSED:
            self._checkunpaused()
            self._temptime-=1
        elif self._state == STATE_PAUSED_GAME:
            self._checkunpausedgame()
            self._temptime-=1
        elif self._state == STATE_COMPLETE:
            self._restart()
            self._temptime-=1

        if self.input.is_key_down("escape"):
            self.stop()
    
    def draw(self):
        """Draws the game objects to the view.
        
        Every single thing you want to draw in this game is a GObject.  To draw a GObject 
        g, simply use the method g.draw(self.view).  It is that easy!
        
        Many of the GObjects (such as the paddle, ball, and bricks) are attributes in Play. 
        In order to draw them, you either need to add getters for these attributes or you 
        need to add a draw method to class Play.  We suggest the latter.  See the example 
        subcontroller.py from class."""
        # IMPLEMENT ME
        if self._state == STATE_INACTIVE:
            self._mssg.draw(self.view)
        elif self._state == STATE_COUNTDOWN:
            self._background.draw(self.view)
            self._game.drawBricks(self.view)
            self._game.drawPaddle(self.view)
            self._mssg.draw(self.view)
        elif self._state == STATE_ACTIVE:
            self._background.draw(self.view)
            self._game.drawBricks(self.view)
            self._game.drawPaddle(self.view)
            self._game.drawBall(self.view)
            self._game.drawPowerup(self.view)
            self._game.drawMulti(self.view)
        elif self._state == STATE_PAUSED:
            self._mssg.draw(self.view)
        elif self._state == STATE_PAUSED_GAME:
            self._background.draw(self.view)
            self._game.drawBricks(self.view)
            self._game.drawPaddle(self.view)
            self._game.drawBall(self.view)
            self._game.drawPowerup(self.view)
            self._game.drawMulti(self.view)
            self._mssg.draw(self.view)
        elif self._state == STATE_COMPLETE:
            self._background.draw(self.view)
            self._mssg.draw(self.view)
    
    # HELPER METHODS FOR THE STATES GO HERE
    def _checktoggle(self):
        """"""
        if self.input.is_key_down("spacebar") and self._prev_space == False:
            self._soundtoggle = not self._soundtoggle
        self._prev_space = self.input.is_key_down("spacebar")
        if self._soundtoggle == True:
            self._backtracklst[self._tracknum].play()
            if self._state == STATE_PAUSED_GAME:
                self._backtracklst[self._tracknum].volume = .5
            else:
                self._backtracklst[self._tracknum].volume = 1
        elif self._soundtoggle == False:
            self._backtracklst[self._tracknum].volume = 0
        
    
    def _zoom(self):
        """Zooms in and out of background and changing it after each cycle
        
        This method zooms in for 5 seconds and out for 5 seconds. While zooming 
        out it rotates the photo. It also changes the background photo after one
        zoom in and zoom out cycle while resetting photo dimensions and 
        rotation."""
        timefactor = (self._timeframe/60.)%10
        if timefactor < 5:
            self._background.width = GAME_WIDTH+(timefactor)*180
            self._background.height = GAME_HEIGHT+(timefactor)*180
        elif timefactor >= 5:
            self._background.width = GAME_WIDTH+(10-timefactor)*180
            self._background.height = GAME_HEIGHT+(10-timefactor)*180
            self._background.angle += timefactor
        if timefactor == 0:
            self._cyclecount = (self._cyclecount+1)%3
            self._background = self._backgroundlst[self._cyclecount]
            self._background.angle = 0
    
    def _GLabelmssg(self, txt):
        """creates a GLabel and assigns it to attribute _mssg
        
        Parameter txt: The text to put in Glabel
        Precondition: text is a string"""
        assert isinstance(txt, str)
        self._mssg = GLabel(text=txt)
        self._mssg.font_name = "Times.ttf"
        self._mssg.font_size = 30
        self._mssg.x = GAME_WIDTH / 2.0
        self._mssg.y = GAME_HEIGHT / 2.0
        self._mssg.fillcolor = colormodel.CYAN
        
    def _checkstartgame(self):
        """Determines the current state and assigns it to self._state
        
        This method checks for a key press and if the current state is
        STATE_INACTIVE and if both true, it changes state to STATE_NEWGAME."""
        curr_keys = self.input.key_count
        if (curr_keys > 0 and self._state == STATE_INACTIVE and 
        self._timeframe >= self._temptime + 30):
            self._state = STATE_NEWGAME
            self._game = Play()
            self._backtracklst[self._tracknum].volume = 0
            self._tracknum = 0
            self._backtracklst[self._tracknum].volume = 1
    
    def _checktimeserve(self):
        """Determines if time is greater than 3 seconds and changes state to 
        STATE_ACTIVE. It will also serve ball once state is STATE_ACTIVE.
        
        This method checks attribute _timeframe if it is greater than 3 seconds 
        and if True, changes state to STATE_ACTIVE and will serve ball."""
        if self._timeframe < 60:
            self._mssg.text = "3"
        elif 60 <= self._timeframe < 120:
            self._mssg.text = "2"
        elif 120 <= self._timeframe < 180:
            self._mssg.text = "1"
        if self._timeframe >= 180:
            self._mssg = None
            self._state = STATE_ACTIVE
            self._game.serveBall()
            self._timeframe = 0
        
    def _checkpaused(self):
        """Checks if game is paused or if game is won and changes state 
        accordingly.
        
        If the ball hits the bottom and player still has lives, the game goes to
        STATE_PAUSED. It also saves a temporary time. If the player has no more
        lives, the game goes to STATE_COMPLETE and sets message to GAME_OVER.
        If the player manages to hit all bricks, the state goes to 
        STATE_COMPLETE and sets message to win message."""
        truth = self._game.checkHitBottom()
        if truth == True:
            self._lives-=1
            if self._lives > 0:
                self._state = STATE_PAUSED
                self._GLabelmssg("Life lost!: Press any key to " + 
                "continue.\nLives: " + str(self._lives))
                self._backtracklst[self._tracknum].volume = 0
                self._tracknum += 1
                self._backtracklst[self._tracknum].volume = 1
                self._temptime = self._timeframe
            elif self._lives == 0:
                self._backtracklst[self._tracknum].volume = 0
                self._tracknum = 3
                self._backtracklst[self._tracknum].volume = 1
                self._state = STATE_COMPLETE
                self._GLabelmssg("GAME OVER")
                self._temptime = self._timeframe
        if self._game.noBricks() == True:
            self._backtracklst[self._tracknum].volume = 0
            self._tracknum = 4
            self._backtracklst[self._tracknum].volume = 1
            self._state = STATE_COMPLETE
            self._GLabelmssg("Congratulations, You Win!")
            self._temptime = self._timeframe
    
    def _checkpausedgame(self):
        """"""
        curr_keys = self.input.is_key_down("p")
        if (curr_keys and self._prev_p == False and self._timeframe >= 
        self._temptime + 15):
            self._state = STATE_PAUSED_GAME
            self._GLabelmssg("Paused: Press p to continue.\nLives: " + 
            str(self._lives))
            self._temptime = self._timeframe
            self._prev_p == True
        else:
            self._prev_p = False 
    
    def _checkunpaused(self):
        """Resets background and unpauses if player presses key after a certain
        buffer time.
        
        Resets background image dimensions and rotation. I also uses the 
        _temptime save when the game was fiirst paused as reference for how long
        to wait before it will detect keypresses. It then resets time counter,
        changes state to STATE_COUNTDOWN, and recenters the paddle."""
        self._background.angle = 0
        self._background.width = GAME_WIDTH
        self._background.height = GAME_HEIGHT
        curr_keys = self.input.key_count
        if curr_keys > 0 and self._timeframe >= self._temptime + 30:
            self._state = STATE_COUNTDOWN
            self._game.centerPaddle()
            self._timeframe = 0
            self._temptime = 0
            self._game.resetPowerup()
            self._game.resetPower()
    
    def _checkunpausedgame(self):
        """"""
        curr_keys = self.input.is_key_down('p')
        if curr_keys and self._timeframe >= self._temptime + 30:
            self._state = STATE_ACTIVE
            self._temptime = self._timeframe
            self._mssg = None
            self._prev_p = True
        else:
            self._prev_p = False
    
    def _restart(self):
        """Resets background to first image and waits for player to press key 
        after a buffer period. It then resets game.
        
        Resets background to first unmodified image. It then uses _temptime to
        wait for buffer period before accepting player keypress. It changes 
        state to STATE_INACTIVE, ends current game, changes message to start 
        message, resets time frame, resets lives, and resets _temptime."""
        self._background = self._backgroundlst[0]
        self._background.angle = 0
        self._background.width = GAME_WIDTH
        self._background.height = GAME_HEIGHT
        curr_keys = self.input.key_count
        if curr_keys > 0 and self._timeframe >= self._temptime + 30:
            self._state = STATE_INACTIVE
            self._backtracklst[self._tracknum].volume = 0
            self._backtracklst = [Sound("Kancer.wav"), Sound("heman.wav"),
            Sound("nyan.wav"), Sound("wonderful.wav"), Sound("wonderful.wav"), 
            Sound("saxguy.wav")]
            self._tracknum = 5
            self._game = None
            self._GLabelmssg("Press any key to play")
            self._timeframe = 0
            self._lives = NUMBER_TURNS
            self._temptime = self._timeframe