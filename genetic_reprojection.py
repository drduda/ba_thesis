import numpy as np
from math import sqrt
import projection


class shadow_mapped_eye(projection.Eye):
    def __init__(self):
        '''
            The eye on which the ellipses are shadow mapped on.
        '''
        #TODO Set random center later or take some heuristic
        projection.Eye.__init__(self)


class shadow_mapped_pupil():
    def __init__(self,shadow_mapped_eye, ellipse):
        '''
        Take ellipse as input for shadowmapping.
        '''
        #TODO: np.nditer(a, flags=['external_loop'], order='F'): for performance
        #Achtung traversiert!
        points = ellipse.points_on_ellipse_T
        res = points.shape[0]
        line_length_array = np.empty(res)

        a = shadow_mapped_eye.center[0]
        b = shadow_mapped_eye.center[1]
        c = shadow_mapped_eye.center[2]
        r = shadow_mapped_eye.sphere_radius

        for i in range(res):
            point = points[i]
            x = point[0]
            # Is display size
            y = shadow_mapped_eye.display_distance
            z = point[1]
            #TODO CHECK IF REALLY ELLIPSE points
            u = (-sqrt((-2*a*x - 2*b*y - 2*c*z)**2 - 4*(x**2 + y**2 + z**2)*(a**2 + b**2 + c**2 - r**2)) + 2*a*x + 2*b*y + 2*c*z)/(2*(x**2 + y**2 + z**2))
            line_length_array[i] = u






#For Execution
s_e = shadow_mapped_eye()
p = projection.Pupil(s_e, [0,0,0.2])
s_p = shadow_mapped_pupil(s_e, p.ellipse)
