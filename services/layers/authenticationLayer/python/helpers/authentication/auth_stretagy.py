"""
This module defines the abstract base class for authentication strategies.
"""
# pylint: disable=too-few-public-methods

from abc import ABC, abstractmethod

class AuthenticationStrategy(ABC):
    """
    A base class representing an abstract authentication strategy. Subclasses
    should implement the `get_credentials` method.
    """

    @abstractmethod
    def get_credentials(self, user_id):
        """
        This function retrieves the user's credentials based on their user_id.

        Parameters:
            user_id (str): The ID of the user for which to retrieve credentials.

        Raises:
            NotImplementedError: This method must be overridden.
        """
        raise NotImplementedError("Abstract Method")
