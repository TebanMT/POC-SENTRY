"""
This module provides authentication strategies that retrieve credentials from environment variables.
"""
# pylint: disable=line-too-long
# pylint: disable=too-few-public-methods

import os
from utils.logger_config import setup_logger
from .auth_stretagy import AuthenticationStrategy


logger = setup_logger(__name__)

class ESAuthStrategy(AuthenticationStrategy):
    """
    This strategy retrieves Elasticsearch credentials from environment variables.
    """

    def get_credentials(self, user_id = None):
        """
        Retrieves the Elasticsearch credentials from environment variables.

        Parameters:
            user_id (str, optional): The ID of the user for which to retrieve credentials. Defaults to None.

        Returns:
            result (dict): Dictionary containing 'user' and 'password' keys with the Elasticsearch credentials.
        """
        logger.info("****ESAuthStrategy.get_credentials()****")

        result = {}
        result["user"] = os.environ.get('USER_ES_CITIES',"")
        result["password"] = os.environ.get('PASSWORD_ES_CITIES',"")
        return result

class ReportingAuthStrategy(AuthenticationStrategy):
    """
    This strategy retrieves reporting service credentials from environment variables.
    """

    def get_credentials(self, user_id = None):
        """
        Retrieves the reporting service credentials from environment variables.

        Parameters:
            user_id (str, optional): The ID of the user for which to retrieve credentials. Defaults to None.

        Returns:
            result (dict): Dictionary containing 'user' and 'password' keys with the reporting service credentials.
        """
        logger.info("****ReportingAuthStrategy.get_credentials()****")
        result = {}
        result["user"] =  os.environ.get("REPORTING_SERVICES_USER", "")
        result["password"] = os.environ.get("REPORTING_SERVICES_PASSWORD", "")
        return result


class FileStorageAtuhStrategy(AuthenticationStrategy):
    """
    This strategy retrieves the token for File Storage Endpoint.
    """

    def get_credentials(self, user_id = None):
        """
        Retrieves the reporting service credentials from environment variables.

        Parameters:
            user_id (str, optional): The ID of the user for which to retrieve credentials. Defaults to None.

        Returns:
            result (dict): Dictionary containing 'user' and 'password' keys with the reporting service credentials.
        """
        logger.info("****FileStorageAtuhStrategy.get_credentials()****")
        _ = user_id
        result = {}
        result["user"]        = os.environ.get("FILE_STORAGE_USER", "")
        result["password"]    = os.environ.get("FILE_STORAGE_PASSWORD", "")
        return result
