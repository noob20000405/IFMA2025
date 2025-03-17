"""
@author: babacardiallo
"""
import abc
from dataclasses import dataclass


# Base abstract class representing a generic financial deal
class Deal(abc.ABC):
    """
    Abstract base class for financial instruments.
    Provides a common interface for all derived Deal types.
    """

    def get_class_name(self):
        """
        Returns the name of the class of the current instance.
        This can be useful for logging or debugging purposes.
        """
        return self.__class__.__name__


@dataclass
class Call(Deal):
    """
    Represents a Call option, which gives the holder the right,
    but not the obligation, to buy an underlying asset at a specified
    price within a specified time period.
    """
    # TODO: Implement attributes and methods specific to a Call option
    pass


@dataclass
class Put(Deal):
    """
    Represents a Put option, which gives the holder the right,
    but not the obligation, to sell an underlying asset at a specified
    price within a specified time period.
    """
    # TODO: Implement attributes and methods specific to a Put option
    pass


@dataclass
class Future(Deal):
    """
    Represents a Futures contract, which obligates the buyer to
    purchase, or the seller to sell, an underlying asset at a
    predetermined price and date in the future.
    """
    # TODO: Implement attributes and methods specific to a Futures contract
    pass


    