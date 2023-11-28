'''
    Developer:
    THREELabs / Kevin Webber
    
    Project Details:
    Skateboarding game derived from the SauRun game created by Mason W.
'''

'''
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
'''



# Configuration/Boilerplate
import ssd1306
import machine
import time
import uos
import random
import gc
import utime
import thumby
import os


# Overclock
machine.freq(220000000)

# This line helps make sure we don't run out of memory
gc.enable() 

from framebuf import FrameBuffer, MONO_VLSB # Graphics stuff

# Sensitive game parameters
XVel = 0.05
YVel = 0
Distance = 0
YPos = 0
Gravity = 0.08
MaxFPS = 60
Points = 0
GameRunning = True
CactusPos = random.randint(72, 300)
CloudPos = random.randint(60, 200)
BirdPos = random.randint(60, 200)
SunPos = random.randint(60, 200)
JumpSoundTimer = 0


'''
# BITMAP: width: 72, height: 30
bg = bytearray([0,0,0,0,0,0,0,0,0,0,0,4,0,0,0,0,0,0,0,0,128,0,0,0,0,0,0,0,0,0,0,0,0,0,64,0,0,0,0,0,0,0,0,0,0,0,0,128,0,0,0,0,0,0,0,0,0,0,0,4,0,0,0,0,0,0,0,0,0,64,0,0,
            0,0,0,0,0,8,20,8,0,0,0,128,128,128,128,128,128,128,128,128,128,128,128,128,0,0,0,0,64,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,2,1,0,0,0,0,128,192,224,224,240,240,248,248,252,252,252,252,252,252,252,252,248,248,240,
            224,240,240,248,248,252,252,254,254,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,254,252,248,248,240,224,224,224,192,192,192,192,192,192,192,192,192,192,192,224,224,224,240,248,252,252,254,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,
            63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63])

bg2 = bytearray([0,0,0,2,0,0,0,16,64,0,0,0,0,128,64,128,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,16,0,0,0,0,0,0,0,0,0,0,16,40,16,0,0,0,0,0,0,0,0,0,0,0,0,0,32,0,0,0,0,0,0,0,0,64,160,64,2,0,
            240,224,192,128,128,128,0,8,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,8,0,128,128,128,192,224,240,240,248,248,248,252,252,252,254,254,254,255,255,255,255,255,254,254,254,254,252,252,252,248,248,240,240,225,224,192,192,128,128,0,0,0,0,0,32,0,0,0,
            255,255,255,255,255,255,255,255,254,254,254,254,252,252,252,252,252,252,252,254,254,254,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,254,252,252,248,240,240,224,224,
            63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63])
'''



# BITMAP: width: 72, height: 30
bg = bytearray([255,255,15,167,179,185,179,167,15,255,255,255,199,187,61,189,61,187,199,255,127,127,63,95,63,127,127,255,255,255,241,245,1,241,21,81,17,241,245,81,81,85,81,81,85,81,81,85,81,81,245,17,81,21,241,1,245,241,255,255,255,255,255,175,7,171,253,171,7,175,255,255,
           215,199,208,199,208,198,208,199,208,199,215,199,215,199,208,199,208,199,215,199,208,195,215,199,215,195,208,199,215,199,215,199,208,199,215,199,215,199,215,198,214,192,214,198,208,214,198,208,198,214,199,215,199,215,199,208,199,215,199,215,199,215,199,214,198,208,198,208,198,214,199,215,
           255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,
           63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63])



# BITMAP: width: 72, height: 30
bg2 = bytearray([255,255,255,127,63,127,255,255,15,135,11,201,205,205,205,205,205,11,135,15,255,255,127,63,127,255,255,255,127,127,127,127,127,127,255,255,255,255,255,127,191,95,31,75,161,75,31,95,191,127,255,255,255,255,255,131,53,181,181,181,181,53,53,53,181,181,181,181,53,131,255,255,
            215,199,215,199,208,199,215,199,208,199,208,199,208,198,214,192,215,192,215,192,215,199,215,192,215,199,215,192,210,199,215,199,215,194,208,199,215,199,208,198,214,192,214,198,208,214,198,208,198,214,192,215,199,215,199,215,192,215,196,212,199,212,196,212,199,212,196,215,192,215,199,215,
            255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,
            63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63])














# Background sprites & initial x positions
bgSpr = thumby.Sprite(72, 30, bg)
bg2Spr = thumby.Sprite(72, 30, bg2)
bgSpr.x = 0
bg2Spr.x = 72





scrollCtr = 0


#Sprite Details
# BITMAP: width: 10, height: 16
PlayerRunFrame1 = bytearray([255,191,191,161,8,97,251,251,255,255,
           223,191,15,183,184,183,174,29,191,223])


           
# BITMAP: width: 8, height: 16
# BITMAP: width: 10, height: 16
PlayerRunFrame3 = bytearray([255,255,255,225,8,97,251,251,255,255,
           223,187,57,190,160,23,174,29,191,223])   

# BITMAP: width: 8, height: 8
Obj1 = bytearray([255,3,235,235,235,235,3,255])


# BITMAP: width: 8, height: 8
CactusSpr2 = bytearray([255,227,8,234,234,8,227,255])

# BITMAP: width: 16, height: 16
CloudSpr = bytearray([127,31,207,239,199,243,251,251,243,199,31,223,223,159,63,255,
            248,251,243,247,247,247,247,247,247,247,247,247,247,243,250,248])
            
# BITMAP: width: 16, height: 16

SunSpr = bytearray([255,31,239,247,251,253,253,253,253,253,253,251,247,239,31,255,
           255,248,247,239,223,191,191,191,191,191,191,223,239,247,248,255])

# BITMAP: width: 16, height: 16
BirdSpr = bytearray([255,255,239,247,251,251,251,247,239,247,251,251,251,247,255,255,
           255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255])



# BITMAP: width: 32, height: 32
SplashSpr = bytearray([0,0,0,0,0,0,0,0,128,128,192,224,252,254,254,252,240,240,240,224,224,192,192,128,128,0,0,0,0,0,0,0,
           0,0,12,12,2,3,3,1,1,29,125,253,255,63,127,127,127,127,127,63,62,248,192,129,1,1,2,6,4,0,0,0,
           0,0,0,0,0,0,0,0,0,0,8,13,15,14,12,0,0,0,0,0,0,1,7,3,0,0,0,0,0,0,0,0,
           0,0,0,0,0,0,0,0,16,24,12,4,7,7,4,4,4,4,4,4,4,7,7,4,12,24,16,0,0,0,0,0])

# Create Sprite objects using bitmaps
SplashObj = thumby.Sprite(32, 32, SplashSpr,40,1)

ObjSpr = Obj1

thumby.display.fill(0)




# Draw sprites and update display
thumby.display.drawSprite(SplashObj)
thumby.display.drawText("Skate", 1, 1, 1)
thumby.display.drawText("Or Die", 1, 14, 1)
thumby.display.update()





thumby.display.setFPS(60)

thumby.saveData.setName("Sk8OrDie")

while(thumby.buttonA.pressed() == True or thumby.buttonB.pressed() == True):
    if(time.ticks_ms() % 1000 < 500):
        thumby.display.drawFilledRectangle(0, 32, 72, 8, 0)
        thumby.display.drawText("Start!", 9, 32, 1)
    else:
        thumby.display.drawFilledRectangle(0, 32, 50, 8, 1) 
        thumby.display.drawText("Start!", 9, 32, 0)
    thumby.display.update()
    pass
while(thumby.buttonA.pressed() == False and thumby.buttonB.pressed() == False):
    if(time.ticks_ms() % 1000 < 500):
        thumby.display.drawFilledRectangle(0, 32, 72, 8, 0)
        thumby.display.drawText("Start!", 9, 32, 1)
    else:
        thumby.display.drawFilledRectangle(7, 32, 38, 8, 1)
        thumby.display.drawText("Start!", 9, 32, 0)
    thumby.display.update()
    pass
while(thumby.buttonA.pressed() == True or thumby.buttonB.pressed() == True):
    if(time.ticks_ms() % 1000 < 500):
        thumby.display.drawFilledRectangle(0, 32, 72, 8, 0)
        thumby.display.drawText("Start!", 9, 32, 1)
    else:
        thumby.display.drawFilledRectangle(0, 32, 72, 8, 1)
        thumby.display.drawText("Start!", 9, 32, 0)
    thumby.display.update()
    pass

while(GameRunning):
    
        # Scrolling background
    scrollCtr += 1
    if(scrollCtr % 8 == 0): # Move the background every 8 loops
        bgSpr.x -= 1
        bg2Spr.x -= 1


    # Re-place the x coordinate of backgrounds when they're unseen
    if (bg2Spr.x == 0):
        bgSpr.x = 72
    if (bg2Spr.x == -72):
        bg2Spr.x = 72
        
        
    t0 = utime.ticks_us() # Check the time


    # Is the player on the ground and trying to jump?
    if(JumpSoundTimer < 0):
        JumpSoundTimer = 0
    if((thumby.buttonA.pressed() == True or thumby.buttonB.pressed() == True) and YPos == 0.0):
        # Jump!
        JumpSoundTimer = 200
        YVel = -1.5 # How High you will jump

    # Handle "dynamics"
    YPos += YVel
    YVel += Gravity
    Distance += XVel
    JumpSoundTimer -= 15
    
    if(JumpSoundTimer > 0):
        thumby.audio.set(500-JumpSoundTimer)
    else:
        thumby.audio.stop()

    # Accelerate the player just a little bit
    XVel += 0.0000150

    # Make sure we haven't fallen below the ground
    if(YPos > 0):
        YPos = 0.0
        YVel = 0.0

    # Has the player hit a cactus?
    if(CactusPos < 8 and CactusPos > -8 and YPos > -8):
        # Stop the game and give a prompt
        GameRunning = False
        thumby.display.fill(1)
        thumby.audio.stop()
        #thumby.display.drawText("Oh no!", 18, 1, 0)
        thumby.display.drawText(str(int(Distance))+"m", 26, 9, 0)
        high = -1
        if(thumby.saveData.hasItem("highscore")):
            high = int(thumby.saveData.getItem("highscore"))
            thumby.display.drawText("High: " + str(high)+"m", 8, 17, 0)
        if(Distance > high):
            thumby.saveData.setItem("highscore", Distance)
            thumby.saveData.save()
        thumby.display.drawText("Again?", 19, 25, 0)
        thumby.display.drawText("A:N B:Y", 16, 33, 0) 
        thumby.display.update()
        thumby.audio.playBlocking(300, 250)
        thumby.audio.play(260, 250)

        while(thumby.inputPressed() == False):
            pass # Wait for the user to give us something

        while(GameRunning == False):
            if(thumby.buttonB.pressed() == True == 1):
                # Restart the game
                XVel = 0.05
                YVel = 0
                Distance = 0
                YPos = 0
                Points = 0
                GameRunning = True
                CactusPos = random.randint(72, 300)
                CloudPos = random.randint(60, 200)
                BirdPos = random.randint(60, 200)
                SunPos = random.randint(60, 200)

            elif(thumby.buttonA.pressed() == True):
                # Quit
                machine.reset()

    # Is the cactus out of view?
    if(CactusPos < -24):
        # "spawn" another one (Set its position some distance ahead and change the sprite)
        Points += 10
        thumby.audio.play(440, 300)
        CactusPos = random.randint(72, 500)
        if(random.randint(0, 1) == 0):
            ObjSpr = Obj1
        else:
            ObjSpr = CactusSpr2
            
    # Is the Sun out of view?
    if(SunPos < -10):
        # "spawn" another one
        SunPos = random.randint(40, 200)


    # Is the cloud out of view?
    if(CloudPos < -32):
        # "spawn" another one
        CloudPos = random.randint(40, 200)
        
    # Is the bird out of view?
    if(BirdPos < -32):
        # "spawn" another one
        BirdPos = random.randint(40, 200)

    # More dynamics
    CactusPos -= XVel * 16
    CloudPos -= XVel * 1
    BirdPos -= XVel * 2
    SunPos -= XVel * 1

    # Draw game state 
    thumby.display.fill(1)
    thumby.display.drawSprite(bgSpr)
    thumby.display.drawSprite(bg2Spr)
    thumby.display.blit(ObjSpr, int(16 + CactusPos), 23, 8, 8, 1, 0, 0) # Example: thumby.display.blit(bitmapData, x, y, width, height, key, mirrorX, mirrorY)
    thumby.display.blit(CloudSpr, int(32 + CloudPos), 12, 16, 16, 1, 0, 0)
    thumby.display.blit(BirdSpr, int(10 + BirdPos), 8, 16, 16, 1, 0, 0)
    thumby.display.blit(CloudSpr, int(2 + CloudPos), 2, 16, 16, 1, 0, 0)
    thumby.display.blit(BirdSpr, int(32 + BirdPos), 2, 16, 16, 1, 0, 0)
    thumby.display.blit(SunSpr, int(32 + SunPos), 2, 16, 16, 1, 0, 0)
    
    if(t0 % 250000 < 125000 or YPos != 0.0):
        # Player is in first frame of run animation
        thumby.display.blit(PlayerRunFrame1, 8, int(15 + YPos), 10, 16, 1, 0, 0)
        
    else:
        # Player is in second frame of run animation
        thumby.display.blit(PlayerRunFrame3, 8, int(15 + YPos), 10, 16, 1, 0, 0)
        


    thumby.display.drawFilledRectangle(0, 31, thumby.display.width, 9, 0) # Ground
    #Hide POints thumby.display.drawText(str(int(Points)), 0, 0, 0) # Current points
    #Disable Points thumby.display.drawText("pts", len(str(int(Points))) * 8, 0, 0)
    thumby.display.drawText(str(int(Distance)), 0, 32, 1) # Current distance
    thumby.display.drawText("m", len(str(int(Distance))) * 8, 32, 1)
    thumby.display.update()

    # Spin wheels until we've used up one frame's worth of time
    while(utime.ticks_us() - t0 < 1000000.0 / MaxFPS):
        pass
