"""Exceptions for Zool"""

class ZoolError(Exception):
    """Base class for Zool exceptions."""
    pass

class InappropriateConstraint(ZoolError):
    """_summary_

    Attributes
    ----------
    constraint : str
        THe constraint provided.
    label : str
        The label that the constraint was provided to.
	message : str
    	Message.
    """

    def __init__(self, constraint: str, label: str, message: str):
        """Initialise

        Parameters
        ----------
        constraint : str
            The constraint that was given
        label : str
            The label that was provided.
        message : str
            The message.
        """
        self.constraint = constraint
        self.label = label
        self.message = message
