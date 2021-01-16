from ledcontroller import LEDScene


class BlinkScene (LEDScene):
    def __init__(self):
        super().__init__()
        self.state = False

    def tick(self, deltaFrames: int) -> list:
        if self.state:
            self.controller.fill((200, 0, 0, 0))
        else:
            self.controller.fill((0, 0, 200, 0))
        self.state = self.state != True

    def should_execute(self, delta_frames) -> boolean:
        return True
        #  delta_frames % self.convert_to_frames(.2) == 0

    def is_finished(self, delta_frames) -> boolean:
        return delta_frames >= self.convert_to_frames(10)


class RunlightScene (LEDScene):
    def __init__(self, steps_per_second=30, finish=160, bar_size=3, color=(255, 0, 0, 0)):
        super().__init__()
        self.delay_frames = self.convert_to_frames_ms(1000/steps_per_second)
        self.finish_frame = self.convert_to_frames(finish)
        self.bar_size = 3
        self.direction = +3
        self.pos = 0
        self.color = color

    def _calc(self, pos):
        start = max(int(self.pos-(self.bar_size/2))+1, 0)
        end = min(int(self.pos+(self.bar_size/2)+0.5), self.length)
        return(start, end)

    def tick(self, deltaFrames: int) -> list:
        (old_start, old_end) = self._calc(self.pos)
        self.pos += self.direction
        (start, end) = self._calc(self.pos)
        if end >= len(self.start_values) or (start <= 0 and self.direction < 0):
            self.direction *= -1
        return
        # restore old
        for i in range(old_start, old_end):
            self.controller.write_pixel(i+self.start_pixel, self.start_values[i])

        for i in range(start, end):
            self.controller.write_pixel(i+self.start_pixel, self.color)

    def should_execute(self, delta_frames) -> boolean:
        return delta_frames % self.delay_frames == 0

    def is_finished(self, delta_frames) -> boolean:
        return delta_frames >= self.finish_frame
