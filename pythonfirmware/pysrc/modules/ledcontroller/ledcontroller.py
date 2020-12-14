import ulogging as logging
from machine import Pin
from neopixel import NeoPixel
import uasyncio
import sys

AREA_ALL = ':'


LOG = logging.getLogger("LED")


def calc_pos_difference_with_wrap(start: int, end: int):
    if end >= start:
        return end-start
    else:
        delta = sys.maxsize-start
        delta += end
        return delta


class LEDScene:
    def __init__(self):
        self.start_values = []
        self.fps = 20
        pass

    def set_init_values(self,  init_values=None):
        self.start_values = init_values

    def set_fps(self, fps):
        self.fps = fps

    def tick(self, deltaFrames: int, currentValues) -> list:
        pass

    def should_execute(self, delta_frames) -> boolean:
        return True

    def is_finished(self, delta_frames) -> boolean:
        return False

    # Utillity - - Functions
    def convert_to_frames(self, seconds):
        frames = int(seconds*self.fps)
        if frames <= 0:
            frames = 1
            LOG.warning("Limit reached, reset to 1 frame")
        return frames

    def convert_to_frames_ms(self, ms):
        return int((ms/1000)*self.fps)


class LEDSceneIterator(LEDScene):
    def __init__(self):
        super().__init__()

    def tickPixel(self, pixel, deltaFrames, currentValue, initValue):
        pass

    def tick(self, deltaFrames: int, currentValues) -> list:
        if not self.should_execute(deltaFrames):
            return None
        result = []
        for (i, v) in enumerate(currentValues):
            result.append(self.tickPixel(i, deltaFrames, v, self.start_values[i]))
        return result


class LEDSceneItem:
    def __init__(self, region: string, start: int, end: int, init_frames: int, scene: LEDScene, restore_after_exec=False, cur_values=False):
        self.start = start
        self.end = end
        self.region = region
        self.init_frames = init_frames
        self.scene = scene
        self.restore = restore_after_exec
        self.values = cur_values


class LEDController:
    def __init__(self, led, fps=20, bpp=3, pixel=0):
        pled = Pin(led, Pin.OUT)
        self.pixelcount = pixel
        self.pixel = NeoPixel(pled, pixel, bpp=bpp)   # create NeoPixel driver on GPIO0 for 8 pixels
        # self.pixel.fill((0, 0, 0, 0))
        # self.pixel.write()
        self.fps = fps
        self.current_frame = 0
        uasyncio.get_event_loop().create_task(self.tick())
        self.scenes = []

    def _get_region(self, region):
        # TODO: parse string
        start = 0
        end = 0

        if ':' in region:
            r = region.split(':')
            if r[0] == '':
                start = 0
            else:
                start = int(r[0])
                if start < 0:
                    start = self.pixelcount+start
            if r[1] == '':
                end = self.pixelcount-1
            else:
                end = int(r[1])
                if end < 0:
                    end = self.pixelcount+end
        return (start, end)

    def _clean_color(self, color):
        (r, g, b) = color
        if r < 0:
            r = 0
        if g < 0:
            g = 0
        if b < 0:
            b = 0
        return (r, g, b)

    def _write(self, led_start, led_end, values):
        ledNum = led_start
        for value in values:
            self.pixel[ledNum] = self._clean_color(value)
            ledNum += 1
            if ledNum > led_end:
                break

    def _get(self, start, end):
        result = []
        for ledNum in range(start, end+1):
            result.append(self.pixel[ledNum])
        return result

    def _fill(self, led_start, led_end, value):
        for ledNum in range(led_start, led_end+1):
            self.pixel[ledNum] = self._clean_color(value)

    def _remove_scene(self, scene_id):
        scene: LEDSceneItem = self.scenes.pop(scene_id)
        if scene.restore:
            self._write(scene.start, scene.end, scene.values)
            return True
        else:
            return False

    def _tick_scenes(self):
        # TODO only execute first Scene for Area
        remove_ids = []
        dirty = False
        for (index, item) in enumerate((self.scenes)):
            scene: LEDScene = item.scene
            deltaFrames = calc_pos_difference_with_wrap(item.init_frames, self.current_frame)
            if scene.should_execute(deltaFrames):
                results = scene.tick(deltaFrames, self._get(item.start, item.end))
                self._write(item.start, item.end, results)
                dirty = True
            if scene.is_finished(deltaFrames):
                remove_ids.append(index)
        for i in reversed(remove_ids):
            if self._remove_scene(i):
                dirty = True
        if dirty:
            self.pixel.write()

    def fill(self, value, led=AREA_ALL):
        (start, stop) = self._get_region(led)
        self._fill(start, stop, value)
        self.pixel.write()

    def write(self, values, led=AREA_ALL):
        (start, stop) = self._get_region(led)
        if isinstance(values, list):
            self._write(start, stop, values)
        elif isinstance(values, tuple):
            self._fill(start, stop, values)
        self.pixel.write()

    def add_scene(self, scene: LEDScene, restore_after_execution=True, region=AREA_ALL):
        # TODO Only allow areas
        (start, stop) = self._get_region(region)
        initValues = self._get(start, stop)
        item = LEDSceneItem(region, start, stop, self.current_frame, scene, restore_after_execution, initValues)
        item.scene.set_fps(self.fps)
        item.scene.set_init_values(initValues)
        self.scenes.insert(0, item)
        LOG.debug("Added Scene {} to region [{}] ({},{})".format(scene, region, start, stop))
        return item

    async def tick(self):
        while True:
            self.current_frame += 1
            self._tick_scenes()
            await uasyncio.sleep_ms(1000//self.fps)