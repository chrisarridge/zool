"""Testing of various layouts."""

import zool
import unittest


class TestFactory(unittest.TestCase):
	def test(self):
		tmp = zool.vertical_stack([5,5,10,10], padding=2, margin_left=2,
				margin_right=2.0, margin_top=2.0, margin_bottom=2,
				w=20)
		self.assertEqual(tmp.figure_width, 24)
		self.assertEqual(tmp.figure_height, 40)
		self.assertEqual(tmp['3'].yb, 2)
		self.assertEqual(tmp['3'].yt, 2+10)
		self.assertEqual(tmp['2'].yb, 2+10+2)
		self.assertEqual(tmp['2'].yt, 2+10+2+10)
		self.assertEqual(tmp['1'].yb, 2+10+2+10+2)
		self.assertEqual(tmp['1'].yt, 2+10+2+10+2+5)
		self.assertEqual(tmp['0'].yb, 2+10+2+10+2+5+2)
		self.assertEqual(tmp['0'].yt, 2+10+2+10+2+5+2+5)

if __name__ == '__main__':
    unittest.main()
