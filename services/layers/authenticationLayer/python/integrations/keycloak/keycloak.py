"""
    File to declare the class to conect to a Keycloak Rest service
"""
#pylint: disable=line-too-long
#pylint: disable=too-many-arguments
import requests

from utils.utils_aws import AppConfig
from utils.logger_config import setup_logger

logger = setup_logger(__name__)

class Keycloak:
    """
    A utility class to manage and interact with Keycloak authentication.

    Attributes:
        token (str): The access token used for authorization.
        config (AppConfig): Configuration object containing necessary parameters.
        is_context (bool): A flag indicating if the class is being used as a context manager.
        refresh_token (str): Token used to refresh the session.

    Note:
        If an external_token is provided during initialization, the class will assume it's being used to
        validate the session rather than to initialize a new token.
    """

    def __init__(self, external_token: str = None):
        """
        Initializes the Keycloak instance.

        Args:
            external_token (str, optional): Token obtained externally. Defaults to None.
        """
        self.token = external_token
        self.config = AppConfig()
        self.is_context = False
        self.refresh_token = None

    def initialize_token(self, username, password, client_id='fileStorage', grant_type='password', scope='openid'):
        """
        Initializes the token by fetching it using provided credentials.

        Args:
            username (str): The user's username.
            password (str): The user's password.
            client_id (str, optional): The client ID. Defaults to 'client_id'.
            grant_type (str, optional): Grant type for OAuth2. Defaults to 'password'.
            scope (str, optional): OAuth2 scope. Defaults to 'openid'.
        """
        logger.info("****initialize_token()****")
        if self.token:
            raise ValueError("An external token is already set. You cannot initialize an internal token simultaneously.")
        self.token = self.get_token(username, password, client_id, grant_type, scope)


    def __enter__(self):
        self.is_context = True
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        _ , _ , _ = exc_type, exc_value, traceback
        if self.refresh_token:
            self.invalidate_token()
        self.token = None
        self.is_context = False

    def validate_session(self):
        """
        Validates the session using the provided token.

        Returns:
            str: User ID if session is valid, otherwise None.
        """
        logger.info("****validate_session()****")
        try:
            logger.debug("Token length = %s", len(self.token))
            url =  self.config.keycloak_url
            realm = self.config.keycloak_realm
            logger.debug("Keycloak URL = %s Realm = %s" , url, realm)
            userinfo_url = f"{url}/realms/{realm}/protocol/openid-connect/userinfo"
            headers = {'Authorization': f'Bearer {self.token}'}
            logger.debug("Sending request to %s ", userinfo_url)
            info = requests.get(userinfo_url, headers=headers, timeout=30)
            logger.debug("Received response: %s", info.text)
            response = info.json()
            if 'sub' in response:
                logger.info("Valid session with sub: %s", response['sub'])
                return response['sub']
            logger.warning("No 'sub' field in response")
            return None
        except Exception as err: #pylint: disable=broad-exception-caught
            logger.error("Exception occurred while validating token session %s", str(err), exc_info=True)
            return None

    def get_token(self, username, password, client_id = 'fileStorage', grant_type = 'password', scope='openid'):
        """
        Fetches and returns an access token.

        Args:
            username (str): The user's username.
            password (str): The user's password.
            client_id (str, optional): The client ID. Defaults to 'client_id'.
            grant_type (str, optional): Grant type for OAuth2. Defaults to 'password'.
            scope (str, optional): OAuth2 scope. Defaults to 'openid'.

        Returns:
            str: Access token.
        """
        logger.info("****get_token()****")
        url =  self.config.keycloak_url
        realm = self.config.keycloak_realm
        try:
            result = requests.post(f'{url}/realms/{realm}/protocol/openid-connect/token',
                data={
                    'username': username,
                    'password': password,
                    'grant_type': grant_type,
                    'client_id': client_id,
                    'scope': scope
                },
                timeout=30
            )

            self.refresh_token = result.json()['refresh_token']
            return result.json()['access_token']
        except requests.RequestException as err:
            logger.error("Error fetching token: %s", err)
            return ''

    def invalidate_token(self):
        """
        Invalidates the current session token.
        """
        logger.info("****invalidate_token()****")
        url =  self.config.keycloak_url
        realm = self.config.keycloak_realm
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Authorization': f'Bearer {self.token}'
        }
        data = {
            'refresh_token': self.refresh_token,
            'client_id': 'fileStorage',
            'scope': 'openid'
        }

        response = requests.post(f'{url}/realms/{realm}/protocol/openid-connect/logout', headers=headers, data=data, timeout=30)

        if response.status_code == 204:
            logger.info("Token invalidated successfully.")
        else:
            logger.error("Error invalidating token. Status Code:  %s , Response: %s",response.status_code, response.text)
