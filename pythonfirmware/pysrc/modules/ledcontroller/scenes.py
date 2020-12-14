from .ledcontroller import *


LOG = logging.getLogger("Scene")


class SceneReplay(LEDScene):
    def __init__(self, frames: list, repeat=-1):
        self.frames = frames
        self.current_frame_index = 0
        self.repeat = repeat
        self.last_frame = 0
        (self.current_frame_delay_ms, self.current_frame_data) = self.frames[self.current_frame_index % len(self.frames)]

    def _progress_frame(self):
        (self.current_frame_delay_ms, self.current_frame_data) = self.frames[self.current_frame_index % len(self.frames)]
        if self.current_frame_index % len(self.frames) == 0:
            if self.repeat > 0:
                self.repeat -= 1

    def tick(self, deltaFrames: int, currentValues) -> list:
        LOG.debug("Display Frame {}".format(self.current_frame_data))
        results = []
        for index in range(len(currentValues)):
            results.append(self.current_frame_data[index % len(self.current_frame_data)])
        self.current_frame_index += 1
        self.last_frame = deltaFrames
        self._progress_frame()
        return results

    def _next_frame_framecount(self):
        delta = self.convert_to_frames_ms(self.current_frame_delay_ms)
        return self.last_frame+delta

    def should_execute(self, delta_frames) -> boolean:
        return delta_frames >= self._next_frame_framecount()

    def is_finished(self, delta_frames) -> boolean:
        return self.repeat == 0


class SceneMorph(LEDSceneIterator):
    def __init__(self, fadeTo, steps=10, runtime_s=1, precalc=False):
        super().__init__()
        self.step_delay = runtime_s/steps
        self.steps = steps
        self.current_step = steps
        self.target_color = fadeTo

    def set_init_values(self,  init_values=None):
        self.start_values = init_values
        self.step_values = []
        if init_values:
            for v in init_values:
                stepv = tuple((x-y)/self.steps for x, y in zip(v, self.target_color))
                self.step_values.append(stepv)
        LOG.debug("Morph : initValues {}".format(init_values))
        LOG.debug("Morph : stepValues {}".format(self.step_values))
        # Need to calculate, because of floating point acuracy
        # only if precalc = True

    def should_execute(self, delta_frames) -> boolean:
        stepWidth = self.convert_to_frames(self.step_delay)
        if delta_frames % stepWidth == 0:
            return True

    def is_finished(self, delta_frames) -> boolean:
        return self.current_step <= 0

    def tick(self, deltaFrames: int, currentValues) -> list:
        self.current_step -= 1
        result = super().tick(deltaFrames, currentValues)
        # LOG.debug("Morph step values {}".format(result))
        return result

    def tickPixel(self, pixel, deltaFrames, currentValue, initValue):
        if self.current_step == 0:
            return self.target_color
        else:
            # Make sure to add special behavior if floating point accuracy is requested
            # TODO: Add precalc values
            return tuple(int(x-y) for x, y in zip(currentValue, self.step_values[pixel]))
