

import cfled
import uasyncio
import time as utime

from machine import Pin

pinDebug1=Pin(25,Pin.OUT)
pinDebug2=Pin(26,Pin.OUT)
pinDebug1.value(0)
pinDebug2.value(0)

# Default Logging
import ulogging as logging
LOG = logging.getLogger(__name__)



class Band:
    def __init__(self,ledcount,pin,bpp):
        self.leds = cfled.RmtLed(pin=pin,leds=ledcount,bpp=bpp)
        self.leds.clear()
        self.leds.display()
        self.rgbw=(0,0,0,0)
        self.state=False
        self.ledSaved=None
        self.scenes={}
        self.activeScene=None
        self.sceneFrame = 0

    def isActiveScene(self):
        return self.activeScene is not  None

    def deactivateCurrentScene(self):
        if self.isActiveScene():
            self.activeScene.deactivate()
            self.activeScene=None
            self.update()


    def addScene(self,scene):
        name=scene.getName()
        self.scenes[name]=scene
        LOG.info("Added Scene ({}) to band.".format(name))

    def removeScene(self,scene):
        name=scene.getName()
        self.scenes.pop(name)
        LOG.info("Remove Scene ({}) from band.".format(name))

    def activateScene(self,name):
        if self.isActiveScene():
            self.deactivateCurrentScene()

        if name in self.scenes.keys() :
            scene = self.scenes[name]
            scene.activate(self)
            self.activeScene=scene
            self.sceneFrame=0


    def update(self):
        if (self.state):
            if not self.isActiveScene():
                self.leds.fill(rgbw=self.rgbw)
        else:
            if self.isActiveScene():
                self.deactivateCurrentScene()
                return
            self.leds.clear()
        self.leds.display()


    def set(self,rgbw=None,state=None):
        if state is not None :
            self.state=state
        if rgbw is not None :
            self.rgbw=rgbw

    def backup(self):
        self.ledSaved = self.leds.backup()

    def restore(self) :
        if self.ledSaved is not None:
            self.leds.restore(self.ledSaved)

    async def tick(self):
        fc=0
        while True:
            fc+=1
            pinDebug1.value(fc%2)

            fps=5
            ticksBefore=utime.ticks_ms()

            if self.isActiveScene():
                if self.state:
                    fps=self.activeScene.getFPS()
                    pinDebug2.value(1)
                    self.activeScene.frame(self.sceneFrame)
                    self.leds.display()
                    pinDebug2.value(0)
                    self.sceneFrame+=1
            else:
                self.update()
            ticksAfter=utime.ticks_ms()

            currentWait = utime.ticks_diff(ticksAfter,ticksBefore)
            targetWait = 1000//fps
            realWait = targetWait-currentWait
            # TODO use gpio to signal states and timing
            if realWait <0 :
                realWait=10


            await uasyncio.sleep_ms(realWait)

class BaseScene:
    def __init__(self):
        self.band = None

    def getFPS(self):
        return 20

    def getName(self):
        return "__BASE Scene"

    def activate(self,band):
        self.band = band

    def deactivate(self):
        pass

    def frame(self,framecounter):
        pass
