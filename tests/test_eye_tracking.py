from unittest import TestCase


class TestIntersecting_lines(TestCase):
    def test_intersecting_lines(self):
        from geometry import Line
        from geometry import intersecting_lines
        import numpy as np

        l1 = Line([0, 1], [.5, .5])
        l2 = Line([0, -1], [.5, -.5])

        intersection = intersecting_lines([l1, l2])

        np.testing.assert_almost_equal([-1, 0], intersection)
