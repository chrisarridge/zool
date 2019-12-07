""" This module implements various classes for colours in plots.
"""

# Modules
import matplotlib.colors


### ========================================================================
###
### Colour Brewer colours
###
### ========================================================================
class ColourBrewer(object):
	"""This class implements a container for ColorBrewer colours.

	The class provides a mechanism to return colours (either as normalised RGB
	or hex) from the ColorBrewer project (colorbrewer.org). Eight palettes are
	available:

	* 'accent': 8 colours
	* 'dark2': 8 colours
	* 'paired': 12 colours
	* 'pastel1': 9 colours
	* 'pastel2': 8 colours
	* 'set1': 9 colours
	* 'set2': 8 colours
	* 'set3': 12 colours
	"""
	def __init__(self):
		""" Default constructor. """
		self._cb_rgb = dict()
		self._cb_hex = dict()
		self._cb_len = dict()

		# Add colours for 'accent' colour map.
		red = [0.498039, 0.745098, 0.992157, 1.000000, 0.219608, 0.941176, 0.749020, 0.400000 ];
		green = [0.788235, 0.682353, 0.752941, 1.000000, 0.423529, 0.007843, 0.356863, 0.400000 ];
		blue = [0.498039, 0.831373, 0.525490, 0.600000, 0.690196, 0.498039, 0.090196, 0.400000 ];
		self._cb_len['accent'] = len(red)
		for ii in range(len(red)):
			self._cb_rgb['accent',ii] = (red[ii],green[ii],blue[ii])
			self._cb_hex['accent',ii] = matplotlib.colors.to_hex((red[ii],green[ii],blue[ii]))

		# Add colours for 'dark2' colour map.
		red = [  0.105882, 0.850980, 0.458824, 0.905882, 0.400000, 0.901961, 0.650980, 0.400000 ];
		green = [0.619608, 0.372549, 0.439216, 0.160784, 0.650980, 0.670588, 0.462745, 0.400000 ];
		blue = [ 0.466667, 0.007843, 0.701961, 0.541176, 0.117647, 0.007843, 0.113725, 0.400000 ];
		self._cb_len['dark2'] = len(red)
		for ii in range(len(red)):
			self._cb_rgb['dark2',ii] = (red[ii],green[ii],blue[ii])
			self._cb_hex['dark2',ii] = matplotlib.colors.to_hex((red[ii],green[ii],blue[ii]))

		# Add colours for 'paired' colour map.
		red = [  0.650980, 0.121569, 0.698039, 0.200000, 0.984314, 0.890196, 0.992157, 1.000000, 0.792157, 0.415686, 1.000000, 0.694118 ];
		green = [0.807843, 0.470588, 0.874510, 0.627451, 0.603922, 0.101961, 0.749020, 0.498039, 0.698039, 0.239216, 1.000000, 0.349020 ];
		blue = [ 0.890196, 0.705882, 0.541176, 0.172549, 0.600000, 0.109804, 0.435294, 0.000000, 0.839216, 0.603922, 0.600000, 0.156863 ];
		self._cb_len['paired'] = len(red)
		for ii in range(len(red)):
			self._cb_rgb['paired',ii] = (red[ii],green[ii],blue[ii])
			self._cb_hex['paired',ii] = matplotlib.colors.to_hex((red[ii],green[ii],blue[ii]))

		# Add colours for 'pastel1' colour map.
		red = [  0.984314, 0.701961, 0.800000, 0.870588, 0.996078, 1.000000, 0.898039, 0.992157, 0.949020 ];
		green = [0.705882, 0.803922, 0.921569, 0.796078, 0.850980, 1.000000, 0.847059, 0.854902, 0.949020 ];
		blue = [ 0.682353, 0.890196, 0.772549, 0.894118, 0.650980, 0.800000, 0.741176, 0.925490, 0.949020 ];
		self._cb_len['pastel1'] = len(red)
		for ii in range(len(red)):
			self._cb_rgb['pastel1',ii] = (red[ii],green[ii],blue[ii])
			self._cb_hex['pastel1',ii] = matplotlib.colors.to_hex((red[ii],green[ii],blue[ii]))

		# Add colours for 'pastel2' colour map.
		red = [  0.701961, 0.992157, 0.796078, 0.956863, 0.901961, 1.000000, 0.945098, 0.800000 ];
		green = [0.886275, 0.803922, 0.835294, 0.792157, 0.960784, 0.949020, 0.886275, 0.800000 ];
		blue = [ 0.803922, 0.674510, 0.909804, 0.894118, 0.788235, 0.682353, 0.800000, 0.800000 ];
		self._cb_len['pastel2'] = len(red)
		for ii in range(len(red)):
			self._cb_rgb['pastel2',ii] = (red[ii],green[ii],blue[ii])
			self._cb_hex['pastel2',ii] = matplotlib.colors.to_hex((red[ii],green[ii],blue[ii]))

		# Add colours for 'set1' colour map.
		red = [  0.894118, 0.215686, 0.301961, 0.596078, 1.000000, 1.000000, 0.650980, 0.968627, 0.600000 ];
		green = [0.101961, 0.494118, 0.686275, 0.305882, 0.498039, 1.000000, 0.337255, 0.505882, 0.600000 ];
		blue = [ 0.109804, 0.721569, 0.290196, 0.639216, 0.000000, 0.200000, 0.156863, 0.749020, 0.600000 ];
		self._cb_len['set1'] = len(red)
		for ii in range(len(red)):
			self._cb_rgb['set1',ii] = (red[ii],green[ii],blue[ii])
			self._cb_hex['set1',ii] = matplotlib.colors.to_hex((red[ii],green[ii],blue[ii]))

		# Add colours for 'set2' colour map.
		red = [  0.400000, 0.988235, 0.552941, 0.905882, 0.650980, 1.000000, 0.898039, 0.701961 ];
		green = [0.760784, 0.552941, 0.627451, 0.541176, 0.847059, 0.850980, 0.768627, 0.701961 ];
		blue = [ 0.647059, 0.384314, 0.796078, 0.764706, 0.329412, 0.184314, 0.580392, 0.701961 ];
		self._cb_len['set2'] = len(red)
		for ii in range(len(red)):
			self._cb_rgb['set2',ii] = (red[ii],green[ii],blue[ii])
			self._cb_hex['set2',ii] = matplotlib.colors.to_hex((red[ii],green[ii],blue[ii]))

		# Add colours for 'set3' colour map.
		red = [  0.552941, 1.000000, 0.745098, 0.984314, 0.501961, 0.992157, 0.701961, 0.988235, 0.850980, 0.737255, 0.800000, 1.000000 ];
		green = [0.827451, 1.000000, 0.729412, 0.501961, 0.694118, 0.705882, 0.870588, 0.803922, 0.850980, 0.501961, 0.921569, 0.929412 ];
		blue = [ 0.780392, 0.701961, 0.854902, 0.447059, 0.827451, 0.384314, 0.411765, 0.898039, 0.850980, 0.741176, 0.772549, 0.435294 ];
		self._cb_len['set3'] = len(red)
		for ii in range(len(red)):
			self._cb_rgb['set3',ii] = (red[ii],green[ii],blue[ii])
			self._cb_hex['set3',ii] = matplotlib.colors.to_hex((red[ii],green[ii],blue[ii]))

	def get_hex(self, label, index):
		"""Return hex colour string for a colour in a given palette.

		Args:
		:param label str: Colour label from ColorBrewer.
		:param index int: Colour index in that pallette.
		:return str: Hex string #rrggbb.
		"""
		try:
			this_len = self._cb_len[label]
		except KeyError:
			raise ValueError('The ColourBrewer colour map <{}> is unknown to Zool'.format(label))
		else:
			if index<this_len:
				return(self._cb_hex[label,index])
			else:
				raise ValueError('The ColourBrewer colour map <{}> only has {} colours (requested index {})'.format(label,this_len,index))

	def get_rgb(self, label, index):
		"""Return RGB colour triple for a colour in a given palette.

		Args:
		:param label str: Colour label from ColorBrewer.
		:param index int: Colour index in that pallette.
		:param triple: Triple (rgb) cwith each component normalised to 1.0.
		"""
		try:
			this_len = self._cb_len[label]
		except KeyError:
			raise ValueError('The ColourBrewer colour map <{}> is unknown to Zool'.format(label))
		else:
			if index<this_len:
				return(self._cb_rgb[label,index])
			else:
				raise ValueError('The ColourBrewer colour map <{}> only has {} colours (requested index {})'.format(label,this_len,index))
