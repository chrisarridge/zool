import unittest

import zool


class TestPlotElement(unittest.TestCase):
    def test_base_layout(self):
        """Test the base size is correct without any child items."""

        # Fixed width and height.
        layout1 = zool.Layout(figwidth=10.0, figheight=5.0)
        layout1.layout()
        # layout1._setup_constraints()
        # layout1.solver.updateVariables()
        self.assertAlmostEqual(layout1["base"].width.value(), 10.0)
        self.assertAlmostEqual(layout1["base"].height.value(), 5.0)

        # Fixed width and set the height from a fixed aspect
        # ratio (width/height).
        layout2 = zool.Layout(figwidth=10.0, figheight=zool.FixedAspect(4.0))
        layout2.layout()
        # layout2._setup_constraints()
        # layout2.solver.updateVariables()
        self.assertAlmostEqual(layout2["base"].width.value(), 10.0)
        self.assertAlmostEqual(layout2["base"].height.value(), 2.5)

        # Fixed height and set the width from a fixed aspect
        # ratio (width/height).
        layout3 = zool.Layout(figwidth=zool.FixedAspect(4.0), figheight=4.0)
        layout3.layout()
        # layout3._setup_constraints()
        # layout3.solver.updateVariables()
        self.assertAlmostEqual(layout3["base"].width.value(), 16.0)
        self.assertAlmostEqual(layout3["base"].height.value(), 4.0)

    def test_simple_vertical_stack(self):
        """Check that we can construct a simple vertical stack"""
        layout = zool.Layout(
            figwidth=10.0,
            layout="vertical",
            padding=0.1,
            margin_left=0.5,
            margin_right=0.5,
            margin_top=0.5,
            margin_bottom=0.5,
        )  # omitting figheight means it defaults to from children
        layout["a"] = zool.PlotElement(height=4.0)
        layout["b"] = zool.PlotElement(height=4.0)
        layout["c"] = zool.PlotElement(height=4.0)
        layout["d"] = zool.PlotElement(height=2.0)
        layout.layout()

        # layout._setup_constraints()
        # layout.solver.updateVariables()

        # The total plot height will now
        # be (0.5 + 0.5) + (4 + 4 + 4 + 2) + 3*0.1
        self.assertAlmostEqual(
            layout["base"].height.value(),
            (0.5 + 0.5) + (4 + 4 + 4 + 2) + 3 * 0.1,
        )

    def test_simple_vertical_stack_with_named(self):
        """Test vertical stack where height of one panel is from another."""
        layout = zool.Layout(
            figwidth=10.0,
            layout="vertical",
            padding=0.1,
            margin_left=0.5,
            margin_right=0.5,
            margin_top=0.5,
            margin_bottom=0.5,
        )  # omitting figheight means it defaults to from children
        layout["a"] = zool.PlotElement(height=4.0)
        layout["b"] = zool.PlotElement(height=zool.Named("d"))
        layout["c"] = zool.PlotElement(height=4.0)
        layout["d"] = zool.PlotElement(height=2.0)
        layout.layout()
        # layout._setup_constraints()
        # layout.solver.updateVariables()
        # print(layout.solver.dumps())
        # layout.display()

        self.assertAlmostEqual(layout["a"].height.value(), 4)
        self.assertAlmostEqual(layout["b"].height.value(), 2)
        self.assertAlmostEqual(layout["c"].height.value(), 4)
        self.assertAlmostEqual(layout["d"].height.value(), 2)
        self.assertAlmostEqual(
            layout["base"].height.value(),
            (0.5 + 0.5) + (4 + 2 + 4 + 2) + 3 * 0.1,
        )

    def test_simple_vertical_stack_with_split(self):
        """Test a vertical stack with one element split vertically in two."""
        layout = zool.Layout(
            figwidth=10.0,
            layout="vertical",
            padding=0.1,
            margin_left=0.5,
            margin_right=0.5,
            margin_top=0.5,
            margin_bottom=0.5,
        )  # omitting figheight means it defaults to from children
        layout["a"] = zool.PlotElement(height=4.0)
        layout["b"] = zool.PlotElement(height=4.0)
        layout["c"] = zool.PlotElement(
            height=zool.FromChildren(), margin_top=0.5, margin_bottom=0.5
        )
        layout["d"] = zool.PlotElement(height=2.0)
        layout["c", "ca"] = zool.PlotElement(height=2.0)
        layout["c", "cb"] = zool.PlotElement(height=2.0)
        layout.layout()
        # layout._setup_constraints()
        # layout.solver.updateVariables()
        # print(layout.solver.dumps())
        # layout.display()

        self.assertAlmostEqual(layout["a"].height.value(), 4)
        self.assertAlmostEqual(layout["b"].height.value(), 4)
        self.assertAlmostEqual(layout["c"].height.value(), 5)
        self.assertAlmostEqual(layout["d"].height.value(), 2)
        self.assertAlmostEqual(
            layout["base"].height.value(),
            (0.5 + 0.5) + (4 + 4 + 5 + 2) + 3 * 0.1,
        )

    def test_simple_vertical_stack_filled(self):
        """Construct a vertical stack using filling of the available space."""
        layout = zool.Layout(
            figwidth=10.0,
            figheight=17.0,
            layout="vertical",
            padding=0.25,
            margin_left=0.5,
            margin_right=0.5,
            margin_top=0.5,
            margin_bottom=0.5,
        )  # omitting figheight means it defaults to from children
        layout["a"] = zool.PlotElement(height=zool.Fill())
        layout["b"] = zool.PlotElement(height=zool.Fill())
        layout["c"] = zool.PlotElement(height=zool.Fill())
        layout["d"] = zool.PlotElement(height=zool.Fill())
        layout["e"] = zool.PlotElement(height=zool.Fill())
        layout.layout()
        # layout._setup_constraints()
        # layout.solver.updateVariables()
        # print(layout.solver.dumps())
        # layout.display()

        # The height of the plot is 17, with a margin of 0.5 and the top and
        # bottom and padding of 0.25, so 17 - (0.5 + 0.5) - (4*0.25) = 15
        # remaining, divided among 5 panels = 3
        self.assertAlmostEqual(layout["a"].height.value(), 3)
        self.assertAlmostEqual(layout["b"].height.value(), 3)
        self.assertAlmostEqual(layout["c"].height.value(), 3)
        self.assertAlmostEqual(layout["d"].height.value(), 3)
        self.assertAlmostEqual(layout["e"].height.value(), 3)

    def test_simple_vertical_stack_fixedaspect(self):
        """Test a simple vertical stack using a fixed aspect ratio."""
        layout = zool.Layout(
            figwidth=10.0,
            layout="vertical",
            padding=0.25,
            margin_left=0.5,
            margin_right=0.5,
            margin_top=0.5,
            margin_bottom=0.5,
        )  # omitting figheight means it defaults to from children
        layout["a"] = zool.PlotElement(height=zool.FixedAspect(2))
        layout["b"] = zool.PlotElement(height=zool.FixedAspect(2))
        layout["c"] = zool.PlotElement(height=zool.FixedAspect(2))
        layout["d"] = zool.PlotElement(height=zool.FixedAspect(2))
        layout.layout()
        # layout._setup_constraints()
        # layout.solver.updateVariables()
        # print(layout.solver.dumps())
        # layout.display()
        # for id in layout._elements:
        #     print(id,layout[id].height.value())

        # Each panel has an aspect ratio is 2 so with a width of 9
        # then their heights will be 4.5, the total plot height
        # will be 0.75 + 2*0.5 + 4*4.5 = 19.75
        self.assertAlmostEqual(layout["a"].height.value(), 4.5)
        self.assertAlmostEqual(layout["b"].height.value(), 4.5)
        self.assertAlmostEqual(layout["c"].height.value(), 4.5)
        self.assertAlmostEqual(layout["d"].height.value(), 4.5)
        self.assertAlmostEqual(layout["base"].height.value(), 19.75)

    def test_stack_with_horizontal_panel(self):
        """Test a vertical stack including a horizontal split panel."""
        layout = zool.Layout(
            figwidth=10.0,
            figheight=zool.FromChildren(),
            layout="vertical",
            padding=0.25,
            margin_left=0.5,
            margin_right=0.5,
            margin_top=0.5,
            margin_bottom=0.5,
        )  # omitting figheight means it defaults to from children
        layout["one"] = zool.PlotElement(height=2)
        layout["two"] = zool.PlotElement(height=2)
        layout["three"] = zool.PlotElement(
            height=3,
            padding=1,
            margin_left=0.5,
            margin_right=0.5,
            layout="horizontal",
        )
        layout["three", "four"] = zool.PlotElement(width=zool.Fill())
        layout["three", "five"] = zool.PlotElement(width=zool.Fill())
        layout.layout()
        # layout._setup_constraints()
        # layout.solver.updateVariables()
        # layout.display()
        # print(layout.solver.dumps())
        # for id in layout._elements:
        #     print(id,layout[id].width.value())
        layout.preview()
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


if __name__ == "__main__":
    unittest.main()
