import numpy as np
import projection

class Track_session:
    '''
    Class that contains all the data of one tracking session
    '''
    def __init__(self, eye, pupil_params: list, resolution = 100):
        self.eye = eye
        self.gaze_amount = len(pupil_params)
        self.pupils = []
        #self.ellipses_params = np.empty((self.gaze_amount, 5))
        for gaze_id in range(0,self.gaze_amount):
            p = projection.Pupil(self.eye, pupil_params[gaze_id])
            self.pupils.append(p)



