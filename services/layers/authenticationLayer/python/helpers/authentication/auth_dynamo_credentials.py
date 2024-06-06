"""
This module defines authentication strategies that interact with DynamoDB.
"""
# pylint: disable=line-too-long

from datetime import datetime, timezone
from abc import abstractmethod
from dateutil import parser

from utils.utils_format import get_current_time_utc
from utils.logger_config import setup_logger
from .auth_stretagy import AuthenticationStrategy

import boto3

logger = setup_logger(__name__)

try:
    ssm = boto3.client('ssm')
    parameter = ssm.get_parameter(Name='/dynamo/users-sessions', WithDecryption=True)
    NAME_DYNAMO_USER_SESSION_TABLE = parameter['Parameter']['Value']
    dynamodb = boto3.resource('dynamodb')
    DYNAMO_TABLE_USSER_SESSION = dynamodb.Table(NAME_DYNAMO_USER_SESSION_TABLE)
except boto3.exceptions.botocore.exceptions.ClientError as error:
    logger.error(str(error))
    raise PermissionError(error) from error

class DynamoDBAuthStrategy(AuthenticationStrategy):
    """
    This strategy retrieves user credentials from a DynamoDB table.
    """

    def get_credentials(self, user_id):
        """
        Retrieve the user's credentials from a DynamoDB table based on their keycloak_user_id.

        Parameters:
            user_id (str): The ID of the user for which to retrieve credentials.
                           In this case, the user_id is the keycloak id saved in dynamo.

        Returns:
            item (dict): User credentials from DynamoDB.

        Raises:
            KeyError: When no user is found for the provided id.
        """
        logger.info("****get_credentials()****")
        logger.info("Getting credentials for user: %s", user_id)
        keycloak_user_id = str(user_id)
        response = DYNAMO_TABLE_USSER_SESSION.query(
            IndexName='keycloakIdIndex',
            KeyConditionExpression=boto3.dynamodb.conditions.Key('keycloakId').eq(keycloak_user_id)
        )
        try:
            item = response['Items'][0]
            return self.parse_credentials(item)
        except IndexError as err:
            logger.error(err)
            raise KeyError(": No user for id: "+ keycloak_user_id) from err

    @abstractmethod
    def parse_credentials(self, credentials: dict):
        """
        Parses the raw credentials retrieved from DynamoDB.

        Parameters:
            credentials (dict): The raw credentials data.

        Raises:
            NotImplementedError: This method must be overridden.
        """



class RESTAuthStrategy(DynamoDBAuthStrategy):
    """
    This strategy retrieves user credentials from a DynamoDB table and parses them for a REST interface.
    """

    def parse_credentials(self, credentials:dict):
        """
        Parses the raw credentials retrieved from DynamoDB for a REST interface.

        Parameters:
            credentials (dict): The raw credentials data.

        Returns:
            Parsed token for a REST interface.

        """
        logger.info("****RESTAuthStrategy.parse_credentials()****")
        token = credentials['gtwToken']
        token_exspire = credentials['gtwexpires']
        token_exspire_time = datetime.fromtimestamp(int(token_exspire), timezone.utc).strftime("%Y-%m-%dT%H:%M:%S")
        token_exspire_time = datetime.strptime(token_exspire_time, "%Y-%m-%dT%H:%M:%S")
        current_time = get_current_time_utc()
        if current_time > token_exspire_time:
            raise PermissionError(": Token Expired")
        return token


class SOAPAuthStrategy(DynamoDBAuthStrategy):
    """
    This strategy retrieves user credentials from a DynamoDB table and parses them for a SOAP interface.
    """

    def parse_credentials(self, credentials):
        """
        Parses the raw credentials retrieved from DynamoDB for a SOAP interface.

        Parameters:
            credentials (dict): The raw credentials data.

        Returns:
            Parsed credentials for a SOAP interface.
        """
        logger.info("****SOAPAuthStrategy.parse_credentials()****")
        last_change = credentials['soapLastChange']
        creation = credentials['DateOfCreation']
        date_last_change = parser.parse(last_change)
        date_creation = parser.parse(creation)
        # Convert to UTC
        date_last_change_current_time_zone = date_last_change.astimezone(
            datetime.now().astimezone().tzinfo
        ).strftime('%Y-%m-%dT%H:%M:%S.%f%z')
        date_creation_current_time_zone = date_creation.astimezone(
            datetime.now().astimezone().tzinfo
        ).strftime('%Y-%m-%dT%H:%M:%S.%f%z')
        if ":" not in date_last_change_current_time_zone[-5:-3]:
            date_last_change_current_time_zone = date_last_change_current_time_zone[:-2] + ":" + date_last_change_current_time_zone[-2:]
        if ":" not in date_creation_current_time_zone[-5:-3]:
            date_creation_current_time_zone = date_creation_current_time_zone[:-2] + ":" + date_creation_current_time_zone[-2:]

        return {
            'IdUser':           str(credentials['soapUserId']),
            'SessionGuid':      credentials['soapSessionGuid'],
            'Culture':          credentials['Culture'],
            'IP':               credentials['IP'],
            'DateOfCreation':   date_creation_current_time_zone,
            'LastChange':       date_last_change_current_time_zone,
        }

class ChecksAuthStrategy(DynamoDBAuthStrategy):
    """
    This strategy retrieves user credentials from a DynamoDB table and parses them for a Checks interface.
    """
    def parse_credentials(self, credentials:dict):
        """
        Parses the raw credentials retrieved from DynamoDB for a Checks interface.

        Parameters:
            credentials (dict): The raw credentials data.

        Returns:
            Parsed token for a Checks interface.

        """
        logger.info("****ChecksAuthStrategy.parse_credentials()****")

        return {
            'token'         : credentials['tokenAccessCheck'],
            'id_user'       : credentials['soapUserId'],
            'culture'       : credentials['Culture'],
            'session_guid'  : credentials['soapSessionGuid'],
            'user_name'     : credentials['username'],
            'pc_name'       : credentials['pcName'],
            'pc_identifier' : credentials['pcIdentifier'],
            'pc_serial'     : credentials['pcSerial'],
        }
