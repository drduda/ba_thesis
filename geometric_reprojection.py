import numpy as np
import sympy as sy
import projection

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



class Cone:
    '''
    The cone is described by the coefficients which its implicit equation has.
    Attribute self.a_xx is coefficient a for term x². Its general form is:
    a*x**2 + b*y**2 + c*z**2 + 2*f*y*z + 2*g*z*x + 2*h*x*y + 2*u*x + 2*v*y + 2*w*z + d = 0
    '''
    def __init__(self, a_xx, b_yy, c_zz, f_yz, g_zx, h_xy, u_x, v_y, w_z, d):

        self.a_xx = a_xx
        self.b_yy = b_yy
        self.c_zz = c_zz

        self.f_yz = f_yz
        self.g_zx = g_zx
        self.h_xy = h_xy

        self.u_x = u_x
        self.v_y = v_y
        self.w_z = w_z

        self.d = d


    @staticmethod
    def construct_by_ellipse():
        pass
