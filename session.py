import numpy as np
import projection

class Track_session:
    '''
    Class that contains all the data of one tracking session
    '''

    def __init__(self, eye, pupil_param: list, resolution = 100):
        self.eye = eye
        self.gaze_amount = len(pupil_param)
        self.__gaze_number = range(0,self.gaze_amount)
        self.pupils = pupil_param
        self.pupil_circle = np.empty((self.gaze_amount, resolution, 3))
        for gaze_id in self.__gaze_number:
            p = projection.Pupil(self.eye, self.pupils[gaze_id])
            self.pupil_circle[gaze_id] = p.make_3d_circle(resolution=resolution)




