""" Core definitions.
"""
from __future__ import annotations
from typing import Union,Tuple,Dict,Iterable,TypeVar,Type
import collections
import uuid
import itertools
import json
import warnings

import matplotlib.axes
import matplotlib.figure
import matplotlib.pyplot as plt
import matplotlib.colors
import matplotlib.patches
import kiwisolver as ks

from .constraints import *
from .exceptions import *


class PlotElement:
    """This class implements a core element of a Zool plot layout.

    Attributes
    ----------
    _id : str
        Label for this plot element
    _ax : matplotlib.Axes
        Axes created to represent this plot element.
    _width : ks.Variable
        Width as represented by a KiwiSolve constraint variable.
    _height : ks.Variable
        Height as represented by a KiwiSolve constraint variable.
    _width_constraint : constraints.Fixed, constraints.FixedAspect, constraints.FromChildren, constraints.FromParent, constraints.Fill, constraints.Named
        Width constraint.
    _height_constraint : constraints.Fixed, constraints.FixedAspect, constraints.FromChildren, constraints.FromParent, constraints.Fill, constraints.Named
        Height constraint.
    _margin_left : float
        Width of the left-hand margin.
    _margin_right : float
        Width of the right-hand margin.
    _margin_top : float
        Height of the top margin.
    _margin_bottom : float
        Height of the bottom margin.
    _x_left : float
        Coordinates of the left-hand edge of the element.
    _x_right : float
        Coordinates of the right-hand edge of the element.
    _y_top : float
        Coordinates of the top edge of the element.
    _y_bottom : float
        Coordinates of the bottom edge of the element.
    _child_layout_direction : str
        In what direction are any child elements laid out?  "horizontal" or "vertical".
    _child_layout_padding : float
        The padding applied between any child elements.
    _parent : str
        String referring to the parent element id.
    _children : list(str)
        List containing id strings for the child elements.
    """

    def __init__(self, id: str=None, width: Union[float,Fixed,FixedAspect,FromChildren,FromParent,Fill,Named]=FromParent(),
                        height: Union[float,Fixed,FixedAspect,FromChildren,FromParent,Fill,Named]=FromParent(),
                        layout: str='vertical', padding: float=0.0,
                        margin_left: float=0.0, margin_right: float=0.0, margin_top: float=0.0, margin_bottom: float=0.0):
        """Initialise

        Parameters
        ----------
        id : str, optional
            Id for the element, by default None in which case a random uuid.uuid4() string will be generated.
        width : Union[float,Fixed,FixedAspect,FromChildren,FromParent,Fill,Named], optional
            Width specification for the element, if it's a float then it will be assumed to be fixed, by default FromParent().
        height : Union[float,Fixed,FixedAspect,FromChildren,FromParent,Fill,Named], optional
            Height specification for the element, if it's a float then it will be assumed to be fixed, by default FromParent().
        layout : str, optional
            How to lay out child elements: 'horizontal' or 'vertical', by default None
        padding : float, optional
            Spacing between child elements, by default 0.0
        margin_left : float, optional
            Left-hand margin for this element, by default 0.0
        margin_right : float, optional
            Right-hand margin for this element, by default 0.0
        margin_top : float, optional
            Top margin for this element, by default 0.0
        margin_bottom : float, optional
            Bottom margin for this element, by default 0.0
        """
        self._id = id if id is not None else str(uuid.uuid4())
        self._ax = None

        # Store the width and height constraints.
        if isinstance(width, (float,int)):
            self._width_constraint = Fixed(float(width))
        else:
            self._width_constraint = width

        if isinstance(height, (float,int)):
            self._height_constraint = Fixed(float(height))
        else:
            self._height_constraint = height

        # Setup the KiwiSolve constraint variables for this element.
        self._width = ks.Variable()
        self._width.setName(self._id+'-w')
        self._height = ks.Variable()
        self._height.setName(self._id+'-h')

        # Margins.
        self._margin_left = margin_left
        self._margin_right = margin_right
        self._margin_top = margin_top
        self._margin_bottom = margin_bottom

        # Coordinates of the four edges of the element.
        self._x_left = 0.0
        self._x_right = 0.0
        self._y_top = 0.0
        self._y_bottom = 0.0

        # Layout control information: How does this element lay out its child
        # elements, by row or column? What padding is there between elements?
        if not isinstance(layout, str):
            raise TypeError('Layout must be a string')
        if not (layout=='horizontal' or layout=='vertical'):
            raise ValueError('Layout must be "vertical" or "horizontal"')
        self._child_layout_direction = layout

        if not isinstance(padding,(float,int)):
            raise TypeError('Padding must be a number')
        self._child_padding = float(padding)

        # Parent and child element id strings.
        self._parent = None
        self._children = list()

    def append_child(self, id: str):
        """Append a child element id to the child list of this element.

        Parameters
        ----------
        id : str
            Id to append.

        Raises
        ------
        TypeError
            Raised if id is not a string.
        """
        if not isinstance(id, str):
            raise TypeError
        self._children.append(id)

    @property
    def id(self) -> str:
        """Get the id string.

        Returns
        -------
        str
            Id.
        """
        return self._id

    @id.setter
    def id(self, v: str):
        """Set the id string.

        Parameters
        ----------
        v : str
            New id to set.

        Raises
        ------
        TypeError
            If the new id is not a string.
        """
        if not isinstance(v, str):
            raise TypeError
        self._id = v
        self._width.setName(self._id+'-w')
        self._height.setName(self._id+'-h')

    @property
    def axes(self) -> matplotlib.axes.Axes:
        """Get the matplotlib axes for this element.

        Returns
        -------
        matplotlib.Axes
        """
        return self._ax

    @axes.setter
    def axes(self, ax: matplotlib.axes.Axes):
        """Set the matplotlib axes for this element.

        Parameters
        ----------
        ax : matplotlib.axes.Axes
            Axes object to set.

        Raises
        ------
        TypeError
            If the provided object is not a matplotlib Axes.
        """
        if not isinstance(ax, matplotlib.axes.Axes):
            raise TypeError
        self._ax = ax


    @property
    def width(self) -> ks.Variable:
        """Get the width contraint variable.

        Returns
        -------
        ks.Variable
            The width constraint.
        """
        return self._width

    @property
    def height(self) -> ks.Variable:
        """Get the height contraint variable.

        Returns
        -------
        ks.Variable
            The height constraint.
        """
        return self._height

    @property
    def width_constraint(self) -> Union[Fixed,FixedAspect,FromChildren,FromParent,Fill,Named]:
        """Return the width constraint.

        Returns
        -------
        Union[Fixed,FixedAspect,FromChildren,FromParent,Fill,Named]
            Constraint
        """
        return self._width_constraint

    @property
    def height_constraint(self) -> Union[Fixed,FixedAspect,FromChildren,FromParent,Fill,Named]:
        """Return the height constraint

        Returns
        -------
        Union[Fixed,FixedAspect,FromChildren,FromParent,Fill,Named]
            Constraint
        """
        return self._height_constraint

    @property
    def child_padding(self) -> float:
        """Return the amount of padding between each child element.

        Returns
        -------
        float
            Padding.
        """
        return self._child_padding

    @property
    def total_child_padding(self) -> float:
        """Return the total amount of padding required inside this element.

        Returns
        -------
        float
            Total padding.
        """
        return self._child_padding*(len(self._children)-1)

    @property
    def has_children(self) -> bool:
        """Check if this element has any child elements.

        Returns
        -------
        bool
            True if there are child elements, False if not.
        """
        if len(self._children)>0:
            return True
        else:
            return False

    @property
    def is_child_layout_vertical(self) -> bool:
        """Check if this element lays out its child elements vertically.

        Returns
        -------
        bool
            True if they are laid out vertically, False if not.
        """
        if self._child_layout_direction=="vertical":
            return True
        else:
            return False

    @property
    def is_child_layout_horizontal(self) -> bool:
        """Check if this element lays out its child elements horizontally.

        Returns
        -------
        bool
            True if they are laid out horizontally, False if not.
        """
        if self._child_layout_direction=="horizontal":
            return True
        else:
            return False

    @property
    def margin_left(self) -> float:
        """Get the width of the left-hand margin.

        Returns
        -------
        float
            Margin width.
        """
        return self._margin_left

    @property
    def margin_right(self) -> float:
        """Get the width of the right-hand margin.

        Returns
        -------
        float
            Margin width.
        """
        return self._margin_right

    @property
    def margin_top(self) -> float:
        """Get the height of the top margin.

        Returns
        -------
        float
            Margin height.
        """
        return self._margin_top

    @property
    def margin_bottom(self) -> float:
        """Get the height of the bottom margin.

        Returns
        -------
        float
            Margin height.
        """
        return self._margin_bottom

    @property
    def x_left(self) -> float:
        """Get the left-hand X coordinate for this element.

        Returns
        -------
        float
            Coordinate
        """
        return self._x_left

    @x_left.setter
    def x_left(self, v: Union[float,int]):
        """Set the left-hand X coordinate.

        Parameters
        ----------
        v : Union[float,int]
            X coordinate.

        Raises
        ------
        TypeError
            If the provided value is not a float or int.
        """
        if isinstance(v, (float,int)):
            self._x_left = float(v)
        else:
            raise TypeError

    @property
    def x_right(self) -> float:
        """Get the right-hand X coordinate for this element.

        Returns
        -------
        float
            Coordinate
        """
        return self._x_right

    @x_right.setter
    def x_right(self, v: Union[float,int]):
        """Set the right-hand X coordinate.

        Parameters
        ----------
        v : Union[float,int]
            X coordinate.

        Raises
        ------
        TypeError
            If the provided value is not a float or int.
        """
        if isinstance(v, (float,int)):
            self._x_right = float(v)
        else:
            raise TypeError

    @property
    def y_top(self) -> float:
        """Get the top Y coordinate for this element.

        Returns
        -------
        float
            Coordinate
        """
        return self._y_top

    @y_top.setter
    def y_top(self, v: Union[float,int]):
        """Set the top Y coordinate.

        Parameters
        ----------
        v : Union[float,int]
            Y coordinate.

        Raises
        ------
        TypeError
            If the provided value is not a float or int.
        """
        if isinstance(v, (float,int)):
            self._y_top = float(v)
        else:
            raise TypeError

    @property
    def y_bottom(self) -> float:
        """Get the bottom Y coordinate for this element.

        Returns
        -------
        float
            Coordinate
        """
        return self._y_bottom

    @y_bottom.setter
    def y_bottom(self, v: Union[float,int]):
        """Set the bottom Y coordinate.

        Parameters
        ----------
        v : Union[float,int]
            Y coordinate.

        Raises
        ------
        TypeError
            If the provided value is not a float or int.
        """
        if isinstance(v, (float,int)):
            self._y_bottom = float(v)
        else:
            raise TypeError

    @property
    def num_children(self) -> int:
        """Return the number of child elements.

        Returns
        -------
        int
            Number of child elements.
        """
        return len(self._children)

    @property
    def child_iterator(self) -> Iterable[str]:
        """Return an iterator over all the child PlotElements.

        Returns
        -------
        Iterable[str]
        """
        return self._children.__iter__

    def to_dict(self) -> dict:
        """Serialise this plot element to a dictionary.

        Returns
        -------
        dict
        """
        d = {'widthConstraint': self._width_constraint.to_dict(),
            'heightConstraint': self._height_constraint.to_dict(),
            'marginLeft': self._margin_left,
            'marginRight': self._margin_right,
            'marginTop': self._margin_top,
            'marginBottom': self._margin_bottom,
            'childLayoutDirection': self._child_layout_direction, 'childPadding': self._child_padding,
            'label': self._id, 'parentId':'' if self._parent is None else self._parent,
            'childLabels': self._children}
        return d



_T = TypeVar("_T")


class Layout:
    """Layout class


    The general synax to add a PlotElement is ``layout[parent_id, new_id] = ...``
    but this can be contracted to ``layout[new_id] = ...`` when
    adding to the base of the plot.  If new_id is `None` then
    the code will take an auto-generated id from the element, otherwise
    it will set the element id to new_id and add it.  If the element to add is a
    dictionary then all the elements will be added as children of the selected parent.
    Any given new node id will be ignored.

    Examples
    --------
    >>> layout['base','Jane'] = zool.PlotElement()  # add the element id=Jane to the base.

    >>> layout[None] = zool.PlotElement()  # add the element to the base with an autogenerated id

    >>> layout['Jane'] = zool.PlotElement()  # add the element id=Jane to the base.

    >>> layout['Jane'] = zool.PlotElement()  # add the element id=Jane to the base.
    >>> layout['Jane','Mosi'] = zool.PlotElement()     # add the element id=Mosi to id=Jane        

    >>> layout['Jane',None] = zool.PlotElement()     # add the element to id=Jane with an autogenerated id

    Attributes
    ----------
    _elements : dict
        Contains all the elements in this plot indexed by their id labels.
    """
    def __init__(self, figwidth: Union[float,Fixed,FixedAspect,FromChildren]=FromChildren(),
                        figheight: Union[float,Fixed,FixedAspect,FromChildren]=FromChildren(),
                        layout: str="vertical", padding: float=0.0,
                        margin_left: float=0.0, margin_right: float=0.0, margin_top: float=0.0, margin_bottom: float=0.0):
        """Initialise

        The width and height will be inclusive of any margins.

        Parameters
        ----------
        figwidth : Union[float,Fixed,FixedAspect,FromChildren], optional
            Width of the figure, by default calculate from child elements.
        figheight : Union[float,Fixed,FixedAspect,FromChildren], optional
            Height of the figure, by default calculate from child elements.
        layout : str, optional
            How to lay out child elements: 'horizontal' or 'vertical', by default 'vertical'.
        padding : float, optional
            Spacing between child elements, by default 0.0
        margin_left : float, optional
            Left-hand margin for the figure, by default 0.0
        margin_right : float, optional
            Right-hand margin for the figure, by default 0.0
        margin_top : float, optional
            Top margin for the figure, by default 0.0
        margin_bottom : float, optional
            Bottom margin for the figure, by default 0.0
        """
        # Setup elements mappable to store all the PlotElements.
        self._elements = dict()

        # The solver we will use to figure out the layout.
        self._solver = ks.Solver()
        self._solved = False

        # Setup base element.
        base = PlotElement(id='base', width=figwidth, height=figheight,
                            margin_left=margin_left, margin_right=margin_right, margin_top=margin_top, margin_bottom=margin_bottom,
                            padding=padding, layout=layout)
        self._elements = {'base':base}


    def layout(self):
        """Layout the plot.
        """
        self._setup_constraints()
        self._solver.updateVariables()
        self._compute_coordinates()
        self._solved = True

    def _setup_constraints(self):
        """Resets the solver and sets up all the constraints needed to layout the plot.

        This routine calls _setup_child_constraints to process all the child elements.  I think
        this could be optimised.
        """
        self._solver.reset()
        self._solved = False

        # Setup the base element.
        if isinstance(self["base"].width_constraint, Fixed):
            self._solver.addConstraint((self["base"].width == self["base"].width_constraint.size) | "required")
        elif isinstance(self["base"].width_constraint, FromChildren):
            pass
        elif isinstance(self["base"].width_constraint, FixedAspect):
            self._solver.addConstraint((self["base"].width == self["base"].height*self["base"].width_constraint.aspect) | "required")
        elif isinstance(self["base"].width_constraint, (FromParent,Named,Fill)):
            raise InappropriateConstraint(type(self["base"].width_constraint), "base", "Base element cannot be constrained by parent (there isn't one), another element, or fill (there's nothing to fill)")
        else:
            raise InappropriateConstraint(type(self["base"].width_constraint), "base", "Unknown constraint")

        if isinstance(self["base"].height_constraint, Fixed):
            self._solver.addConstraint((self["base"].height == self["base"].height_constraint.size) | "required")
        elif isinstance(self["base"].height_constraint, FromChildren):
            pass
        elif isinstance(self["base"].height_constraint, FixedAspect):
            self._solver.addConstraint((self["base"].height == self["base"].width/self["base"].height_constraint.aspect) | "required")
        elif isinstance(self["base"].height_constraint, (FromParent,Named,Fill)):
            raise InappropriateConstraint(type(self["base"].height_constraint), "base", "Base element cannot be constrained by parent (there isn't one), another element, or fill (there's nothing to fill)")
        else:
            raise InappropriateConstraint(type(self["base"].height_constraint), "base", "Unknown constraint")

        # Now recursively process all the child constraints.
        self._setup_child_constraints("base")


    def _setup_child_constraints(self, id: str):
        """Sets up all the constraints for a set of child elements needed to layout the plot.

        Parameters
        ----------
        id : str
            Id to process all the child elements for.

        Raises
        ------
        UnknownElement
            If the id is not known.
        """

        if id not in self._elements:
            raise UnknownElement(id)

        # If we are laying out vertically then we sum up the height
        # of all the child elements, if horizontally then we sum
        # the width of all our child elements, plus any padding.
        if self[id].is_child_layout_vertical:
            wsum = self[id].margin_left + self[id].margin_right
            hsum = self[id].total_child_padding + self[id].margin_top + self[id].margin_bottom
        elif self[id].is_child_layout_horizontal:
            wsum = self[id].total_child_padding + self[id].margin_left + self[id].margin_right
            hsum = self[id].margin_top + self[id].margin_bottom
        else:
            raise RuntimeError("Cannot establish the layout direction")
        hfill = []
        wfill = []

        # Now process the constraints of each of the child items.
        for child_id in self[id].child_iterator():

            # Set the constraints for all the child elements.
            if isinstance(self[child_id].width_constraint, Fixed):
                self._solver.addConstraint((self[child_id].width == self[child_id].width_constraint.size) | "required")
            elif isinstance(self._elements["base"].width_constraint, FixedAspect):
                self._solver.addConstraint((self[child_id].width == self[child_id].height*self[child_id].width_constraint.aspect) | "required")
            elif isinstance(self[child_id].width_constraint, FromParent):
                self._solver.addConstraint((self[child_id].width == self[id].width - self[id].margin_left - self[id].margin_right) | "required")
            else:
                pass

            if isinstance(self[child_id].height_constraint, Fixed):
                self._solver.addConstraint((self[child_id].height == self[child_id].height_constraint.size) | "required")
            elif isinstance(self[child_id].height_constraint, FixedAspect):
                self._solver.addConstraint((self[child_id].height == self[child_id].width/self[child_id].height_constraint.aspect) | "required")
            elif isinstance(self[child_id].height_constraint, FromParent):
                self._solver.addConstraint((self[child_id].height == self[id].height - self[id].margin_top - self[id].margin_bottom) | "required")
            else:
                pass

            # Add a constraint where an element gets its width or height from another specific node.
            if isinstance(self[child_id].width_constraint, Named):
                self._solver.addConstraint((self[child_id].width==self[self[child_id].width_constraint.id].width) | 'required')
            if isinstance(self[child_id].height_constraint, Named):
                self._solver.addConstraint((self[child_id].height==self[self[child_id].height_constraint.id].height) | 'required')

            # Form a constraint for the sum of all the child widths and all the elements that are part of the fill.
            if isinstance(self[child_id].width_constraint, (Fixed,FixedAspect,FromChildren,Named)):
                wsum += self[child_id].width
            elif isinstance(self[child_id].width_constraint, Fill):
                wfill.append(child_id)
            else:
                pass

            # Form a constraint for the sum of all the child heights and all the elements that are part of the fill.
            if isinstance(self[child_id].height_constraint, (Fixed,FixedAspect,FromChildren,Named)):
                hsum += self[child_id].height
            elif isinstance(self[child_id].height_constraint, Fill):
                hfill.append(child_id)
            else:
                pass

        # Add constraints if this node gets it's width/height from its child nodes.
        if isinstance(self[id].height_constraint, FromChildren):
            if self[id].is_child_layout_vertical:
                self._solver.addConstraint((self[id].height==hsum) | "required")

        if isinstance(self[id].width_constraint, FromChildren):
            if self[id].is_child_layout_horizontal:
                self._solver.addConstraint((self[id].width==wsum) | "required")

        # Add constraints where child nodes fill to consume all the remaining space.
        if len(hfill)>0:
            child_heights = (self[id].height-hsum)/float(len(hfill))
            for key in hfill:
                self._solver.addConstraint((self[key].height == child_heights) | 'required')
        if len(wfill)>0:
            child_widths = (self[id].width-wsum)/float(len(wfill))
            for key in wfill:
                self._solver.addConstraint((self[key].width == child_widths) | 'required')

        # recursively process child nodes
        for child_id in self[id].child_iterator():
            self._setup_child_constraints(child_id)


    def _compute_coordinates(self):
        """Compute coordinates for all the elements.
        """
        self["base"].x_left = 0.0
        self["base"].y_top = self["base"].height.value()
        self["base"].x_right = self["base"].width.value()
        self["base"].y_bottom = 0.0
        self._compute_child_coordinates("base")


    def _compute_child_coordinates(self, id: str):
        """Compute coordinates for all the child elements of a given id.

        Parameters
        ----------
        id : str
            Id to process all the child elements for.

        Raises
        ------
        UnknownElement
            If the id is not known.
        """
        
        if id not in self._elements:
            raise UnknownElement(id)

        # These are offsets (from the parent coordinates) for this level of
        # the tree. If we are stepping across multiple sibling elements at the
        # same level, then these will increment so that we have the offset from
        # the beginning of each element
        x_origin = self[id].x_left + self[id].margin_left
        y_origin = self[id].y_top - self[id].margin_top

        # Process all the child nodes, recursively processing as necessary.
        for child_id in self[id].child_iterator():

            # Set the coordinates.
            self[child_id].x_left = x_origin
            self[child_id].y_top = y_origin
            self[child_id].x_right = x_origin + self[child_id].width.value()
            self[child_id].y_bottom = y_origin - self[child_id].height.value()

            # If this child element also has child elements, then recursively
            # process it.
            if self[child_id].has_children:
                self._compute_child_coordinates(child_id)

            # Shift the offset along, depending on whether this was a vertical
            # of horizontal layout
            if self[id].is_child_layout_horizontal:
                x_origin += self[child_id].width.value() + self[id].child_padding
            if self[id].is_child_layout_vertical:
                y_origin -= self[child_id].height.value() + self[id].child_padding


    def preview(self, show: bool=True) -> Tuple[matplotlib.figure.Figure, matplotlib.axes.Axes]:
        """Preview the layout by drawing it in a Matplotlib figure.

        The base and any elements with children are only drawn in outline.  Elements
        with no child elements are filled using the user's default colour map.

        Parameters
        ----------
        show : bool, optional
            Whether to show the figure or not using plt.show, default is True.

        Returns
        -------
        Tuple[matplotlib.figure.Figure, matplotlib.axes.Axes]
            The created figure and axes handles.
        """
        fig = matplotlib.pyplot.figure()
        ax = matplotlib.pyplot.gca()

        # Used to cycle over the user's default colour map.
        colour_cycle = itertools.cycle(plt.rcParams['axes.prop_cycle'])

        # Draw a rectangle for each element - elements with child elements are
        # only drawn in outline.
        for id in self._elements:
            if id=="base" or self[id].has_children:
                ax.add_patch(matplotlib.patches.Rectangle((self[id]._x_left, self[id]._y_bottom),
                                                      self[id].width.value(), self[id].height.value(),
                                                      fc="none", ec="black", linewidth=2))
            else:
                ax.add_patch(matplotlib.patches.Rectangle((self[id]._x_left, self[id]._y_bottom),
                                                        self[id].width.value(), self[id].height.value(),
                                                        fc=colour_cycle.__next__()["color"], ec="none"))
                ax.text(self[id]._x_left + self[id].width.value()*0.5, self[id]._y_bottom + self[id].height.value()*0.5,
                        id, color="black", horizontalalignment="center", verticalalignment="center")

        ax.set_xlim(-1, self["base"].width.value()+1)
        ax.set_ylim(-1, self["base"].height.value()+1)
        ax.set_aspect("equal")
        if show:
            plt.show()


    def display(self):
        """Print a tree display of the plot layout.
        """
        print('base')
        self._recurse_display(0, 'base')


    def _recurse_display(self, indent_depth : int, element_id : str):
        """Recursively display the contents of this layout.

        Parameters
        ----------
        indent_depth : int
            The depth we are at.
        element_id : _type_
            The element id that is the base of this part of the tree we are
            recursing through.
        """
        # Format the text - could be simplified easily but needs some additional
        # logic to fix the formatting.
        indent = "│   "*indent_depth

        # Loop over all the elements, if there are child elements
        # in this node then we recurse over them.
        for i,k in enumerate(self[element_id].child_iterator):
            if i==self[element_id].num_children-1:
                print(indent+"└── "+k)
            else:
                print(indent+"├── "+k)
            if self[k].has_children:
                self._recurse_display(indent_depth+1, k)


    def __getitem__(self, v: str) -> PlotElement:
        """Get a plot element by id

        Parameters
        ----------
        v : str
            The plot element to get.

        Returns
        -------
        PlotElement
        """
        return self._elements[v]


    def __setitem__(self, ids : Union[Tuple[str,str],Tuple[str,None],str,None],
                                element : Union[PlotElement,collections.OrderedDict]):
        """Add a PlotElement to the tree.

        Parameters
        ----------
        ids : Union[Tuple[str,str],Tuple[str,None],str,None]
            Combination of parent id and new id for inserted PlotElements.
        element : Union[PlotElement,collections.OrderedDict]
            PlotElement or an OrderedDict of PlotElement objects.

        Raises
        ------
        TypeError
            If the provided element was not a PlotElement object or OrderedDict of PlotElement objects.
        TypeError
            Raised if a provided parent id is not a string, and if a provided new id is not a string or None.
        ValueError
            Raised if a provided tuple has more than two ids in it (parent and new).
        """

        # If ids is None then our default behaviour is to insert the element(s) as a child
        # of the base node with the id in the element(s).
        if ids is None:

            if isinstance(element,PlotElement):
                # Insert a single PlotElement
                # print("Inserting single PlotElement into the base with its current ID")
                self._elements[element.id] = element
                self['base'].append_child(element.id)
                self._solved = False

            elif isinstance(element,collections.OrderedDict):
                # Insert all the PlotElement objects from an ordered dictionary
                # print("Inserting all PlotElements from OrderedDict into the base with their current IDs")
                for k,v in element.items():
                    self._elements[k] = v
                    self["base"].append_child(k)
                    self._solved = False

            else:
                raise TypeError('Expected either an OrderedDict of PlotElement objects or a PlotElement')

        # ids is not None so the user has selected either a parent id, or a parent id
        # and a new id for the inserted PlotElement.  Note that if we have an OrderedDict
        # of PlotElements then we will ignore the new id.
        else:

            # Check for layout[parent_id, new_id] form.
            if isinstance(ids,tuple):
                if len(ids)>2:
                    raise ValueError('Expected two items (parent id and new id) but received {} items'.format(len(ids)))

                # If we are here then ids should be either (str,str) or (str,None). Check for this.
                if not isinstance(ids[0],str):
                    raise TypeError('Parent id is not a string (received {})'.format(type(ids[0])))
                if ids[1] is not None:
                    if not isinstance(ids[1],str):
                        raise TypeError('New id must either be None or a string (received {})'.format(type(ids[1])))

                # If we are here then we have a parentid string and a potential new id so we
                # can go ahead and add the element(s).  NOTE: WE MIGHT WANT TO DO
                # A CHECK HERE TO SEE IF parentid IS A MEMBER OF self._elements (TODO).

                if ids[1] is None:
                    # Put the object or objects as a child of the parentid with their existing ids.
                    if isinstance(element,PlotElement):
                        # print("Inserting single PlotElement into the given node with its current ID")
                        self._elements[element.id] = element
                        self["base"].append_child(element.id)
                        self._solved = False

                    elif isinstance(element,collections.OrderedDict):
                        # print("Inserting all PlotElements from OrderedDict into the given node with their current IDs")
                        for k,v in element.items():
                            self._elements[k] = v
                            self["base"].append_child(k)
                        self._solved = False

                    else:
                        raise TypeError('Expected either an OrderedDict of elements or an element')

                else:
                    # Put the object as a child of parentid but set the id of the inserted element first.
                    # print("Inserting single PlotElement into the given node with the new ID")
                    element.id = ids[1]
                    self._elements[element.id] = element
                    self[ids[0]].append_child(element.id)
                    self._solved = False

            elif isinstance(ids,str):
                if isinstance(element,PlotElement):
                    # print("Inserting single PlotElement into the base node with a new ID")
                    element.id = ids
                    self._elements[element.id] = element
                    self["base"].append_child(element.id)
                    self._solved = False

                elif isinstance(element,collections.OrderedDict):
                    # print("Inserting all PlotElements from OrderedDict into the base node with their current IDs")
                    warnings.warn("Ignoring new id when inserting multiple PlotElement objects", UserWarning)
                    for k,v in element.items():
                        self._elements[k] = v
                        self["base"].append_child(k)
                    self._solved = False

            else:
                raise TypeError("Expected either tuple or str but received {}".format(type(ids)))


    def figure(self) -> matplotlib.figure.Figure:
        """Generate and return a Matplotlib Figure object sized correctly for our figure.

        Returns
        -------
        matplotlib.figure.Figure
            Figure object.

        Raises
        ------
        NoSolution
            If the layout has not yet been solved.
        """

        if not self._solved:
            raise NoSolution("Cannot create a figure since the layout has not been solved and so the width and height are unknown")
        return matplotlib.pyplot.figure(figsize=(self["base"].width.value()/2.54,self["base"].height.value()/2.54))


    def axes(self, id: str) -> matplotlib.axes.Axes:
        """Generate an return a Matplotlib Axes object sized correctly for this element.

        Parameters
        ----------
        id : str
            The element that the user needs an axis for.

        Raises
        ------
        UnknownElement
            If the element id is not known.
        
        NoSolution
            If the layout has not yet been solved.
        """

        if id not in self._elements:
            raise UnknownElement(id)

        if not self._solved:
            raise NoSolution("Cannot create the axes since the layout has not been solved and so the width, height and position are unknown")

        if self[id].axes is None:
            self[id].axes = matplotlib.pyplot.axes([self[id].x_left/self["base"].width.value(),
                                                self[id].y_bottom/self["base"].height.value(),
                                                self[id].width.value()/self["base"].width.value(),
                                                self[id].height.value()/self["base"].height.value()])

        return self[id].axes


    def reset_axis(self, id: str):
        """Reset the axes for PlotElement - for example if Matplotlib has changed its dimensions.

        Parameters
        ----------
        id : str
            Id of the axes to correct.

        Raises
        ------
        UnknownElement
            If the element id is not known.
        
        NoSolution
            If the layout has not yet been solved.
        
        UserError
            If the axes has not been created.

        """
        if id not in self._elements:
            raise UnknownElement(id)

        if not self._solved:
            raise NoSolution("Cannot create the axes since the layout has not been solved and so the width, height and position are unknown")

        if self[id].axes is None:
            warnings.warn("This PlotElement doesn't have an axis to reset - creating the axis")
            self.axes(id)
        else:
            self[id].axes.set_position([self[id].x_left.value()/self["base"].width.value(),
                                                self[id].y_bottom.value()/self["base"].height.value(),
                                                self[id].width.value()/self["base"].width.value(),
                                                self[id].height.value()/self["base"].height.value()])


    def to_dict(self) -> dict:
        """Convert this Layout, and all the PlotElements and their constraints to a dictionary

        Returns
        -------
        dict
        """
        d = {"zool":{"version":"ver",
                     "solved":self._solved,
                     "plotElements":{k: v.to_dict() for k,v in self._elements.items()}}}

        return d

    def to_json(self, **kwargs) -> str:
        """Serialise this Layout to a JSON string.

        Parameters
        ----------
        Any keyword arguments are passed onto the JSON serialiser.

        Returns
        -------
        str
            String of JSON.
        """
        d = self.to_dict()
        return json.dumps(d, **kwargs)

    def save(self, filename: str, **kwargs):
        """Serialise this Layout to a JSON file.

        Parameters
        ----------
        filename : str
            Filename to write to, if the filename doesn't end in .json then this will be appended.
        Any keyword arguments are passed onto the JSON serialiser.
        """

        d = self.to_dict()
        with open(filename if filename[-5:]==".json" else filename+".json", 'w') as fh:
            json.dump(d, fh, **kwargs)
        d = {"zool":{"version":"ver",
                     "solved":self._solved,
                     "plotElements":{k: v.to_dict() for k,v in self._elements.items()}}}

    @classmethod
    def from_json(cls: Type[_T], json_string: str) -> _T:
        """Deserialise JSON string to create a new Layout and set of PlotElement objects.

        Parameters
        ----------
        cls : Type[_T]
            Layout object.
        json_string : str
            String of JSON to deserialise.

        Returns
        -------
        _T
            Layout object.
        """

        def recursively_parse(layout: Type[_T], elements: dict, parentId: str):
            """Recursively add all the child elements of a given id.

            Parameters
            ----------
            layout : Type[_T]
                Layout object.
            elements : dict
                Dictionary of serialised PlotElements.
            parentId : _type_
                Parent id of the child elements to add.
            """
            for childId in elements[parentId]["childLabels"]:
                layout[parentId,childId] = PlotElement(
                        width=constraint_deserialiser(elements[childId]["widthConstraint"]),
                        height=constraint_deserialiser(elements[childId]["heightConstraint"]),
                    margin_left=elements[childId]["marginLeft"],
                    margin_right=elements[childId]["marginRight"],
                    margin_top=elements[childId]["marginTop"],
                    margin_bottom=elements[childId]["marginBottom"],
                    layout=elements[childId]["childLayoutDirection"],
                    padding=elements[childId]["childPadding"])

            for childId in elements[parentId]["childLabels"]:
                if len(elements[childId]["childLabels"])>0:
                    recursively_parse(layout, elements, childId)

        # Parse the JSON into a dictionary.
        d = json.loads(json_string)

        # Make sure this is a Zool dictionary.
        if "zool" not in d:
            raise DeserialisationError("Not a zool JSON (missing <zool> key)")
        if "plotElements" not in d["zool"]:
            raise DeserialisationError("No PlotElements in JSON")
        if not isinstance(d["zool"]["plotElements"], dict):
            raise DeserialisationError("Container of PlotElements is not a dictionary")

        # Find the base and construct the layout object.
        # NOTE: there is no type checking on the margins, padding, layout.
        elements = d["zool"]["plotElements"]
        layout = cls(figwidth=constraint_deserialiser(elements["base"]["widthConstraint"]),
                    figheight=constraint_deserialiser(elements["base"]["heightConstraint"]),
                    margin_left=elements["base"]["marginLeft"],
                    margin_right=elements["base"]["marginRight"],
                    margin_top=elements["base"]["marginTop"],
                    margin_bottom=elements["base"]["marginBottom"],
                    layout=elements["base"]["childLayoutDirection"],
                    padding=elements["base"]["childPadding"])

        # Recursively add all the child elements, solve the layout and return.
        recursively_parse(layout, elements, "base")
        layout.layout()
        return layout

    @classmethod
    def load(cls: Type[_T], filename: str) -> _T:
        """Load JSON from a file and then deserialise to create a new Layout object.

        Parameters
        ----------
        cls : Type[_T]
            Layout object.
        filename : str
            Filename of JSON to load.

        Returns
        -------
        _T
            Layout object.
        """
        with open(filename, "r") as fh:
            d = json.load(fh)

        return cls.from_json(d)
