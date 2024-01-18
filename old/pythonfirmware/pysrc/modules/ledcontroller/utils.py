

def morph_linear(steps: int, fromValue: tuple, toValue: tuple):
    stepv = tuple((y-x)/steps for x, y in zip(fromValue, toValue))
    result = []
    for i in range(steps):
        result.append(tuple(int(x+(y*i)) for x, y in zip(fromValue, stepv)))
    return result


def morph_frames_linear(steps: int, fromFrame: list, toFrame: list):
    stepv = []
    size = min(len(fromFrame), len(toFrame))
    for i in range(size):
        fromValue = fromFrame[i]
        toValue = toFrame[i]
        stepv.append(tuple((y-x)/steps for x, y in zip(fromValue, toValue)))

    result = []
    for j in range(steps):
        current = []
        for i in range(size):
            fromValue = fromFrame[i]
            toValue = toFrame[i]
            current.append(tuple(int(x+(y*j)) for x, y in zip(fromValue, stepv[i])))
        result.append(current)
    return result


def morph_scene_linear(scene: list):
    """ Scene Format to transmit
        [
            (deltaTimeFromPrevious,steps_from_previous,[(r,g,b)....]),
            ...
        ]
        example
        [
            (1000,1,[(0,0,0)]), #set first frame
            (500,2,[(20,20,20)]), #transit to (20,20,20) in 500 ms and 2 steps. it'll repeat the first frame
            (1000,1,[(20,20,20)]), simple loop transition (stay and keep (20,20,20) for 1 second)
            (500,2,[(0,0,0)]), #transit to (0,0,0) in 500 ms and 2 steps. it'll repeat the first frame
        ]
        Result:
        [ (100,[(0,0,0)]), #F1
          (250,[(0,0,0)]), #F2
          (250,[(10,10,10)]),#F2
          (1000,[(20,20,20)]),#F3
          (250,[(20,20,20)]),#F4
          (250,[(10,10,10)])#F4
        ]

    """
    last = None
    result = []
    for frame in scene:
        (delay, steps, target) = frame
        if last == None:
            last = target
        for morphed_frame in morph_frames_linear(steps, last, target):
            val = (delay//steps, morphed_frame)
            result.append(val)
        last = target
    return result
