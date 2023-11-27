import unittest

import zool


class TestPlotElement(unittest.TestCase):
    def test(self):
        element = zool.PlotElement()
        self.assertIsNotNone(element.id)
        self.assertIsInstance(element.id, str)

        element.id = "test"
        self.assertIsInstance(element.id, str)
        self.assertEqual(element.id, "test")

        with self.assertRaises(TypeError):
            element.id = 42

        element = zool.PlotElement(id="test")
        self.assertIsInstance(element.id, str)


#        self.assertIsInstance(element.to_serialised_dict(), dict)


class TestLayoutSetting(unittest.TestCase):
    """Check that a Layout object __setitem__ correctly raises exceptions."""

    def test_incorrect_arg(self):
        layout = zool.Layout()
        with self.assertRaises(ValueError):
            layout["base", "a", "b"] = zool.PlotElement()


if __name__ == "__main__":
    unittest.main()
