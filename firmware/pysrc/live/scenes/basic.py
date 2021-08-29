from ledstrip import Band,BaseScene

class Rainbow(BaseScene):
    def __init__(self):
        super().__init__()
        self.pos=0
        self.step=10
        self.lauflicht_step=2

    def getName(self):
        return "rainbow"


    def frame(self, framecounter):
        leds=self.band.leds
        if framecounter == 0 :
            count = len(leds)
            for i in range(count):
                hue=(i*self.step)%255
                leds.set(i,hsv_plain=(hue,200,255))
        else:
            leds >>=self.lauflicht_step
        return True

class RainbowReverse(BaseScene):
    def __init__(self):
        super().__init__()
        self.pos=0
        self.step=10
        self.lauflicht_step=-2

    def getName(self):
        return "rainbow-reverse"


    def frame(self, framecounter):
        leds=self.band.leds
        if framecounter == 0 :
            count = len(leds)
            for i in range(count):
                hue=(i*self.step)%255
                leds.set(i,hsv_plain=(hue,200,255))
        else:
            leds >>=self.lauflicht_step
        return True
def register(band:Band):
    band.addScene(Rainbow())
    band.addScene(RainbowReverse())
