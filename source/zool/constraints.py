"""Constraints and constraint serialisers/deserialisers
"""
from dataclasses import dataclass
from typing import Union

from .exceptions import DeserialisationError


@dataclass
class Fixed:
    """Constraint for a fixed width or height size.

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
        return {"constraint": "fixed", "size": self.size}


@dataclass
class FixedAspect:
    """Constraint with a fixed aspect ratio.

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
        return {"constraint": "fixedAspect", "aspect": self.aspect}


class FromChildren:
    """Constraint where the width or height comes from any child elements."""

    def to_dict(self) -> dict:
        """Convert this constraint into a dictionary

        Returns
        -------
        dict
        """
        return {"constraint": "fromChildren"}


class FromParent:
    """Constraint where a width or height comes from the parent element."""

    def to_dict(self) -> dict:
        """Convert this constraint into a dictionary

        Returns
        -------
        dict
        """
        return {"constraint": "fromParent"}


class Fill:
    """Constraint where width or height set to fill parent element."""

    def to_dict(self) -> dict:
        """Convert this constraint into a dictionary

        Returns
        -------
        dict
        """
        return {"constraint": "fill"}


@dataclass
class Named:
    """Constraint where width or height comes from another element.

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
        return {"constraint": "named", "id": self.id}


def constraint_deserialiser(
    v: dict,
) -> Union[Fixed, FixedAspect, FromChildren, FromParent, Fill, Named]:
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
        If the serialised constraint is incomplete or unknown.
    """

    if not isinstance(v, dict):
        raise TypeError("Supplied variable is not a dictionary")
    if "constraint" not in v:
        raise DeserialisationError(
            "Unknown", "Supplied dictionary does not have a <constraint> entry"
        )

    if v["constraint"] == "fixed":
        if "size" not in v:
            raise DeserialisationError(
                "Fixed", "Require a value for a fixed constraint"
            )
        return Fixed(float(v["size"]))

    elif v["constraint"] == "fixedAspect":
        if "aspect" not in v:
            raise DeserialisationError(
                "FixedAspect", "Require a value for a fixedAspect constraint"
            )
        return FixedAspect(float(v["aspect"]))

    elif v["constraint"] == "named":
        if "id" not in v:
            raise DeserialisationError(
                "Named",
                "Require a panel id for a named width/height constraint",
            )
        return Named(v["id"])

    elif v["constraint"] == "fill":
        return Fill()

    elif v["constraint"] == "fromChildren":
        return FromChildren()

    elif v["constraint"] == "fromParent":
        return FromParent()

    else:
        raise DeserialisationError(
            v["constraint"],
            "Unknown constraint type <{}>".format(v["constraint"]),
        )
