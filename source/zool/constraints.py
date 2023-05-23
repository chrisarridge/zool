"""Constraint sizing options"""
from typing import Union


class Fixed:
    """Fixes the size to a specific number"""

    def __init__(self, v: float):
        """Initialise

        Parameters
        ----------
        v : float
            Size in cm.
        """
        self._size = v

    @property
    def size(self) -> float:
        """Get the size

        Returns
        -------
        float
            Size in cm.
        """
        return self._size



class FixedAspect:
    """Fixes the aspect ratio"""

    def __init__(self, v: float):
        """Initialise

        Parameters
        ----------
        v : float
            The required aspect ratio.
        """
        self._aspect = v

    @property
    def aspect(self) -> float:
        """Get the aspect ratio.

        Returns
        -------
        float
            Aspect ratio.
        """
        return self._aspect



class FromChildren:
    """Determine sizing from child elements"""
    pass



class FromParent:
    """Determine sizing from parent element"""
    pass



class Fill:
    """Determining sizing to fill parent element"""
    pass



class Named:
    """Determine sizing from another element"""
    def __init__(self, id: str):
        """Initialise

        Parameters
        ----------
        id : str
            Id of the named element.
        """
        self._id = id

    @property
    def id(self) -> str:
        """Get the id

        Returns
        -------
        str
            Eleent id.
        """
        return self._id



def _constraint_serialiser(v: Union[Fixed,FixedAspect,FromChildren,FromParent,Fill,Named]) -> dict:
    """Helper function to turn constraints into something that can be serialised

    Parameters
    ----------
    v : Union[Fixed,FixedAspect,FromChildren,FromParent,Fill,Named]
        Constraint to serialise.

    Returns
    -------
    dict
        Returns a dictionary to be written to JSON.

    Raises
    ------
    ValueError
        If the constraint is of an unknown type.
    """

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



def _constraint_deserialiser(v: dict) -> Union[Fixed,FixedAspect,FromChildren,FromParent,Fill,Named]:
    """Helper function to turn serialised constraints back into constraints

    Parameters
    ----------
    v : dict
        Dictionary to turn into a constraint class.

    Returns
    -------
    Union[Fixed,FixedAspect,FromChildren,FromParent,Fill,Named]
        Constraint.

    Raises
    ------
    ValueError
        If the argument is not a dictionary, or doesn't contain a 'constraint'
        key, where a constraint doesn't have a required value, or where we do
        not understand the constraint.
    """
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
        raise ValueError('Unknown constraint type <{}>'.format(v['constraint']))
