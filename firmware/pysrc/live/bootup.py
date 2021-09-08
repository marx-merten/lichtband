from fileconfig import Config
from mqttapp.utils import schedule
import uasyncio as asyncio

# Default Logging
import ulogging as logging
LOG = logging.getLogger(__name__)



class Boot:
    def __init__(self,lichtband):
        super().__init__()
        self.lichtband=lichtband
        # Logical Save and Restore routine
        self.state=Config("state.json")
        self.ready=False
        schedule(self.updateState())

    async def updateState(self):
        while True:

            if self.ready:
                (r,g,b) = self.lichtband.rgb
                self.state.write("led/r",r)
                self.state.write("led/g",g)
                self.state.write("led/b",b)
                self.state.write("led/state",self.lichtband.state)
                if self.state.dirty:
                    self.state.save()
                    LOG.info("State Saved {}".format(self.state.cfgjson))
            await asyncio.sleep_ms(5000)



    def updateReady(self):
        LOG.info("RDY")
        self.ready=True
        r = self.state.get("led/r")
        g = self.state.get("led/g")
        b = self.state.get("led/b")
        st= self.state.get("led/state")
        LOG.info("STate {},({},{},{})".format(st,r,g,b))
        if st is not None:
            # Assume full stae for now
            self.lichtband.set( rgb=(r,g,b),state=st)
            self.lichtband.update()