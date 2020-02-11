""" Core definitions.
"""

# Required standard packages
import matplotlib.pyplot
import matplotlib.patches
import matplotlib.colors
import enum
import collections
import kiwisolver as ks
import json
# KiwiSolver for constraint programming.
import kiwisolver as ks

# Zool modules
import zool.colours



## ========================================================================
##
## Layout sizing types.
##
## ========================================================================
class Fixed:
	def __init__(self, s):
		self._size = s
	@property
	def size(self):
		return self._size

class FixedAspect:
	def __init__(self, s):
		self._aspect = s
	@property
	def aspect(self):
		return self._aspect

class FromChildren:
	def __init__(self):
		pass

class FromParent:
	def __init__(self):
		pass

class Fill:
	def __init__(self):
		pass

class Named:
	def __init__(self, id):
		self._id = id

	@property
	def id(self):
		return self._id

def _constraint_serialiser(v):
	"""Helper function to turn constraints into something that can be serialised"""
	if isinstance(v, Fixed):
		return {'constraint':'fixedDimension', 'value':v.size}
	elif isinstance(v, FixedAspect):
		return {'constraint':'fixedAspectRatio', 'value':v.aspect}
	elif isinstance(v, FromChildren):
		return {'constraint':'fromChildren'}
	elif isinstance(v, FromParent):
		return {'constraint':'fromParent'}
	elif isinstance(v, Fill):
		return {'constraint':'fill'}
	elif isinstance(v, Named):
		return {'constraint':'named', 'value':v.id}
	else:
		raise ValueError('Unknown constraint type')



def _constraint_deserialiser(v):
	"""Helper function to turn serialised constraints back into constraints"""
	if not isinstance(v, dict):
		raise ValueError('Supplied variable is not a dictionary')
	if 'constraint' not in v:
		raise ValueError('Supplied dictionary does not have a "constraint" entry')

	if v['constraint']=='fixedDimension':
		if 'value' not in v:
			raise ValueError('Require a value for a fixedDimension constraint')
		else:
			return Fixed(float(v['value']))
	elif v['constraint']=='fixedAspectRatio':
		if 'value' not in v:
			raise ValueError('Require a value for a fixedAspectRatio constraint')
		else:
			return FixedAspect(float(v['value']))
	elif v['constraint']=='named':
		if 'value' not in v:
			raise ValueError('Require a panel id for a named width/height constraint')
		else:
			return Named(v['value'])
	elif v['constraint']=='fill':
		return Fill()
	elif v['constraint']=='fromChildren':
		return FromChildren()
	elif v['constraint']=='fromParent':
		return FromParent()
	else:
		raise UserError('Unknown constraint type <{}>'.format(v['constraint']))


## ========================================================================
##
## Exceptions
##
## ========================================================================
class ZoolError(Exception):
	"""Base class for Zool exceptions."""
	pass

class InappropriateConstraint(ZoolError):
	"""Exception raised for errors in the constraints provided.

	Attributes:
		:param: constraint str: Constraint provided.
		:param: label str: Label that the constraint was provided to
		:param: message str: Message.
	"""

	def __init__(self, constraint, label, message):
		self.constraint = constraint
		self.label = label
		self.message = message




## ========================================================================
##
## Plot element that makes up part of a plot.
##
## ========================================================================
class PlotElement(object):
	"""This class implements a core element of a Zool plot layout."""

	def __init__(self):
		"""Default constructor.
		"""
		# Margins.
		self.margin_left = 0
		self.margin_right = 0
		self.margin_top = 0
		self.margin_bottom = 0

		# Dimensions of the element. We also have some flags so that we can
		# determine if the dimensions have been properly set yet, and where
		# the dimension information originates.
		self.width = ks.Variable()
		self.height = ks.Variable()
		self.width_constraint = 'none'
		self.height_constraint = 'none'

		# Coordinates of the four edges of the element.
		self.xl = 0.0
		self.xr = 0.0
		self.yt = 0.0
		self.yb = 0.0

		# Layout control information: How does this element lay out its child
		# elements, by row or column? What padding is there between elements?
		self.layout = 'none'
		self.padding = 0.0

		# Label for this element.
		self.label = ''

		# Figure axis.
		self.ax = None

		# Parent and child nodes for the linked list.
		self.parent = None
		self.children = dict()

	def to_serialised_dict(self):
		child_labels = []
		for v in self.children:
			child_labels.append(v)

		d = {'width': _constraint_serialiser(self.width_constraint),
			'height': _constraint_serialiser(self.height_constraint),
			'marginLeft': self.margin_left,
			'marginRight': self.margin_right,
			'marginTop': self.margin_top,
			'marginBottom': self.margin_bottom,
			'layout': self.layout, 'padding': self.padding,
			'label': self.label, 'parentLabel':'' if self.parent is None else self.parent.label,
			'childLabels':child_labels}

		return d


class Figure(collections.MutableMapping):
	"""This class does all the layout of a new Zool figure layout.

	:notes:
	Figure/element dimensions can be determined by one of the following methods:
		* zool.Fixed: dimensions are fixed and defined via 'width' or 'height'.
		* zool.FromChildren: dimensions come from child elements.
		* zool.FromParent: dimensions come from parent elements.
		* zool.Fill: dimensions are figured out by filling the space.
		* zool.Named: dimensions are set to those of a named element.
		* zool.FixedAspect: dimensions have a fixed aspect ratio.
	"""

	def __init__(self, figwidth=Fixed(0.0), figheight=Fixed(0.0),
					margin_left=0.0, margin_right=0.0,
					margin_top=0.0, margin_bottom=0.0,
					layout='vertical', padding=0.0):
		"""Default constructor.

		Args:
		:param figwidth: Width of the figure, base size is adjusted re: margins.
		:param figheight: Height of the figure, base is adjusted re: margins.
		:param margin_left float: Width of the margin on the left-hand side [cm].
		:param margin_right float: Width of the margin on the right-hand side [cm].
		:param margin_top float: Height of the margin at the top of the plot [cm].
		:param margin_bottom float: Height of the margin at the bottom of the plot [cm].
		:param layout str: Is the figure layed out with each element horizontally ('horizontal') or vertically ('vertical').
		:param padding float: How much padding is there between elements [cm].
		"""

		self.store = dict()

		self.solver = ks.Solver()

		self.label_index = 0

		self.fig_width_constraint = figwidth
		self.fig_height_constraint = figheight

		# All the plot elements are arranged in a tree structure, built
		# from a linked list of PlotElement objects. Base is the root of
		# this tree.
		self.base = PlotElement()
		self.base.label = 'base'
		self.base.width.setName('base-w')
		self.base.height.setName('base-h')
		self.parent = None

		# Set base plot element parameters.
		if isinstance(figwidth, Fixed):
			self.solver.addConstraint((self.base.width == figwidth.size -
									margin_left - margin_right) | 'required')
		elif isinstance(figwidth, FromChildren):
			pass
		elif isinstance(figwidth, Named):
			pass
		else:
			raise InappropriateConstraint(type(figwidth),'base','Figure width setup can only be \
						constrained using Fixed, FromChildren or Named.')
		self.base.width_constraint = figwidth

		if isinstance(figheight, Fixed):
			self.solver.addConstraint((self.base.height == figheight.size -
									margin_bottom - margin_top) | 'required')
		elif isinstance(figheight, FromChildren):
			pass
		elif isinstance(figheight, Named):
			pass
		else:
			raise InappropriateConstraint(type(figheight),'base','Figure height setup can only be \
						constrained using Fixed, FromChildren or Named.')
		self.base.height_constraint = figheight

		self.base.margin_left = margin_left
		self.base.margin_right = margin_right
		self.base.margin_top = margin_top
		self.base.margin_bottom = margin_bottom
		self.base.padding = padding
		if layout=='horizontal':
			self.base.layout = 'horizontal'
		elif layout=='vertical':
			self.base.layout = 'vertical'
		else:
			raise ValueError('Unknown layout method <{}> (should be horizontal or vertical)'.format(layout))

		# Initialise the dictionary (we are subclassing the dict class).
		self.store['base'] = self.base

		# Store the full figure dimensions - although this won't be determined until we
		# complete the layout.
		self.figure_width = 0.0
		self.figure_height = 0.0

	## ------------------------------------------------------------------------
	## Serialiser to generate json figure configuration.
	def to_json(self, filename):
		delements = {}
		for k,v in self.store.items():
			if not k=='base':
				delements[k] = v.to_serialised_dict()

		d = {'figureWidthConstraint': _constraint_serialiser(self.fig_width_constraint),
			'figureHeightConstraint': _constraint_serialiser(self.fig_height_constraint),
			'marginLeft': self.base.margin_left,
			'marginRight': self.base.margin_right,
			'marginTop': self.base.margin_top,
			'marginBottom': self.base.margin_bottom,
			'padding': self.base.padding,
			'layout': self.base.layout,
			'elements': delements}

		with open(filename, 'w') as fh:
			json.dump(d, fh)

	## ------------------------------------------------------------------------
	## Make new object from json.
	@staticmethod
	def from_json(filename):
		with open(filename, 'r') as fh:
			d = json.load(fh)

		# TODO: we need to sanity-check the json
		fig = Figure(figwidth=_constraint_deserialiser(d['figureWidthConstraint']),
				figheight=_constraint_deserialiser(d['figureHeightConstraint']),
				margin_left=d['marginLeft'], margin_right=d['marginRight'],
				margin_top=d['marginTop'], margin_bottom=d['marginBottom'],
				layout=d['layout'], padding=d['padding'])
		for k,v in d['elements'].items():
			fig.add(v['parentLabel'], label=k,
					width=_constraint_deserialiser(v['width']),
					height=_constraint_deserialiser(v['height']),
					padding=v['padding'], layout=v['layout'])

		fig.layout()

		return fig

	## ------------------------------------------------------------------------
	## Collection iteration methods
	def __iter__(self):
		""" Iterator over the plot elemnts.
		"""
		return iter(self.store)

	def __len__(self):
		""" Length of the plot elemnts.
		"""
		return len(self.store)

	def __getitem__(self, key):
		""" Get an item from the plot elements.

		Args:
		:param key str: Key for the corresponding value to get.
		"""
		return(self.store[key])

	def __setitem__(self, key, val):
		""" Don't allow setting of plot elements.
		"""
		raise UserError('Cannot set dictionary items in Plot objects (tried setting <{}>).'.format(key))

	def __delitem__(self, key):
		""" Delete a plot element.

		Args:
		:param key str: Key for the item to delete.
		"""
		del self.store[key]


	## ------------------------------------------------------------------------
	## Add method
	def add(self, parent_label, label=None, width=FromChildren(),
				height=FromChildren(), padding=0.0, layout='vertical'):
		"""Add a plot element to this figure.

		If width/height parameters are not set then they will be determined from
		their child elements.  If floats then a specific width/height will be
		set.  If a string then the width/height will be taken from the named
		plot element.

		Args:
		:param parent_label str: What is the parent element for this new element.
		:param label str: What is the label for this new element.
		:param width: Width of the element.
		:param height: Height of the element.
		:param layout str: Is the figure layed out with each element horizontally ('horizontal') or vertically ('vertical').
		:param padding float: How much padding is there between elements [cm].
		"""

		# Find the parent node.
		p = self.store[parent_label]

		# Generate a label if we need to.
		self.label_index += 1
		if label==None:
			label = 'id_{:2d}'.format(self.label_index)

		# Make the new element.
		f = PlotElement()
		f.label = label
		f.width.setName(label+'-w')
		f.height.setName(label+'-h')

		# Setup the frame.
		if isinstance(width,Fixed):
			self.solver.addConstraint((f.width == width.size) | 'required')
		elif isinstance(width,FromChildren):
			pass
		elif isinstance(width,FromParent):
			self.solver.addConstraint((f.width == p.width) | 'required')
		elif isinstance(width, FixedAspect):
			self.solver.addConstraint((f.width == width.aspect*f.height))
		elif isinstance(width,Fill):
			pass
		elif isinstance(width,Named):
			pass
		else:
			raise InappropriateConstraint(width,label,'Unknown width constraint.')
		f.width_constraint = width

		if isinstance(height,Fixed):
			self.solver.addConstraint((f.height == height.size) | 'required')
		elif isinstance(height,FromChildren):
			pass
		elif isinstance(height,FromParent):
			self.solver.addConstraint((f.height == p.height) | 'required')
		elif isinstance(height, FixedAspect):
			self.solver.addConstraint((f.width == height.aspect*f.height))
		elif isinstance(height,Fill):
			pass
		elif isinstance(height,Named):
			pass
		else:
			raise InappropriateConstraint(type(height),label,'Unknown height constraint.')
		f.height_constraint = height

		if layout=='horizontal':
			f.layout = 'horizontal'
		elif layout=='vertical':
			f.layout = 'vertical'
		else:
			raise ValueError('Unknown layout method <{}> (should be horizontal or vertical)'.format(layout))

		f.padding = padding

		# Add the object to the global dictionary, add it as a child of the
		# parent, and set the parent within this PlotElement
		self.store[label] = f
		p.children[label] = f
		f.parent = p




	## ------------------------------------------------------------------------
	## Show the elements in the plot.
	def show(self):
		""" Show all the elements in the plot.

		:notes: The algorithm recursively processes each node.
		"""
		def traverse(f,level):
			# Display information about this node.
			if f.parent==None:
				print('Node={} w={} h={} x=({},{}) y=({},{})'.format(f.label, f.width.value(), f.height.value(), f.xl, f.xr, f.yb, f.yt))
			else:
				print('{}Node={} w={} h={} x=({},{}) y=({},{})'.format(' '*level, f.label, f.width.value(), f.height.value(), f.xl, f.xr, f.yb, f.yt))

			# Recursively process child nodes.
			for key in f.children:
				traverse(f.children[key], level+1)

		traverse(self.base,0)


	## ------------------------------------------------------------------------
	## Layout the entire figure.
	def layout(self):
		"""Layout figure.

		This method runs through the algorithm laying out the plot elements,
		solving all the constraints to figure out where the plot elements are
		and their dimensions.

		:notes:
		* The algorithm uses two embedded recursive functions.
		* tr_dimensions() recursively runs through the elements setting up
			constraints for the solver. The solver then figures out the
			dimensions of each element using the constraints.
		* Then a second recursive function (tr_coordinates) uses the calculated
			dimensions to work out the coordinates of each element.
		* The final step is to calculate the width and height of the figure.
		"""

		def tr_dimensions(f):
			"""Calculate dimensions for a given plot element.

			Args:
			:param f PlotElement object: The plot element to calculate.

			:notes: This function will recursively process child elements.
			"""
			# We calculate the sum of our child node widths and heights.
			if f.layout=='vertical':
				wsum = 0.0
				hsum = (len(f.children)-1)*f.padding
			elif f.layout=='horizontal':
				wsum = (len(f.children)-1)*f.padding
				hsum = 0.0
			wfill = []
			hfill = []
			for key, child in f.children.items():
				if isinstance(child.width_constraint, Fixed):
					wsum += child.width
				if isinstance(child.height_constraint, Fixed):
					hsum += child.height

				if isinstance(child.width_constraint, Fill):
					wfill.append(key)
				if isinstance(child.height_constraint, Fill):
					hfill.append(key)

				if isinstance(child.width_constraint, FromChildren):
					wsum += child.width
				if isinstance(child.height_constraint, FromChildren):
					hsum += child.height

				if isinstance(child.width_constraint, FixedAspect):
					wsum += child.width
				if isinstance(child.height_constraint, FixedAspect):
					hsum += child.height

				if isinstance(child.width_constraint, Named):
					wsum += child.width
				if isinstance(child.height_constraint, Named):
					hsum += child.height

			# Add constraints for where we get our width/height from our child nodes.
			if isinstance(f.height_constraint, FromChildren):
				if f.layout == 'vertical':
					self.solver.addConstraint((f.height==hsum) | 'required')
			if isinstance(f.width_constraint, FromChildren):
				if f.layout == 'horizontal':
					self.solver.addConstraint((f.width==wsum) | 'required')

			# Add constraints for where we have child nodes that need filling.
			if not (len(hfill)==0):
				for key in hfill:
					self.solver.addConstraint((f.children[key].height == (f.height-hsum)/float(len(hfill))) | 'strong')
			if not (len(wfill)==0):
				for key in wfill:
					self.solver.addConstraint((f.children[key].width == (f.width-wsum)/float(len(wfill))) | 'strong')

			# named node
			if isinstance(f.width_constraint, Named):
				self.solver.addConstraint((f.width==self.store[f.width_constraint.id].width) | 'strong')
			if isinstance(f.height_constraint, Named):
				self.solver.addConstraint((f.height==self.store[f.height_constraint.id].height) | 'strong')

			# recursively process child nodes
			for key, child in f.children.items():
				tr_dimensions(child)


		def tr_coordinates(f):
			"""Calculate coordinates for a given plot element.

			Args:
			:param f PlotElement object: The plot element to calculate.

			:notes: This function will recursively process child elements.
			"""
			# These are offsets (from the parent coordinates) for this level of
			# the tree. If we are stepping across multiple sibling elements at the
			# same level, then these will increment so that we have the offset from
			# the beginning of each element
			dx = 0.0
			dy = 0.0

			# If this is the base element, then set the coordinates.
			if f.label=='base':
				f.xl = f.margin_left
				f.xr = f.width.value() + f.margin_left
				f.yt = f.height.value() + f.margin_bottom
				f.yb = f.margin_bottom

			# Process all the child nodes, recursively processing as necessary.
			for key in f.children:

				# Set the coordinates.
				f.children[key].xl = f.xl + dx
				f.children[key].yt = f.yt - dy
				f.children[key].xr = f.xl + dx + f.children[key].width.value()
				f.children[key].yb = f.yt - dy - f.children[key].height.value()

				# If this child element also has child elements, then recursively
				# process it.
				if len(f.children[key].children)>0:
					tr_coordinates(f.children[key])

				# Shift the offset along, depending on whether this was a vertical
				# of horizontal layout
				if f.layout=='horizontal':
					dx += f.children[key].width.value() + f.padding
				if f.layout=='vertical':
					dy += f.children[key].height.value() + f.padding

		tr_dimensions(self.base)
		self.solver.updateVariables()
		tr_coordinates(self.base)
		self.figure_width = self.base.width.value() + self.base.margin_right + self.base.margin_left
		self.figure_height = self.base.height.value() + self.base.margin_top + self.base.margin_bottom



	## ------------------------------------------------------------------------
	## Preview the figure by displaying a figure with coloured patches for
	## each plot element.
	def preview(self):
		""" Preview the figure by displaying a figure with coloured patches for
		each plot element.
		"""
		c = zool.colours.ColourBrewer()
		matplotlib.pyplot.figure()
		ax = matplotlib.pyplot.gca()
		ii = 1
		jj = 1
		for key in self.store:
			ax.add_patch(matplotlib.patches.Rectangle((self.store[key].xl, self.store[key].yb), self.store[key].width.value(), self.store[key].height.value(), facecolor=c.get_hex('paired',ii)))
			if ii==11:
				ii = 0
			else:
				ii = ii + 1
			ax.text(self.store[key].xl + self.store[key].width.value()/2.0, self.store[key].yb + self.store[key].height.value()/2.0, self.store[key].label, color='black', horizontalalignment='center', verticalalignment='center')
		matplotlib.pyplot.xlim(-1,self.figure_width+1)
		matplotlib.pyplot.ylim(-1,self.figure_height+1)
		matplotlib.pyplot.show()


	## ------------------------------------------------------------------------
	## Generate a new axis for a given plot element.
	def axes(self, label):
		""" Generate a new Matplotlib axis for this plot element.

		Args: label(str) plot element id.
		"""
		ax = matplotlib.pyplot.axes([self.store[label].xl/self.figure_width, self.store[label].yb/self.figure_height,
						self.store[label].width.value()/self.figure_width, self.store[label].height.value()/self.figure_height])
		self.store[label].ax = ax
		return(ax)

	## ------------------------------------------------------------------------
	## New figure method.
	def new(self):
		""" Make a new Matplotlib figure with the right width/height.

		:return matplotlib figure: Figure handle.
		"""
		return matplotlib.pyplot.figure(figsize=(self.figure_width/2.54,self.figure_height/2.54))


	## ------------------------------------------------------------------------
	## Reset an axis method.
	def reset_axis(self, label):
		""" Reset the Matplotlib axis for this plot element (in case it's been
		adjusted by Matplotlib).

		Args: label(str) plot element id.
		"""
		if not self.store[label].ax==None:
			self.store[label].ax.set_position([self.store[label].xl/self.figure_width, self.store[label].yb/self.figure_height,
							self.store[label].width.value()/self.figure_width, self.store[label].height.value()/self.figure_height])
		else:
			raise UserError('This panel <{}> does not have an axes to reset.'.format(label))
