"""Functions for decorating a plot
"""
import numpy as np


def draw_zero_line(ax,linespec='-',colour=(0.5,0.5,0.5)):
	"""Draw a horizonal zero line

	Args:
	:param ax matplotlib axis: Axis to draw line onto.
	:param linespec str: Line style to draw (optional).
	:param colour tuple: Colour of the line.
	"""
	print('DEPRACATED')
	draw_zero_line(ax,0,linespec=linespec,colour=colour)


def hline(ax, y=0, linespec='-', colour=(0.5,0.5,0.5)):
	"""Draw a horizonal line

	Args:
	:param ax matplotlib axis: Axis to draw line onto.
	:param y float: Vertical level at which to draw the line.
	:param linespec str: Line style to draw (optional).
	:param colour tuple: Colour of the line.
	"""
	ax.plot(ax.get_xlim(),[y,y],linespec,color=colour)


def vline(ax, p, linespec='-',colour=(0.5,0.5,0.5)):
	"""Draw a vertical line at a given horizonal point(s).

	Args:
	:param ax matplotlib axis: Axis to draw line onto.
	:param p float or sequence: x coordinates of vertical lines to draw.
	:param linespec str: Line style to draw (optional).
	:param colour tuple: Colour of the line.
	"""
	yl = ax.get_ylim()
	if isinstance(p,(list,tuple,np.ndarray)):
		for x in p:
			ax.plot([x,x],yl,linespec,color=colour)


def ylabel(element_name, xoffset, text, fig, **kwargs):
	fig[element_name].ax.text(xoffset/fig.figure_width,
			0.5*(fig[element_name].yt+fig[element_name].yb)/fig.figure_height,
			text, transform=pl.gcf().transFigure,
			verticalalignment='top', horizontalalignment='center',
			rotation=90, rotation_mode='anchor', **kwargs)
