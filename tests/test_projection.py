from unittest import TestCase


class TestProjeciton(TestCase):
    def test_get_ellipse_param_dict(self):
        places = 3

        from projection import Eye, Pupil
        import numpy as np
        e = Eye(np.array([0.0, -5.0, 0.0]), 1.2)

        p = Pupil(e, [0.0, 0.0, 0.2], resolution=50).get_ellipse_param_dict()
        self.assertAlmostEqual(0, p["x_center"])
        self.assertAlmostEqual(0, p["y_center"])
        self.assertAlmostEqual(p["maj"], p["min"], places)

        p = Pupil(e, [30.0, 30.0, 0.2], resolution=50).get_ellipse_param_dict()
        self.assertGreater(p["x_center"], 0)
        self.assertGreater(p["y_center"], 0)
        self.assertAlmostEqual(p["rot"], 135, delta=15)