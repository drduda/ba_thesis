import numpy as np
import projection

class Track_session:
    '''
    Class that contains all the data of one tracking session
    '''
    def __init__(self, eye, pupil_params: list, resolution = 100):
        self.eye = eye
        self.gaze_amount = len(pupil_param)
        self.__gaze_number = range(0,self.gaze_amount)
        self.pupils = []
        for pupil_param in pupil_params:
            p = projection.Pupil(self.eye, self.pupil_param[gaze_id])
            self.pupils.append(p)



import

