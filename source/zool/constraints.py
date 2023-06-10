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



@dataclass
class FixedAspect:
    """Class for storing a fixed aspect ratio constraint.

    Attributes
    ----------
    aspect : float
        Aspect ratio (width/height) for this fixed constraint.
    """
    aspect: float



class FromChildren:
    """Class to store a constraint where the width or height comes from any child elements.
    """
    pass



class FromParent:
    """Class to store a constraint where the width or height comes from the parent element.
    """
    pass



class Fill:
    """Class to store a constraint where the width or height fills any remaining space in the parent element.
    """
    pass



@dataclass
class Named:
    """Class to store a constraint where a width or height is taken from another element.
    
    Attributes
    ----------
    id : str
        Id string to point to the element.
    """
    id: str


def _constraint_serialiser(v: Union[Fixed,FixedAspect,FromChildren,FromParent,Fill,Named]) -> dict:
    """Helper function to turn constraints into something that can be serialised.

    Parameters
    ----------
    v : Union[Fixed,FixedAspect,FromChildren,FromParent,Fill,Named]
        Constraint to serialise.

    Returns
    -------
    dict
        Serialised version.

    Raises
    ------
    TypeError
        Raised if the constraint type is not recognised.
    """
    if isinstance(v, Fixed):
        return {"constraint":"fixedDimension", "value":v.size}
    elif isinstance(v, FixedAspect):
        return {"constraint":"fixedAspectRatio", "value":v.aspect}
    elif isinstance(v, FromChildren):
        return {"constraint":"fromChildren"}
    elif isinstance(v, FromParent):
        return {"constraint":"fromParent"}
    elif isinstance(v, Fill):
        return {"constraint":"fill"}
    elif isinstance(v, Named):
        return {"constraint":"named", "value":v.id}
    else:
        raise TypeError("Unknown constraint type")



def _constraint_deserialiser(v: dict) -> Union[Fixed,FixedAspect,FromChildren,FromParent,Fill,Named]:
    """Helper function to turn serialised constraints back into constraints

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

    if v["constraint"]=="fixedDimension":
        if "value" not in v:
            raise DeserialisationError("Fixed","Require a value for a fixedDimension constraint")
        return Fixed(float(v["value"]))

    elif v["constraint"]=="fixedAspectRatio":
        if "value" not in v:
            raise DeserialisationError("FixedAspect","Require a value for a fixedAspectRatio constraint")
        return FixedAspect(float(v["value"]))

    elif v["constraint"]=="named":
        if "value" not in v:
            raise DeserialisationError("Named","Require a panel id for a named width/height constraint")
        return Named(v["value"])

    elif v["constraint"]=="fill":
        return Fill()

    elif v["constraint"]=="fromChildren":
        return FromChildren()

    elif v["constraint"]=="fromParent":
        return FromParent()

    else:
        raise DeserialisationError(v["constraint"], "Unknown constraint type <{}>".format(v["constraint"]))

