# Gordon Ruan
# ICS 2O1
# Mr. Radulovic
# Culminating Assignment: To The Top! Game
# This is a program which launches a game where the user tries to get the highest score possible by jumping on as many
# platforms as possible without falling down. This is all done within a certain time frame.
# Importing Modules.
import pygame
import random

# Function which directly loads images from exact folder. Load function was not working.
def load(filename):
    return pygame.image.load("png/" + filename)


# Function which scales every image in a list to the same size.
def scale(listname, x_size, y_size):
    for x in range(0, 10):
        listname[x] = pygame.transform.scale(listname[x], (x_size, y_size))
        x += 1


# Window sizes
screen_width = 700
screen_height = 800

# Platform
CurrentRock = "THIS IS A PLACEHOLDER" # CurrentRock changes to "i" in meteors after the first jump onto a meteor.
x_rock = [] # List which holds random position for rocks to spawn on in terms of horizontally.
rock_size = [] # List which holds random size for each rock.
y_rock = [520] # List which holds the y-position for each of the rocks. First rock spawns at 520.
counter = 0 # Number of Meteors. Values for size and position are determined individually later.
PlatformFix = 30    # Number which sizes platform.
PlatformFixY = 13   # Number which also helps size platform and make platform non-floating.

# Determines parameters for first meteor. I don't know why, but this is needed and makes the code work.
for i in range(1):
    x_rock.append(random.randint(-120,580)) # Adds a random number from -120 to 580. This is horizontal position.
    rock_size.append(random.randint(150, 177)) # Adds a random number from 150 to 177. This is size of platform/rock.


# Jump and animation
velocity = [ -30, -28, -26, -24, -22, -20, -18, -16, -14, -12, -10, -8, -6, -4, -2, 0, 2, 4, 6, 8, 10, 12, 14, 16, 18,
            20, 22, 24, 26, 28, 30] # List which changes y-postion of player when player jumps.
jumpCounter = 0 # Index for list "velocity". Increases as time increases for jump, so y-position changes.
#Indicies for lists which hold sprites. Allows for "smooth" animation.
x = 0
movementTick1 = 0
movementTick2 = 0
BreathingTick1 = 0
BreathingTick2 = 0


# Ground
GroundPlatform = 800 # Ground platform height. If player is below this point, they DIE.
FirstFall = True

# Literally just colours
black = [0, 0, 0]
white = [255, 255, 255]
Skyblue = [0, 191, 255]
red = [255,0,0]
blue = [0,0,255]
tan = [228,153,105]
goldenyellow = [250,199,58]

# Character Values and States
Player_size_width = 135 # Horizontal size of player sprites.
Player_size_height = 175# Vertical size of player sprites.
X_pos = x_rock[0]          # x-position of player (Top-left corner).
Y_pos = y_rock[0] - Player_size_height + PlatformFix + PlatformFixY  # y-position of player (Side at top of sprite).
Jumping = False         # Turns "True" when user jumps.
movementVelo = 15       # Pixels player moves when movement buttons are pressed.


# Stuff for Game States
GameOver = False        # Game over state. Turns "True" when certain events happen.
GamePlaying = False     # Game playing state. Turns "True" when start button or reset buttons are pressed.
GameStartScreen = True  # Launch screen. User can choose when to start game.
boxClicking = [0,0]     # Resets position of click.
FirstClick = True       # Resets click so game doesn't automatically reset.


# Score
GameTick = 0    # Clock Tick for just Game playing state.
Timer = 75      # Time for game playing state before game ends.
CurrentScore = 0    # Score, which increases whenever a jump is made to another platform.
HighScore = CurrentScore    # Highscore, which is saved as long as window isn't closed.
NewAdd = True   # Adds "new!" if there's new highscore.
DeadReason1 = False # Puts message on the death screen for death reason.
DeadReason2 = False # Puts another message on the death screen for death reason.


# Scrolling Stuff
scrolling = False   # Turns "True" if y-position is over certain point.
Y_posStartScroll = (screen_height - Player_size_height) / 2 # Position where screen starts "scrolling".

# Load Pictures

Background = load("Background.jpg")
Background = pygame.transform.scale(Background, (screen_width, screen_height))

Boulder = load("Boulder.png")
Boulder = pygame.transform.scale(Boulder, (rock_size[i], rock_size[i]))

StartButton = load("StartButton.png")
StartButton = pygame.transform.scale(StartButton, (200,100))

ResetButton = load("ResetButton.png")
ResetButton = pygame.transform.scale(ResetButton, (200,100))

New = load("NewHS.png")
New = pygame.transform.scale(New, (50,50))

Sun = load("Sun.png")
Sun = pygame.transform.scale(Sun, (100,100))

# List with player sprites inside of them, this is for animation.
Moving = [load('Run (1).png'), load('Run (2).png'), load('Run (3).png'), load('Run (4).png'), load('Run (5).png'),
          load('Run (6).png'), load('Run (7).png'), load('Run (8).png'), load('Run (9).png'), load('Run (10).png')]

Rest = [load("Idle (1).png"), load("Idle (2).png"), load("Idle (3).png"), load("Idle (4).png"), load("Idle (5).png"),
        load("Idle (6).png"), load("Idle (7).png"), load("Idle (8).png"), load("Idle (9).png"), load("Idle (10).png")]


window = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('To The Top! - Culminating Assignment')

pygame.init()

# Fonts
font = pygame.font.SysFont("Sans Serif", 25)
bigfont = pygame.font.SysFont("Sans Serif", 42)


# Labels
GameOverLabelReason1 = bigfont.render("You Fell!", 1, black)
GameOverLabelReason2 = bigfont.render("Time Is Up!", 1, black)
GameOverLabel = bigfont.render("Game Over!", 1, black)

TitleLabel = bigfont.render("To The Top!", 1, black)
TitleLabel = pygame.transform.scale(TitleLabel, (400, 100))

# MAIN LOOP
clock = pygame.time.Clock()
quit = False
while not quit:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit = True
        if event.type == pygame.MOUSEBUTTONDOWN:
            boxClicking = event.pos

    # Scales all images in a list to same size.
    scale(Moving, Player_size_width, Player_size_height)
    scale(Rest, Player_size_width, Player_size_height)


    # Messages for showing score and stuff.
    CurrentScoreLabel = font.render(("Score: " + str(CurrentScore)), 1, goldenyellow)
    TimerLabel = font.render(str(Timer), 1, goldenyellow)
    HighScoreLabel = font.render("Highscore: " + str(HighScore), 1, goldenyellow)

    # Start screen.
    if GameStartScreen == True:
        window.fill(white)  # Sets background white.
        window.blit(StartButton, (250,350)) # Start Button.
        window.blit (TitleLabel, (150,200)) # Puts game title on screen
        # If you push on button.
        if boxClicking[0] >= 250 and boxClicking[0] <= 450: #Checks if clicked position is within x parameters of button
            if boxClicking[1] >=350 and boxClicking[1] <= 450:  #Checks for y parameters of button.
                GamePlaying = True              # Sets game playing state to true.
                GameStartScreen = False         # Closes starting screen.
                FirstClick = False              # Allows for reset of clicking position.
            if FirstClick == False:             # Resets clicking position.
                boxClicking = [0,0]

    if GamePlaying == True:                     # Game Playing Loop.
        window.blit(Background, (0,0))          # Putting background over
        keys = pygame.key.get_pressed()         # Checks state of keyboard for any key pressed
        # Keys
        if keys[pygame.K_a]:                    # If key pressed is "a"
            X_pos -= movementVelo               # Player moves left (specified pixels).
            movementTick1 += 1                  # Increases index in list with running sprites.
            if movementTick1 >= len(Moving) - 1:  # If index is greater than length of list
                movementTick1 = 0   # Reset index.
            window.blit(pygame.transform.flip(Moving[movementTick1], True, False), (X_pos, Y_pos))  # Puts image in.
        elif keys[pygame.K_d]:      # Similar to if key pressed is "a"
            X_pos += movementVelo   # Player moves to the right.
            movementTick2 += 1
            if movementTick2 >= len(Moving) - 1:
                movementTick2 = 0
            window.blit(Moving[movementTick2], (X_pos, Y_pos))
        else:
            BreathingTick1 += 0.25      # Increases by 0.25 for each in-game tick, works to slow down animation
            if BreathingTick1 % 1 == 0:     # If Breathing tick 1 is a whole number
                BreathingTick2 = BreathingTick2 + 1 # List index for breathing increases.
            if BreathingTick2 >= len(Rest) - 1:     # If index is greater than length of list
                BreathingTick2 = 0      # Resets index.
            window.blit(Rest[BreathingTick2], (X_pos, Y_pos))


        if keys[pygame.K_SPACE] or keys[pygame.K_w]:    # If key pressed is either W or Space
            Jumping = True                              # Goes to if Jumping is "True"


        if Jumping == True:                             # If Jumping is "True"
            Y_pos += velocity[jumpCounter]              # Increases Y_pos of character by list item in index.
            jumpCounter += 1                            # Increases index number
            if jumpCounter >= len(velocity) - 1:        # If index greater than list length
                jumpCounter = len(velocity) - 1         # Sets pixels Y_pos changes to last item in list
            if Y_pos + Player_size_height <= GroundPlatform and Y_pos + Player_size_height + velocity[
                jumpCounter] >= GroundPlatform:     # If player is currently above Ground and under in the next tick
                Y_pos = GroundPlatform - Player_size_height #Sets player on the ground platform.
                Jumping = False     # Player Y_pos no longer changes
                jumpCounter = 0     # Resets index for velocity list

    # PlatForms
        if counter <= 200:          # If number of rocks is less than 200
            y_rock.append(y_rock[counter] - 225)    # Add y_position of rock into list. Same distance apart.
            x_rock.append(random.randint(-120, 580))    # Adds random x_position for rock.
            rock_size.append(random.randint(150, 177))  # Adds random size for rock
            counter += 1    # Increases of number of rocks finished.

        for i in range(counter):    # For each rock of the 200.
            window.blit(Boulder, (x_rock[i], y_rock[i]))    # Draws the rock
            if Y_pos < Y_posStartScroll:    # if player is above middle of screen.
                scrolling = True
            if Y_pos > Y_posStartScroll:    # if player is below middle of screen.
                scrolling = False
            if scrolling == True:           # if scrolling is "True"
                y_rock[i] += 10             # Move y_position of all rocks down 10 pixels
            if Y_pos + Player_size_height - PlatformFixY < y_rock[i] + PlatformFix and Y_pos + Player_size_height\
                + velocity[jumpCounter]-  PlatformFixY >= y_rock[i] + PlatformFix:
                # If player is currently above platform and in the next tick will be below the platform.
                if X_pos + Player_size_width >= x_rock[i] + PlatformFix and X_pos <= x_rock[i] + rock_size[i] - \
                    PlatformFix:
                    # Checks if player is on appropriate x_position to land on platform
                    Y_pos = y_rock[i] - Player_size_height + PlatformFix + PlatformFixY # Sets player on top of platform
                    Jumping = False # Player Y_pos no longer changes.
                    jumpCounter = 0 # Resets index for velocity list
                    CurrentRock = i # Sets rock that player is currently on top of as "i".
                    CurrentScore += 1   # Increases player's score.
            if CurrentRock != "THIS IS A PLACEHOLDER":  # If player jumped on a rock
                if X_pos + Player_size_width <= x_rock[CurrentRock] + (2 * PlatformFix) or X_pos >= x_rock[CurrentRock]\
                        + rock_size[CurrentRock] - PlatformFix:
                    # If X_pos of player is determined not close enough to platform
                    if Jumping == False: # and if Jumping == False
                        Y_pos += .6     # Player falls off platform
        # Borders
        if X_pos + 50 >= screen_width: # If player X_position 50 pixels to right of edge of border
            X_pos = -150    # Player X_position teleports to left border.
        if X_pos <= -160:   # If player X_position is 160 pixels left of the left border
            X_pos = screen_width - 50   # Player X_position teleports to right border.

        # Ending Game
        if Y_pos + Player_size_height + PlatformFix >= GroundPlatform : # If feet of player are under the Ground
            DeadReason1 = True          # Player death screen draws reason 1.
            DeadReason2 = False
            GameOver = True             # Goes to death screen.

        GameTick += 1                   # Ticks in-game
        if GameTick % 60 == 0:          # If 60 ticks (60 ticks per second) have passed since this previously activated.
            Timer -= 1                  # Lowers timer by 1

        # Values user may want to see
        window.blit(CurrentScoreLabel, (0, 0))      # Draws label showing player's score
        window.blit(TimerLabel, (680 , 0))          # Draws label showing time left


        if Timer == 0:      # If Timer reaches 0
            GamePlaying = False # Game is over
            GameOver = True
            DeadReason1 = False     # Player death screen draws reason 2.
            DeadReason2 = True

    # NOTE: POSITIONS FOR LABELS AREN'T CALCULATED MATHIMATICALLY, JUST WENT BY EYE
    if GameOver == True:    # Game Over Loop
        if CurrentScore >= HighScore:   # If current score is greater than high score
            HighScore = CurrentScore    # High score will now equal current score.
            NewAdd = True   # Allows for drawing of New!
        window.fill(tan)    # Fills background
        window.blit(GameOverLabel, (266, 200))  # Draws Game Over!
        window.blit(CurrentScoreLabel, (315,280))   # Draws user's score in run which just finished
        window.blit(HighScoreLabel, (296, 310)) # Draws high score
        if NewAdd == True:      # If Current score is higher than high score
            window.blit(New, (244, 285))    # Draws New!
            NewAdd = False                  # Stops drawing of New!
        if DeadReason1 == True:             # If player died by falling
            window.blit(GameOverLabelReason1, (284, 240))   # Draws "You Fell!"
        if DeadReason2 == True:                             # If player falls by time running out
            window.blit(GameOverLabelReason2, (264, 240))   # Draws "Time Is Up!"
        window.blit(ResetButton, (250,350))                 # Draws Reset button
        if boxClicking[0] >= 250 and boxClicking[0] <= 450:     # Checks if clicked position is horizontally in button.
            if boxClicking[1] >= 350 and boxClicking[1] <= 450: # Checks if clicked position is vertically in button.
                GamePlaying = True  # Starts Game
                GameOver = False    # Takes out Game Over Screen
                FirstClick = False  # Resets click position
                CurrentScore = 0    # Resets score.
                Timer = 75          # Resets timer.
                GameTick = 0        # Resets ticks in previous game.
                CurrentRock = 0     # Sets Current Rock to first rock.
                counter = 0         # Sets amount of rocks to 0.
                y_rock = [520]      # Resets list of Y_positions for rocks.
                x_rock.clear()      # Clears list with previous horizontal positions for rocks.
                rock_size.clear()   # Clears list with previous sizes for rocks.
                for n in range(1):  # Adds starting rock parameters
                    x_rock.append(random.randint(-120, 580))
                    rock_size.append(random.randint(150, 177))
                X_pos = x_rock[0]   # Sets Player X_position on the x position of the rock
                Y_pos = y_rock[0] - Player_size_height + PlatformFix + PlatformFixY # Sets Player Y_position above rock
                DeadReason1 = False # Resets variable for deciding whichever to draw on death.
                DeadReason2 = False
                if FirstClick == False: # Resets clicking position
                    boxClicking = [0, 0]

    pygame.display.update() # Update Display
    clock.tick(60)  # Tick Rate
pygame.quit()   # Closes Module