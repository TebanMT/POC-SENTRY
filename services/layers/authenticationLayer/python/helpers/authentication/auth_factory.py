"""
This module implements a factory pattern for creating authentication strategies.
"""
# pylint: disable=line-too-long

from abc import ABC, abstractmethod
from utils.logger_config import setup_logger
from .auth_dynamo_credentials import SOAPAuthStrategy, RESTAuthStrategy, ChecksAuthStrategy
from .auth_env_variables import ESAuthStrategy, ReportingAuthStrategy, FileStorageAtuhStrategy

logger = setup_logger(__name__)

class AuthenticationFactory(ABC):
    """
    An abstract base class for authentication strategy factories.
    """

    @abstractmethod
    def create_auth_strategy(self):
        """
        Creates a new authentication strategy.

        Raises:
            NotImplementedError: This method must be overridden.
        """
        logger.info("****create_auth_strategy()****")
        raise NotImplementedError("Abstract Method")

    def get_credentials(self, user_id = None):
        """
        Retrieves the credentials for the given user ID using the created authentication strategy.

        Parameters:
            user_id (int, optional): The ID of the user for which to retrieve credentials. Defaults to 1.

        Returns:
            result (dict): User credentials.
        """
        logger.info("****AuthenticationFactory.get_credentials()****")
        auth_strategy = self.create_auth_strategy()
        return auth_strategy.get_credentials(user_id)


class SOAPAuthenticationFactory(AuthenticationFactory):
    """
    A subclass of AuthenticationFactory that implements a SOAPAuthenticationFactory.
    """
    def create_auth_strategy(self):
        """
        This function creates a SOAP authentication strategy.

        Returns:
            SOAPAuthStrategy: An instance of SOAPAuthStrategy class.
        """
        logger.info("****SOAPAuthenticationFactory.create_auth_strategy()****")
        return SOAPAuthStrategy()

class RESTAuthenticationFactory(AuthenticationFactory):
    """
    A subclass of AuthenticationFactory that implements a RESTAuthenticationFactory.
    """

    def create_auth_strategy(self):
        """
        This function creates a REST authentication strategy.

        Returns:
            RESTAuthStrategy: An instance of RESTAuthStrategy class.
        """
        logger.info("****RESTAuthenticationFactory.create_auth_strategy()****")
        return RESTAuthStrategy()

class ESAuthenticationFactory(AuthenticationFactory):
    """
    A subclass of AuthenticationFactory that implements an ESAuthenticationFactory.
    """

    def create_auth_strategy(self):
        """
        This function creates an Elasticsearch authentication strategy.

        Returns:
            ESAuthStrategy: An instance of ESAuthStrategy class.
        """
        logger.info("****ESAuthenticationFactory.create_auth_strategy()****")
        return ESAuthStrategy()

class ReportingAuthenticationFactory(AuthenticationFactory):
    """
    A subclass of AuthenticationFactory that implements a ReportingAuthenticationFactory.
    """

    def create_auth_strategy(self):
        """
        This function creates a Reporting authentication strategy.

        Returns:
            ReportingAuthStrategy: An instance of ReportingAuthStrategy class.
        """
        logger.info("****ReportingAuthenticationFactory.create_auth_strategy()****")
        return ReportingAuthStrategy()

class FileStorageAuthenticationFactory(AuthenticationFactory):
    """
    A subclass of AuthenticationFactory that implements a FileStorageAuthenticationFactory.
    """

    def create_auth_strategy(self):
        """
        This function creates a File Storage strategy.

        Returns:
            FileStorageAtuhStrategy: An instance of FileStorageAtuhStrategy class.
        """
        logger.info("****FileStorageAuthenticationFactory.create_auth_strategy()****")
        return FileStorageAtuhStrategy()

class ChecksAuthenticationFactory(AuthenticationFactory):
    """
    A subclass of AuthenticationFactory that implements a ChecksAuthenticationFactory.
    """

    def create_auth_strategy(self):
        """
        This function creates a REST authentication strategy.

        Returns:
            ChecksAuthStrategy: An instance of ChecksAuthStrategy class.
        """
        logger.info("****ChecksAuthenticationFactory.create_auth_strategy()****")
        return ChecksAuthStrategy()
