from helpers.authentication.auth_factory import SOAPAuthenticationFactory, ChecksAuthenticationFactory
from helpers.authentication.auth_decorator import auth_decorator

from utils import utils_format
from utils.logger_config import setup_logger
from integrations.legacy.front_office_service.legacy_client import LegacyFactory, soap_serializer

logger = setup_logger(__name__)


class LegacySettings:
    """Class with methods to get payeer information."""

    def __init__(self, credentials = None, client_version = "1") -> None:
        """"""
        self.legacy_client = LegacyFactory.create_client(
            auth            = credentials,
            client_version  = client_version
        )
        self.user_session  = self.legacy_client.auth
        self.client        = self.legacy_client.client

    def get_global_attributes(self):
        """
        Invokes the GetGlobalAttribute service of Hermes 1. This method is used to retrieve
        global arttributes of the hermes 1.
        Parameters:
            body (dict) : Parameters for the compliance KYC rules. For details on the expected
                    format and keys, refer to the 'complience-kyc-rules' endpoint in Stoplight.
        Returns:
            list: A list of dictionaries representing relationships for customer compliance. If
                an unexpected response is received from the Hermes 1 service, this function
                logs the error and returns None.
        """
        logger.info("****Settings.get_global_attributes()****")
        global_attributes = soap_serializer(
            self.client.service.GetGlobalAttribute(self.user_session)
        )

        if isinstance(global_attributes, list):
            return global_attributes

        logger.error(global_attributes)
        return None


@auth_decorator(SOAPAuthenticationFactory())
def test(credentials, event, context):
    """
    Lambda function to retrieve global attributes using SOAP credentials and return a formatted response.
    The function supports two sources for the event input: step functions and API Gateway.

    Args:
    - event (dict): The input event, either from step functions or API Gateway.
    - context (obj): The context in which the function is running. Currently not used.

    Returns:
    - dict: A formatted response containing HTTP status, result, and a message.
    """

    _, _ = context, event
    message, code_http, result = '', 0, None
    logger.info("Request to get global attributes")
    try:
        setting = LegacySettings(credentials=credentials)
        result = setting.get_global_attributes()
        code_http = 200
    except KeyError as missing_key:
        logger.error("Missing key in request parameters: %s", missing_key)
        code_http = 400
    except Exception as internal_error: #pylint: disable=broad-except
        logger.error("Error to get the url. ERROR: %s", internal_error)
        code_http = 500
    response = utils_format.return_formatted_response(None, code_http, result, message, use_camel_case=True)
    return response