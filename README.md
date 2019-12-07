# Zool - Matplotlib-based Layout Library #
**Contributors: [Chris Arridge](https://www.lancaster.ac.uk/physics/about-us/people/chris-arridge), Lancaster University, c.arridge@lancaster.ac.uk**

`Zool` is a Python library for the layout of complex plots using `Matplotlib`.
In contrast to manually-specifying the dimensions and locations of each set of
axes, in `Zool` you can also specify that a axis fills the available space, or
takes its width/height/both from another plot element, or can inherit it from a
parent element or the width of all the child elements.  This is achieved using
constraint programming (using the `KiwiSolve` library) to compute the
size of each plot element.  Several factory routines are provided for generating
specific types of plots (at the moment a standard vertical stack plot, and a
triangle-type plot).

## Installation
Using setup tools launch `python setup.py install`.

## Licence
Copyright (C) 2017-2019 Chris Arridge and Lancaster University

This program is free software: you can redistribute it and/or modify it under
the terms of the GNU General Public License as published by the Free Software
Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.

## Basic Usage
A plot is created by creating a `zool.Plot` object.  The width and height can
be set.  In this example we will create a plot that has a fixed width of 10 cm
(not including left and right margins) and the height of the plot is determined
from the height of all the child elements (and any padding that is added).

	fig = zool.Plot(width=zool.Fixed(10.0), height=zool.FromChildren(),
				layout='vertical', padding=0.5,
				margin_left=2, margin_right=2)

Now we can add a number of child elements, here we just add four
fixed-height panels, three are 5 cm high, one is 10 cm high.  The
width comes from the parent element:

	fig.add('base',width=zool.FromParent(), height=zool.Fixed(5.0))
	fig.add('base',width=zool.FromParent(), height=zool.Fixed(5.0))
	fig.add('base',width=zool.FromParent(), height=zool.Fixed(5.0))
	fig.add('base',width=zool.FromParent(), height=zool.Fixed(5.0))

The plot is then laid out (the constraints solved) using the ``zool.Plot.layout`` method.  We can get a preview of the plot using the ``zool.Plot.preview`` method.

	fig.layout()
	fig.preview()

To make these plots we can then call ``zool.Plot.new`` and then each axis can be obtained using ``zool.Plot.axes``.

	fig.new()
	ax = fig.axes['0']
	plt.plot(np.sin(np.arange(0,2*np.pi,np.pi/64)))
	plt.show()

## Licence
Copyright (C) 2019 Chris Arridge and Lancaster University

This program is free software: you can redistribute it and/or modify it under
the terms of the GNU General Public License as published by the Free Software
Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
