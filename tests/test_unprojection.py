from unittest import TestCase
from tests import test_transformation as trans
import numpy as np

places = 2


class TestImpEllipse(TestCase):
    def test_construct_by_param(self):
        from ellipse_unprojection import ImpEllipse
        e_param = ImpEllipse.construct_by_param(-1.53333, 1.1333, 3.218, 2.49266, 135)
        e_imp = ImpEllipse(1, 0.5, 1, 2.5, -1.5, -5)
        self.assertAlmostEqual(e_param.a_xx, e_imp.a_xx, places)
        self.assertAlmostEqual(e_param.h_xy, e_imp.h_xy, places)
        self.assertAlmostEqual(e_param.b_yy, e_imp.b_yy, places)
        self.assertAlmostEqual(e_param.g_x, e_imp.g_x, places)
        self.assertAlmostEqual(e_param.f_y, e_imp.f_y, places)
        self.assertAlmostEqual(e_param.d, e_imp.d, places)


class TestQuadric(TestCase):
    from ellipse_unprojection import ConeCamera
    from ellipse_unprojection import ImpEllipse
    from ellipse_unprojection import ConeXYZ
    from ellipse_unprojection import Lmn
    from ellipse_unprojection import Double3DCircle

    # Results from Safaee-Rad p.632

    e_imp = ImpEllipse(204.024, -102.452/2, 225.000, -127.567/2, -177.45/2, 66.976)
    from_ellipse = ConeCamera.construct_by_ellipse(204.024, -102.452, 225.000, -127.567, -177.45, 66.976, 1)
    cone_camera = ConeCamera(204.024, 225, 66.976, -177.452 / 2, -127.567 / 2, -102.452 / 2)
    cone_XYZ = ConeXYZ(274.281, 225.00, -3.281)
    surface_normal = np.array([0.421367, 0, 0.906890])
    lmn = Lmn(np.array([0.421367, 0, 0.906890]), np.array([-0.421367, 0, 0.906890]))
    t3_from_pos = lmn.get_t3(positive=True)
    abcd_from = cone_XYZ.get_ABCD(trans.t3)
    not_transformed_pos = abcd_from.get_not_transformed_pos(4)
    double3d_from = Double3DCircle.construct_by_ImpEllipse(e_imp, 4, 1)

    def test_construct_by_ellipse(self, from_ellipse=from_ellipse, cone_camera=cone_camera):
        self.assertAlmostEqual(from_ellipse.a_xx, cone_camera.a_xx, places)
        self.assertAlmostEqual(from_ellipse.b_yy, cone_camera.b_yy, places)
        self.assertAlmostEqual(from_ellipse.c_zz, cone_camera.c_zz, places)
        self.assertAlmostEqual(from_ellipse.f_yz, cone_camera.f_yz, places)
        self.assertAlmostEqual(from_ellipse.g_zx, cone_camera.g_zx, places)
        self.assertAlmostEqual(from_ellipse.h_xy, cone_camera.h_xy, places)

    def test_t1(self, cone_camera=cone_camera, cone_XYZ = cone_XYZ):
        _, t1_from = cone_camera.get_ConeXYZ_and_t1()
        self.assertAlmostEqual(np.linalg.det(t1_from), 1, places)
        np.testing.assert_almost_equal(t1_from, trans.t1)

    def test_construct_by_ImpEllipse(self, double3d_from = double3d_from):
        pos_true = np.array([11.830, 13.660, 27.811])
        orientation_true = np.array([-0.5, 0, -0.866025])
        decimal=2
        np.testing.assert_almost_equal(double3d_from.position, pos_true, decimal=decimal)
        np.testing.assert_almost_equal(double3d_from.posOrientation, orientation_true, decimal=decimal)

##todo what if eigvalues are not in the same order as safaee-rad



