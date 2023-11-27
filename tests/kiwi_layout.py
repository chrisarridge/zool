"""Testing showing how to calculate layout using Kiwisolver"""

import unittest

import kiwisolver as ks


class TestKiwiLayout(unittest.TestCase):
    def test(self):
        # Setup constrain programming variables.
        fig_w = ks.Variable("figure-width")
        fig_h = ks.Variable("figure-height")
        p1_w = ks.Variable("panel1-width")
        p1_h = ks.Variable("panel1-height")
        p2_w = ks.Variable("panel2-width")
        p2_h = ks.Variable("panel2-height")
        p2a_w = ks.Variable("panel2a-width")
        p2a_h = ks.Variable("panel2a-height")
        p2b_w = ks.Variable("panel2b-width")
        p2b_h = ks.Variable("panel2b-height")
        padding = ks.Variable("padding")

        # Setup solver.
        s = ks.Solver()

        # Setup constraints.
        c1 = fig_w - p1_w == 0
        c2 = fig_w - p2_w == 0
        c3 = p2_w - p2a_w - padding - p2b_w == 0
        c4 = p2a_w - p2b_w == 0
        c5 = fig_h - p1_h - padding - p2_h == 0
        c6 = p2a_h == p2_h
        c7 = p2b_h == p2_h
        c8 = padding == 1.0
        c9 = p1_w == 20.0
        c10 = p1_h == 5.0
        c11 = p2_h == 10.0

        s.addConstraint(c1 | "strong")
        s.addConstraint(c2 | "strong")
        s.addConstraint(c3 | "strong")
        s.addConstraint(c4 | "strong")
        s.addConstraint(c5 | "strong")
        s.addConstraint(c6 | "strong")
        s.addConstraint(c7 | "strong")
        s.addConstraint(c8 | "strong")
        s.addConstraint(c9 | "strong")
        s.addConstraint(c10 | "strong")
        s.addConstraint(c11 | "strong")

        s.updateVariables()

        # Check results
        self.assertEqual(fig_w.value(), 20)
        self.assertEqual(fig_h.value(), 16)
        self.assertEqual(p1_w.value(), 20)
        self.assertEqual(p1_h.value(), 5)
        self.assertEqual(p2_w.value(), 20)
        self.assertEqual(p2_h.value(), 10)
        self.assertEqual(p2a_w.value(), 9.5)
        self.assertEqual(p2a_h.value(), 10)
        self.assertEqual(p2b_w.value(), 9.5)
        self.assertEqual(p2b_h.value(), 10)
        self.assertEqual(padding.value(), 1.0)


if __name__ == "__main__":
    unittest.main()
