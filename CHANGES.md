# Version history

## 2.1 - Chris Arridge - 21 May 2023
* Changed install to use pyproject TOML.
* Moved colours to pending deprecated status since this functionality is in Matplotlib.

## 2.0a - Chris Arridge - 11 February 2020
* Added FixedAspect setting to allow the solver to satisfy constraints on the
aspect ratio of a given panel (e.g., for equal axes).
* Rewrote Plot class -> Figure class and incorporated the constraint
specifiers (e.g., Fixed, Fill, Named) internally, rather than converting to
strings.
* Moved all the files in layout into core.
* Added custom exceptions.
* Sorted out distinctions between figure size and base size in the Figure
specification.  Now, figwidth and figheight relate to the total height or
width of the figure, including the margins.  The base width/height is then
worked out from the figure width/height and the margins.
* Updated triangle factory function to use variable names rather than indices.
* Added subplot-style grid factory function.
* Added loading/saving from from/to JSON files.

## 1.0b - Chris Arridge - 05 December 2019
