"""Exceptions class definitions.
"""


class ZoolError(Exception):
    """Base class for Zool exceptions."""

    pass


class InappropriateConstraint(ZoolError):
    """Exception raised for errors in the constraints.

    Attributes
    ----------
    constraint : str
        The constraint.
    id : str
        The id that the constraint was given.
    message : str
        The message accompanying the error.
    """

    def __init__(self, constraint: str, id: str, message: str):
        """Initialise.

        Parameters
        ----------
        constraint : str
            The constraint.
        id : str
            The id that the constraint was given.
        message : str
            The message accompanying the error.
        """
        self.constraint = constraint
        self.id = id
        self.message = message


class NoSolution(ZoolError):
    """No layout solution available."""

    pass


class UnknownElement(ZoolError):
    """Exception raised for where an unknown element id is encountered.

    Attributes
    ----------
    id : str
        The id that was unknown.
    """

    def __init__(self, id: str):
        """Initialise.

        Parameters
        ----------

        id : str
            The id that was unknown.
        """
        self.id = id


class DeserialisationError(ZoolError):
    """Constraint cannot be deserialised because the dictionary isn't complete.

    Attributes
    ----------
    constraint : str
        The constraint.
    message : str
        The message accompanying the error.
    """

    def __init__(self, constraint: str, message: str):
        """Initialise.

        Parameters
        ----------
        constraint : str
            The constraint.
        message : str
            The message accompanying the error.
        """
        self.constraint = constraint
        self.message = message
