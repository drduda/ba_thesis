import numpy as np
import projection

class Track_session:
    '''
    Class that contains all the data of one tracking session
    '''

    def __init__(self, eye, pupil_param: list, resolution = 100):
        self.eye = eye
        gaze_amount = len(pupil_param)
        self.__gaze_number = range(0,gaze_amount)
        self.pupil_param = pupil_param
        self.__pupil_circle= np.empty((gaze_amount, resolution, 3))
        for gaze_id in self.__gaze_number:
            p = projection.Pupil(self.eye, pupil_param[gaze_id])
            self.__pupil_circle[gaze_id] = p.make_3d_circle(resolution=resolution)



