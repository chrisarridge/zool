""" This module implements various simplifying factories for generating layouts.
"""

# Zool modules.
import zool

def vertical_stack(heights, w=16.9, labels=None, **kwargs):
	"""This function returns a standard vertical stack of panels.

	Additional keyword arguments are passed straight through to the Plot class
	constructor.

	Args:
	:param heights list: List of panel heights (in cm).
	:param labels list: Optional list of panel labels.
	:return Zool plot object: Plot layout.
	"""
	fig = zool.Plot(width=zool.Fixed(w), height=zool.FromChildren(),
					layout='vertical', **kwargs)
	for i in range(len(heights)):
		if labels is None:
			fig.add('base', width=zool.FromParent(),
					height=zool.Fixed(heights[i]), label=str(i))
		else:
			fig.add('base', width=zool.FromParent(),
					height=zool.Fixed(heights[i]), label=labels[i])

	fig.layout()
	return fig


def triangle(n, d2d=4.0, d1d=1.0, m_padding=0.2, t_padding=0.1, **kwargs):
	"""This function returns a triangle plot of panels.

	Additional keyword arguments are passed straight through to the Plot class
	constructor.

	Args:
	:param n int: Number of variables to plot in the triangle (n x n).
	:param d2d float: Dimension of the (square) 2d histograms.
	:param d1d float: Dimension of the 1d marginals.
	:param m_padding float: Padding between vertical panels (cm).
	:param t_padding float: Padding between panels in each vertical set (cm).
	:return Zool plot object: Plot layout.
	"""

	fig = zool.Plot(width=zool.FromChildren(),
							height=zool.Named('tleft-frame'),
							layout='horizontal', padding=m_padding, **kwargs)

	# Setup the vertical frames that will hold all the histograms. The
	# arrangement is for (n+1) vertical frames to hold the n variables plus
	# one frame for the marginals for each horizontal row.
	fig.add('base', width=zool.Fixed(d1d),
				height=zool.FromChildren(),
				layout='vertical', padding=t_padding,
				label='tleft-frame')
	for i in range(n):
#		print('t{:1d}-frame'.format(i+1))
		fig.add('base', width=zool.Fixed(d2d),
				height=zool.FromChildren(),
				layout='vertical', padding=t_padding,
				label='t{:1d}-frame'.format(i+1))

	# Add marinal histograms to the left-hand frame, including some padding at
	# the top for alignment.
	fig.add('tleft-frame', width=zool.FromParent(),
				height=zool.Fixed(d1d),
				label='{:1d}-top-padding'.format(i+1))
	for i in range(n):
		fig.add('tleft-frame', width=zool.FromParent(),
				height=zool.Fixed(d2d),
				label='{:1d}-hist-vert'.format(i+1))

	# Add 1D marginal and 2D histograms in the other frames.
	for i in range(n):
		frame = 't{:1d}-frame'.format(i+1)

		# Add padding at the top for alignment.
		for j in range(i):
			fig.add(frame, width=zool.FromParent(),
				height=zool.Fixed(d2d),
				label='{:1d}-{:1d}-padding'.format(i+1,j+1))

		# Add 1d marginal at the top of the column.
		fig.add(frame, width=zool.FromParent(),
				height=zool.Fixed(d1d),
				label='{:1d}-hist'.format(i+1))

		# Add 2d histograms.
		for j in range(n-i):
			fig.add(frame, width=zool.FromParent(),
				height=zool.Fixed(d2d),
				label='{:1d}-{:1d}-hist'.format(i+1,j+1))

	# Finish the layout and make the figure.
	fig.layout()

	return fig
