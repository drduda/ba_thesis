from session import *

####PARAMETERS################
#TODO FOCAL LENGTH
#TODO RIGHT HANDED

def gaze_maker(long_list, lat_list, radius):
    '''
    Combines every option of long and lat that is given
    :param long_list: list of spherical
    :param lat_list: list of spherical
    :param radius: single value
    :return: numpy array
    '''
    output = []
    for long in long_list:
        for lat in lat_list:
            output.append([long, lat, radius])
    return output


symmetric_30 = [[-30.0, -30.0, 0.2], [-30.0, 0.0, 0.2], [-30.0, 30.0, 0.2], [0.0, -30.0, 0.2], [0.0, 0.0, 0.2], [0.0, 30.0, 0.2], [30.0, -30.0, 0.2], [30.0, 0.0, 0.2], [30.0, 30.0, 0.2]]
#symmetric_60 = gaze_maker([-60.0,0.0,60.0],[-60.0,0.0,60.0], 0.2)


if __name__ == "__main__":
    ProjectionSession(symmetric_30, eye_center=np.array([0.0, -5.0, 0.0]), sphere_radius=1.2, resolution=100)
