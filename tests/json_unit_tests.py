import unittest

import zool

class TestPlotElement(unittest.TestCase):
    def test_base_layout(self):
        """Check that we can serialise a base without any child items.
        """

        # Fixed width and set the height from a fixed aspect ratio (width/height).
        layout = zool.Layout(figwidth=10.0, figheight=zool.FixedAspect(4.0))
        layout.layout()
        self.assertAlmostEqual(layout["base"].width.value(), 10.0)
        self.assertAlmostEqual(layout["base"].height.value(), 2.5)

        # Serialise the layout to JSON.
        json_string = layout.to_json()

        # Now deserialise into a new layout object.
        layout2 = zool.Layout.from_json(json_string)
        self.assertAlmostEqual(layout2["base"].width.value(), 10.0)
        self.assertAlmostEqual(layout2["base"].height.value(), 2.5)


    def test_stack_with_horizontal_panel(self):
        """Test a vertical stack but where there is a horizontal panel split up horizontally.
        """
        layout = zool.Layout(figwidth=10.0, figheight=zool.FromChildren(), layout="vertical", padding=0.25,
                            margin_left=0.5, margin_right=0.5, margin_top=0.5, margin_bottom=0.5)     # omitting figheight means it defaults to from children
        layout["one"] = zool.PlotElement(height=2)
        layout["two"] = zool.PlotElement(height=2)
        layout["three"] = zool.PlotElement(height=3, padding=1, margin_left=0.5, margin_right=0.5, layout="horizontal")
        layout["three","four"] = zool.PlotElement(width=zool.Fill())
        layout["three","five"] = zool.PlotElement(width=zool.Fill())
        layout.layout()

        self.assertAlmostEqual(layout["one"].height.value(), 2)
        self.assertAlmostEqual(layout["two"].height.value(), 2)
        self.assertAlmostEqual(layout["three"].height.value(), 3)
        self.assertAlmostEqual(layout["one"].width.value(), 9)
        self.assertAlmostEqual(layout["two"].width.value(), 9)
        self.assertAlmostEqual(layout["three"].width.value(), 9)

        self.assertAlmostEqual(layout["four"].height.value(), 3)
        self.assertAlmostEqual(layout["four"].width.value(), 3.5)
        self.assertAlmostEqual(layout["five"].height.value(), 3)
        self.assertAlmostEqual(layout["five"].width.value(), 3.5)

        json_string = layout.to_json()

        layout2 = zool.Layout.from_json(json_string)

        self.assertAlmostEqual(layout2["one"].height.value(), 2)
        self.assertAlmostEqual(layout2["two"].height.value(), 2)
        self.assertAlmostEqual(layout2["three"].height.value(), 3)
        self.assertAlmostEqual(layout2["one"].width.value(), 9)
        self.assertAlmostEqual(layout2["two"].width.value(), 9)
        self.assertAlmostEqual(layout2["three"].width.value(), 9)

        self.assertAlmostEqual(layout2["four"].height.value(), 3)
        self.assertAlmostEqual(layout2["four"].width.value(), 3.5)
        self.assertAlmostEqual(layout2["five"].height.value(), 3)
        self.assertAlmostEqual(layout2["five"].width.value(), 3.5)

if __name__ == '__main__':
    unittest.main()

