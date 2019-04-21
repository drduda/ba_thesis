import numpy as np
import sympy as sy
import math
import geometry


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
    def construct_by_param(x_center, y_center, maj, min, rot):
        if maj < min:
            raise ValueError("Major axis needs to be bigger than minor")
        if rot > 180:
            raise ValueError("Not more than 180 degress rotation possible")
        x, y = sy.symbols('x y')
        rot = math.radians(rot)
        eq = sy.Eq(((((x - x_center) * math.cos(rot) + (y - y_center) * math.sin(rot)) ** 2) / (maj ** 2))
                   + ((((x - x_center) * math.sin(rot) - (y - y_center) * math.cos(rot)) ** 2) / (min ** 2)) - 1)
        eq = eq.expand(basic=True)
        p = sy.Poly(eq, x, y)
        coeff = p.coeffs()
        #For unique representation scaling is used
        coeff = [x / coeff[0] for x in coeff]
        a_xx = coeff[0]
        h_xy = coeff[1]/2
        g_x = coeff[2]/2
        b_yy = coeff[3]
        f_y = coeff[4]/2
        d = coeff[5]
        return ImpEllipse(a_xx, h_xy, b_yy, g_x, f_y, d)

    @staticmethod
    def get_angle(vert1, vert2):
        """
        Only for testing with wolfram alpha
        :param vert1:
        :param vert2:
        :return: degree in angle
        """
        x_axis = np.array([1, 0])
        input_axis = vert2 - vert1
        input_axis = input_axis / np.linalg.norm(input_axis)
        return math.degrees(np.arccos(np.dot(x_axis, input_axis)))


class Cone(Quadric):
    """
        Represents a cone which is described by the coefficients which its implicit equation has.
        Attribute self.a_xx is coefficient a for term x². Its most general form is:
        a*x**2 + b*y**2 + c*z**2 + 2*f*y*z + 2*g*z*x + 2*h*x*y + 2*u*x + 2*v*y + 2*w*z + d = 0
        Here the simplest form is represented
        All variable names are copied from Safaee-Rad's paper
    """
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
    def construct_by_ellipse(a_xx, h_xy, b_yy, g_x, f_y, d, focal_length):
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
        gamma = - focal_length
        a = gamma**2 * a_xx
        b = gamma**2 * b_yy
        c = d
        d = gamma**2 * d
        f = -gamma*(f_y)
        g = -gamma*(g_x)
        h = gamma**2 * h_xy
        #Not needed
        u = gamma**2 * g_x
        v = gamma**2 * f_y
        w = -gamma*(d)
        return ConeCamera(a, b, c, f, g, h)

    def get_ConeXYZ_and_t1(self):
        """
        :return: the rotation matrix of the principal axis theorem in oder to get the XYZ frame
        """
        def get_t1(eigvalue, eigvector):
            # The second and simplest to calculate row of t1
            m = np.zeros(3)
            for i, li in enumerate(eigvalue):
                t1 = (self.b_yy - li) * self.g_zx - (self.f_yz * self.h_xy)
                t2 = (self.a_xx - li) * self.f_yz - (self.g_zx * self.h_xy)
                t3 = -(self.a_xx - li) * (t1 / t2) / self.g_zx - self.h_xy / self.g_zx
                m[i] = 1 / math.sqrt(1 + (t1 / t2) ** 2 + t3 ** 2)

            np.testing.assert_almost_equal(m, np.absolute(eigvector[1]), decimal=2)

            #Change the column vector sing if necesary
            for i, elem in enumerate(eigvector[1]):
                if elem < 0:
                    eigvector[:, i] = eigvector[:, i] * -1

            if np.linalg.det(eigvector) < 0:
                eigvector[:, 2] = eigvector[:, 2] * -1

            return eigvector

        A = np.array([[self.a_xx, self.h_xy, self.g_zx],
                      [self.h_xy, self.b_yy, self.f_yz],
                      [self.g_zx, self.f_yz, self.c_zz]], dtype='float')
        eigvalue, eigvector = np.linalg.eigh(A)
        if np.sum(eigvalue<0) != 1:
            raise ValueError("Only with one negative eigenvalue a cone can be formed")
        idx = 0
        eigvalue[idx], eigvalue[2] = eigvalue[2], eigvalue[idx]
        eigvector[:, [idx, 2]] = eigvector[:, [2, idx]]

        t1 = get_t1(eigvalue, eigvector)

        if np.linalg.det(eigvector) < 0:
            raise ValueError("Determinant has to be 1")

        return ConeXYZ(eigvalue[0], eigvalue[1], eigvalue[2]), t1




class ConeXYZ(Cone):
    def __init__(self, a_xx, b_yy, c_zz):
        if not (a_xx>0 and b_yy>0 and c_zz<0):
            raise ValueError("Coefficients do not form a cone")

        Cone.__init__(self, a_xx, b_yy, c_zz)

    def get_ABCD(self, t3):
        a = t3
        # Declare the variables
        l1, l2, l3 = a[0][0], a[1][0], a[2][0]
        m1, m2, m3 = a[0][1], a[1][1], a[2][1]
        n1, n2, n3 = a[0][2], a[1][2], a[2][2]

        A = self.a_xx*(l1**2) + self.b_yy*(l2**2) + self.c_zz*(l3**2)
        B = self.a_xx*l1*n1 + self.b_yy*l2*n2 + self.c_zz*l3*n3
        C = self.a_xx*m1*n1 + self.b_yy*m2*n2 + self.c_zz*m3*n3
        D = self.a_xx*n1**2 + self.b_yy*n2**2 + self.c_zz*n3**2

        return ABCD(A, B, C, D)



class Lmn:
    def __init__(self, pos, neg):
        if(np.any(pos<0)):
            raise ValueError("Only positive values allowed")
        if(np.all(neg>=0)):
            raise ValueError("There has to be some negative value")
        self.pos = pos
        self.neg = neg

    @staticmethod
    def construct_by_XYZ(a_xx, b_yy, c_zz):
        #Safaee-Rad p.628
        if a_xx > b_yy:
            n = np.sqrt((b_yy - c_zz) /
                        (a_xx - c_zz))
            m = 0
            l = np.sqrt((a_xx - b_yy) /
                        (a_xx - c_zz))
            return Lmn(np.array([l, m, n]), np.array([-l, m, n]))
        elif b_yy > a_xx:
            n = np.sqrt((a_xx - c_zz) /
                        (b_yy - c_zz))
            m = np.sqrt((b_yy - a_xx) /
                        (b_yy - c_zz))
            l = 0
            return Lmn(np.array([l, m, n]), np.array(l, -m, n))
        elif b_yy == a_xx:
            return Lmn(np.array([0, 0, 1]), np.array([0, 0, 1]))

    def get_t3(self, positive):
        """
        get
        :param positive: True if positive
        :return: t3
        """
        if positive:
            l, m, n = self.pos[0], self.pos[1], self.pos[2]
        if not positive:
            l, m, n = self.neg[0], self.neg[1], self.neg[2]

        t3 = np.empty(shape=(3, 3))
        norm = math.sqrt(l**2 + m**2)
        t3[0][0] = -m/norm
        t3[0][1] = -l*n/norm
        t3[0][2] = l
        t3[1][0] = l/norm
        t3[1][1] = -m*n/norm
        t3[1][2] = m
        t3[2][0] = 0
        t3[2][1] = norm
        t3[2][2] = n
        return t3


class ABCD:
    def __init__(self, a, b, c, d):
        self.a = a
        self.b = b
        self.c = c
        self.d = d

    def get_not_transformed_pos(self, radius):
        z = self.a*radius/(math.sqrt(self.b**2 + self.c**2 -self.a*self.d))
        x = -self.b*z/self.a
        y = -self.c*z/self.a
        return np.array([x, y, z])


class Double3DCircle(geometry.DoubleCircle):
    @staticmethod
    def constructByParamEllipse(x_center, y_center, maj, min, rot, radius_3d_circle, focal_length=1):
        """
        Implements Safaee-Rad et al given the radius
        :param x_center: from ellipse
        :param y_center: from ellipse
        :param maj: semiaxis length of major ellipse axis
        :param min: semiaxis length of minor ellipse axis
        :param rot: counter clockwise rotation in degrees starting from x axis
        :param radius_3d_circle: radius of 3D circle
        :param focal_length:
        :return: Two 3D circle as Double3DCircle object
        """
        e = ImpEllipse.construct_by_param(x_center, y_center, maj, min, rot)

        return Double3DCircle.construct_by_ImpEllipse(e, radius_3d_circle, focal_length)

    @staticmethod
    def construct_by_ImpEllipse(e, radius_3d_circle, focal_length):
        cone_camera = ConeCamera.construct_by_ellipse(e.a_xx, e.h_xy, e.b_yy, e.g_x, e.f_y, e.d, focal_length)
        coneXYZ, t1 = cone_camera.get_ConeXYZ_and_t1()
        lmn = Lmn.construct_by_XYZ(coneXYZ.a_xx, coneXYZ.b_yy, coneXYZ.c_zz)
        t3 = lmn.get_t3(True)
        abcd = coneXYZ.get_ABCD(t3)
        not_transformed_pos = abcd.get_not_transformed_pos(radius_3d_circle)

        pos_orientation = t1.dot(lmn.pos)
        neg_orientation = t1.dot(lmn.neg)
        total_t = t1.dot(t3)
        position = t1.dot(t3).dot(not_transformed_pos)
        if np.any(position<0) == True:
            position = position * -1
        return Double3DCircle(pos_orientation, neg_orientation, position)
