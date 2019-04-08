import numpy as np


class Quadric:
    """
    Base class for ellipse and cones, because they are both quadrics mathmatically.
    """
    def get_equation(self):
        '''
        Returns implicit equation of the quadric which can be copy pasted to Wolfram Alpha
        :return: String of implicit equation
        '''
        output = ''
        for key, value in self.__dict__.items():
            try:
                output += str(value) + '*' + key[2:] + ' + '
            except:
                output += key
        return output[:-4] + ' = 0'


class ImpEllipse(Quadric):
    """
    Class for an ellipse with coefficients from its implicit function as its attributes
    """

    def __init__(self, a_xx, h_xy, b_yy, g_x, f_y, d):
        self.a_xx = a_xx
        self.h_xy = h_xy
        self.b_yy = b_yy
        self.g_x = g_x
        self.f_y = f_y
        self.d = d

    @staticmethod
    def construct_by_param(center_x, center_y, rotation):
        pass


class Cone(Quadric):
    '''
    Represents a cone which is described by the coefficients which its implicit equation has.
    Attribute self.a_xx is coefficient a for term x². Its most general form is:
    a*x**2 + b*y**2 + c*z**2 + 2*f*y*z + 2*g*z*x + 2*h*x*y + 2*u*x + 2*v*y + 2*w*z + d = 0
    Here the simplest form is represented
    All variable names are copied from Safaee-Rad's paper
    '''
    def __init__(self, a_xx, b_yy, c_zz):
        self.a_xx = a_xx
        self.b_yy = b_yy
        self.c_zz = c_zz


class ConeCamera(Cone):
    def __init__(self, a_xx, b_yy, c_zz, f_yz, g_zx, h_xy):
        Cone.__init__(self, a_xx, b_yy, c_zz)
        self.f_yz = f_yz
        self.g_zx = g_zx
        self.h_xy = h_xy

    @staticmethod
    def ellipse_2_cone(a_xx, h_xy, b_yy, g_x, f_y, d, gamma=1):
        """
        Constructs a cone by its ellipse intersection.
        :param a_xx:
        :param h_xy:
        :param b_yy:
        :param g_x:
        :param f_y:
        :param d:
        :param gamma:
        :return:
        """
        a = gamma**2 * a_xx
        b = gamma**2 * b_yy
        c = d
        d = gamma**2 * d
        f = -gamma*(f_y)
        g = -gamma*(g_x)
        h = gamma**2 * h_xy
        u = gamma**2 * g_x
        v = gamma**2 * f_y
        w = -gamma*(d)
        return ConeCamera(a, b, c, f, g, h)


    def rotate_2_XYZ(self):
        """
        :return: the rotation matrix of the principal axis theorem in oder to get the XYZ frame
        """
        #XAX=0 for homogenous quadric
        #TODO CHECK IF MIXED TERMS ARE DOUBLED
        A = np.array([[self.a_xx, self.h_xy, self.g_zx],
                      [self.h_xy, self.b_yy, self.f_yz],
                      [self.g_zx, self.f_yz, self.c_zz]])
        #CHECK WHETHER EIG VALUES FULFILL CONE EQ!
        eigvalue, eigvector = np.linalg.eig(A)
        #TODO First two eigvalues pos, while third negative to fulfill cone eq
        #TODO RIGHT HAND RULE FULLFILLED FOR EIGVEC
        return eigvalue, eigvector


class ConeXYZ(Cone):
    def __init__(self, a_xx, b_yy, c_zz):
        if not (a_xx>0 and b_yy>0 and c_zz<0):
            raise ValueError("Coefficients do not form a cone")
        else:
            Cone.__init__(self, a_xx, b_yy, c_zz)


class lmn:
    def get_surface_normal(self):
        if not self.frame == "XYZ":
            raise TypeError('Only XYZ frame as input allowed')

        #Safaee-Rad p.628
        if self.a_xx > self.b_yy:
            n = np.sqrt((self.b_yy - self.c_zz) /
                        (self.a_xx - self.c_zz))
            m = 0
            l = np.sqrt((self.a_xx - self.b_yy) /
                        (self.a_xx - self.c_zz))
        #TODO implement other cases and two vectors as output inclusive test
        return np.array([l,m,n])


class ThreeDimensionalCircle:
    def __init__(self, position, orientation):
        self.position = position
        self.orientation = orientation


class Double3DCircle:
    '''
    More pseudo than real code
    '''
    def __init__(self, pos3DCircle, neg3DCircle):
        self.pos3DCircle = pos3DCircle
        self.neg3DCircle = neg3DCircle

    @staticmethod
    def constructByParamEllipse(ellipse):
        # TODO ELLIPSE AS INPUT
        cone_camera = Cone.ellipse_2_cone()
        XYZ, rot_2_camera_matrix = cone_camera.rotate_2_XYZ()
        cone_XYZ = Cone(XYZ)
        # Getting the plane normal first and then transform it to camera frame
        orientation = cone_XYZ.get_surface_normal()  # times rot matrix

