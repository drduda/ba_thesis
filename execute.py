import projection
import numpy as np
import eye_tracking
import matplotlib.pyplot as plt
import pupil_param_lists


class Session:
    ####PARAMETERS###
    SPHERE_RADIUS = 1.2
    RESOLUTION = 100
    RADIUS_3D_CIRCLE = 4
    FOCAL_LENGTH = 1

    def __init__(self, eye_center = np.array([0, -5.0, 0])):
        self.eye_center = eye_center
        self.projected_eye_center = [eye_center[0]/-eye_center[1], eye_center[2]/-eye_center[1]]

    def simulate_input_data(self, pupil_param_list=pupil_param_lists.symmetric_30_15):
        """
        Method that simulates an eye looking around and outputs
        the pupils in their 2D elliptic form
        All values are in degrees or centimeters
        :param pupil_param_list: [[longitude, latitude, radius],..]
        :return: elliptic input data for the actual eye tracking
        """
        eye = projection.Eye(self.eye_center, Session.SPHERE_RADIUS)
        ellipse_param_list = []

        for i in range(len(pupil_param_list)):
            p = projection.Pupil(eye, pupil_param_list[i], Session.RESOLUTION)
            ellipse_param_list.append(p.get_ellipse_param_dict())

        return ellipse_param_list


    def reprojection(self, tracked_ellipses, visualize=True):
        """
        :param input_data: list of dictionaries, each dictionary represents an ellipse and looks like
            {"x_center", "y_center": , "maj": , "min", "rot": rotated major axis clockwise in degrees}
        :return: projected eye center np.array([x, y]), distance
        """
        tracked_projected_eye_center = eye_tracking.get_projected_center(tracked_ellipses, Session.RADIUS_3D_CIRCLE, Session.FOCAL_LENGTH, visualize)


        distance = float(np.linalg.norm(tracked_projected_eye_center - self.projected_eye_center))

        if visualize:
            plt.plot(self.projected_eye_center[0], self.projected_eye_center[1], marker='o', label='Actual center')
            plt.xlabel("Measurement error: {0: .3f}cm".format(distance))
            plt.axis("equal")
            plt.show()

        return tracked_projected_eye_center, distance


if __name__ == "__main__":
    sess = Session()
    input_data = sess.simulate_input_data()
    sess.reprojection(input_data)





