"""Constraints and constraint serialisers/deserialisers
"""
from typing import Union
from dataclasses import dataclass

from .exceptions import DeserialisationError

@dataclass
class Fixed:
    """Class for storing a fixed width or fixed height size constraint.

    Attributes
    ----------
    size : float
        The width or height for this fixed constraint.
    """
    size: float

    def to_dict(self) -> dict:
        """Convert this constraint into a dictionary

        Returns
        -------
        dict
        """
        return {"constraint":"fixed","size":self.size}



@dataclass
class FixedAspect:
    """Class for storing a fixed aspect ratio constraint.

    Attributes
    ----------
    aspect : float
        Aspect ratio (width/height) for this fixed constraint.
    """
    aspect: float

    def to_dict(self) -> dict:
        """Convert this constraint into a dictionary

        Returns
        -------
        dict
        """
        return {"constraint":"fixedAspect","aspect":self.aspect}



class FromChildren:
    """Class to store a constraint where the width or height comes from any child elements.
    """

    def to_dict(self) -> dict:
        """Convert this constraint into a dictionary

        Returns
        -------
        dict
        """
        return {"constraint":"fromChildren"}


class FromParent:
    """Class to store a constraint where the width or height comes from the parent element.
    """

    def to_dict(self) -> dict:
        """Convert this constraint into a dictionary

        Returns
        -------
        dict
        """
        return {"constraint":"fromParent"}


class Fill:
    """Class to store a constraint where the width or height fills any remaining space in the parent element.
    """

    def to_dict(self) -> dict:
        """Convert this constraint into a dictionary

        Returns
        -------
        dict
        """
        return {"constraint":"fill"}



@dataclass
class Named:
    """Class to store a constraint where a width or height is taken from another element.
    
    Attributes
    ----------
    id : str
        Id string to point to the element.
    """
    id: str

    def to_dict(self) -> dict:
        """Convert this constraint into a dictionary

        Returns
        -------
        dict
        """
        return {"constraint":"named", "id":self.id}



def constraint_deserialiser(v: dict) -> Union[Fixed,FixedAspect,FromChildren,FromParent,Fill,Named]:
    """Factory function to turn serialised constraints back into constraints

    Parameters
    ----------
    v : dict
        Serialised constraint.

    Returns
    -------
    Union[Fixed,FixedAspect,FromChildren,FromParent,Fill,Named]
        Deserialised constraint object.

    Raises
    ------
    TypeError
        If the supplied serialised constraint isn't a dictionary.
    DeserialisationError
        If the serialised constraint is missing information or contains a constraint we don't know about.
    """

    if not isinstance(v, dict):
        raise TypeError("Supplied variable is not a dictionary")
    if "constraint" not in v:
        raise DeserialisationError("Unknown","Supplied dictionary does not have a <constraint> entry")

    if v["constraint"]=="fixed":
        if "size" not in v:
            raise DeserialisationError("Fixed","Require a value for a fixed constraint")
        return Fixed(float(v["size"]))

    elif v["constraint"]=="fixedAspect":
        if "aspect" not in v:
            raise DeserialisationError("FixedAspect","Require a value for a fixedAspect constraint")
        return FixedAspect(float(v["aspect"]))

    elif v["constraint"]=="named":
        if "id" not in v:
            raise DeserialisationError("Named","Require a panel id for a named width/height constraint")
        return Named(v["id"])

    elif v["constraint"]=="fill":
        return Fill()

    elif v["constraint"]=="fromChildren":
        return FromChildren()

    elif v["constraint"]=="fromParent":
        return FromParent()

    else:
        raise DeserialisationError(v["constraint"], "Unknown constraint type <{}>".format(v["constraint"]))

