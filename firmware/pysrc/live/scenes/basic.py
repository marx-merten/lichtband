from ledstrip import Band,BaseScene

class Rainbow(BaseScene):
    def __init__(self):
        super().__init__()
        self.pos=0
        self.step=3

    def getName(self):
        return "rainbow"

    def frame(self, framecounter):
        leds=self.band.leds
        count = len(leds)
        for i in range(count):
            hue=((i*self.step)+framecounter)%255
            leds.set(i,hsv_plain=(hue,200,200))
        return True

def register(band:Band):
    band.addScene(Rainbow())
