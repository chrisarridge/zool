"""Demonstrate a simple vertical stack without using factory functions.
"""
import matplotlib.pyplot as plt

import zool

# Start Zool plot layout with a fixed width of 10cm, height calculated
# from children (by default), a vertical layout, and some padding/margins.
layout = zool.Layout(figwidth=10.0, layout='vertical', padding=0.5,
                     margin_left=2, margin_right=0.5, margin_top=0.5, margin_bottom=2.0)

# Add four panels, three with a height of 5cm and one with a height 2.5cm.
layout['a'] = zool.PlotElement(height=5.0)
layout['b'] = zool.PlotElement(height=5.0)
layout['c'] = zool.PlotElement(height=5.0)
layout['d'] = zool.PlotElement(height=2.5)

# Finalise the layout.
layout.layout()

# Generate the figure and save it.
fig = layout.figure()
ax = layout.axes("a")
ax = layout.axes("b")
ax = layout.axes("c")
ax = layout.axes("d")
plt.show()
#plt.savefig('simple_vertical_stack.pdf')
