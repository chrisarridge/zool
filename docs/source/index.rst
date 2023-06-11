Zool: Hierarchical Axes Layout for Matplotlib
=============================================

Version |release|.

**Zool** is a Python library for the layout of complex plots using ``Matplotlib``.
In contrast to manually-specifying the dimensions and locations of each set of
axes, in `Zool` you can also specify that a axis fills the available space, or
takes its width/height/both from another plot element, or can inherit it from a
parent element or the width of all the child elements.  This is achieved using
constraint programming (using the `KiwiSolve` library) to compute the
size of each plot element.  Several factory routines are provided for generating
specific types of plots (at the moment a standard vertical stack plot, and a
triangle-type plot).

Why Zool?
---------
Although this functionality is partly available in ``Matplotlib`` with the ``gridspec``
module what we wanted was to be able to produce graphics for publication where the
panels were sized not only to fit column widths of journals but where the panels
would have a readable height.  **Zool** fills this need.

Contributing
------------
Contributions to Zool are welcome.

Licence
-------
This program is free software: you can redistribute it and/or modify it under
the terms of the GNU General Public License as published by the Free Software
Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.

Contents
========

.. toctree::
   :maxdepth: 2

   getting-started
   building-layouts
   save-and-load


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

