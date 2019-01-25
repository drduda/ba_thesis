import numpy as np
import projection

class Track_session:
    '''
    Class that contains all the data of one tracking session
    '''
    def __init__(self, eye, pupil_params: list, resolution = 100):
        self.eye
        self.gaze_amount = len(pupil_params)
        self.pupils = []
        for gaze_id in range(0,self.gaze_amount):
            p = projection.Pupil(eye, pupil_params[gaze_id])
            self.pupils.append(p)

    def __iter__(self):
        self.i = 0
        return self

    def __next__(self):
        if self.i < self.gaze_amount:
            p = self.pupils[self.i]
            self.i += 1
            return p
        else:
            raise StopIteration

