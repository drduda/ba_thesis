import projection
import numpy as np

class Analytical_Ellipse(projection.Ellipse):
    '''
    Wrapper class for an ellipse which adds the implicit function of that ellipse to it.
    For simpler testing, either an ellipse or just its parameters can be handed over as
    a kwargs.
    '''

    def __init__(self, ellipse=None, **kwargs):
        if ellipse:
            self.__class__ = type(ellipse.__class__.__name__,
                                  (self.__class__, ellipse.__class__),
                                  {})
            self.__dict__ = ellipse.__dict__
        else:
            self.major = kwargs.get('major')
            self.minor = kwargs.get('minor')
            self.center= kwargs.get('center')
            self.anti_clockwise_rot = kwargs.get('anti_clockwise_rot')

        #Get analytical coefficients for parameters



class Quadric:
    '''
    Can represent a quadric with max. 3 dimensions which is described by the coefficients which its implicit equation has.
    Attribute self.a_xx is coefficient a for term x². Its general form is:
    a*x**2 + b*y**2 + c*z**2 + 2*f*y*z + 2*g*z*x + 2*h*x*y + 2*u*x + 2*v*y + 2*w*z + d = 0
    All variable names are copied from Safaee-Rad's paper
    '''
    def __init__(self, frame, a_xx, b_yy, c_zz, f_yz, g_zx, h_xy, u_x=None, v_y=None, w_z=None, d=None):

        self.frame = frame

        self.a_xx = a_xx
        self.b_yy = b_yy
        self.c_zz = c_zz

        self.f_yz = f_yz
        self.g_zx = g_zx
        self.h_xy = h_xy
        if frame=='image':
            if not all([u_x, v_y, w_z, d]):
                raise TypeError('For the image frame all coefficients are needed')
            self.u_x = u_x
            self.v_y = v_y
            self.w_z = w_z

            self.d = d


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

        return Quadric('camera', a, b, c, f, g, h)

    def get_equation(self):
        '''
        Returns implicit equation of the quadric which can be copy pasted to Wolfram Alpha
        :return: String of implicit equation
        '''
        output = ''
        for key, value in self.__dict__.items():
            if key == 'frame':
                print(value)
            else:
                try:
                    output += str(value) + '*' + key[2:] + ' + '
                except:
                    output += key

        return output[:-2] + '=0'

    def rotational_transormation_matrix(self):
        """
        :return: the rotation matrix of the principal axis theorem.
        """
        #XAX=0 for homogenous quadric
        #TODO CHECK IF MIXED TERMS ARE DOUBLED
        A = np.array([[self.a_xx, self.h_xy, self.g_zx],
                      [self.h_xy, self.b_yy, self.f_yz],
                      [self.g_zx, self.f_yz, self.c_zz]])

        eigvalue, eigvector = np.linalg.eig(A)
        print(eigvector)

