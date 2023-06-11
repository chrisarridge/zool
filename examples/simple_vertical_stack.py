"""Demonstrate a simple vertical stack without using factory functions.
"""
import matplotlib.pyplot as plt
import numpy as np

import zool

# Start Zool plot layout with a fixed width of 10cm, height calculated
# from children (by default), a vertical layout, and some padding/margins.
layout = zool.Layout(figwidth=10.0, layout='vertical', padding=0.5,
                     margin_left=2, margin_right=0.5, margin_top=0.5, margin_bottom=2.0)

# Add four panels, three with a height of 5cm and one with a height 2.5cm.
layout['a'] = zool.PlotElement(height=5.0)
layout['b'] = zool.PlotElement(height=5.0)
layout['c'] = zool.PlotElement(height=2.5)

# Finalise the layout and preview it.
layout.layout()
layout.preview(show=False)
plt.savefig('simple-vertical-stack-preview.png')
plt.show()

# Generate the figure and save it.
theta = np.linspace(0, 2*np.pi, 360)

fig = layout.figure()
ax = layout.axes("a")
ax.plot(np.degrees(theta), np.sin(2*theta))
ax.set_xticklabels([])
ax.set_xticks(range(0,360,45))
ax.set_ylabel(r"$\sin(2\theta)$")

ax = layout.axes("b")
ax.plot(np.degrees(theta), np.sin(4*theta))
ax.set_xticklabels([])
ax.set_xticks(range(0,360,45))
ax.set_ylabel(r"$\sin(4\theta)$")

ax = layout.axes("c")
ax.plot(np.degrees(theta), np.sin(theta))
ax.set_ylabel(r"$\sin(\theta)$")
ax.set_xlabel(r"$\theta$ [deg]")
ax.set_xticks(range(0,360,45))

plt.savefig('simple-vertical-stack-plot.png')
plt.show()

