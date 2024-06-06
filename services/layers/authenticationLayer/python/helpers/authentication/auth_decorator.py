"""
This module provides a decorator for handling authentication.
"""
# pylint: disable=line-too-long
from utils.utils_format import return_formatted_response
from utils.logger_config import setup_logger

logger = setup_logger(__name__)

def auth_decorator(auth_factory):
    """
    A decorator that fetches user credentials using the provided authentication factory and 
    injects them into the wrapped function.

    Parameters:
        auth_factory (AuthenticationFactory): An instance of AuthenticationFactory to use for fetching user credentials.

    Returns:
        inner_decorator (function): A function that wraps the original function.
    """
    logger.info("****auth_decorator()****")
    def inner_decorator(lambda_function):
        """
        A function that wraps the original function, injecting user credentials.

        Parameters:
            lambda_function (function): The original function to wrap.

        Returns:
            wrapper (function): The wrapped function.
        """
        logger.info("****inner_decorator()****")
        def wrapper(event, context):
            """
            Retrieves the user's credentials and calls the original function, injecting the credentials.

            Parameters:
                event (dict): The event data.
                context (obj): The context in which the function is running.

            Returns:
                result: The result of calling the original function with the injected credentials.
            """
            logger.info("****wrapper()****")
            user_id = None
            try:
                if 'requestContext' in event:
                    user_id = event['requestContext']['authorizer']['keycloak_user_id']
                #for step functions
                elif 'auth' in event:
                    user_id = event['auth']['requestContext']['authorizer']['keycloak_user_id']
            except (KeyError, TypeError):
                user_id = None
            try:
                credentials = auth_factory.get_credentials(user_id)
            except KeyError as err:
                logger.error(err)
                code_http = 400
                response = return_formatted_response(None, code_http, {}, str(err))
                return response
            except PermissionError as err:
                logger.error(err)
                code_http = 401
                response = return_formatted_response(None, code_http, {}, str(err))
                return response
            return lambda_function(credentials, event, context)
        return wrapper
    return inner_decorator
