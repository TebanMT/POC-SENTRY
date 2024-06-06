"""
 File to define the handler to validate de JWT sent by the request
"""
# pylint: disable=import-error
from integrations.keycloak.keycloak import Keycloak
from utils.logger_config import setup_logger

logger = setup_logger(__name__)

def authorizer(event, context):  # pylint: disable=unused-argument
    """
        Handler to validate the session in keycloak using
        a class
    """
    logger.info("Authorizing user...")
    token = event['authorizationToken']
    arn = str(event['methodArn'])
    logger.debug("Token received: %s", token[:10] + '...' if len(token) > 10 else token)
    logger.debug("Method ARN: %s", arn)
    split_arn = arn.split("/")
    general_arn = split_arn[0]+"/"+split_arn[1]+"/*"
    logger.debug("GENERAL Method ARN: %s", general_arn)
    keycloak = Keycloak(external_token = token)
    user_id = keycloak.validate_session()
    if user_id:
        logger.info("Session validated for user ID: %s", user_id)
        policy = generate_allow_policy(general_arn, user_id)
    else:
        logger.warning("Session validation failed")
        policy = generate_deny_policy(general_arn)
    return policy


def generate_allow_policy(arn: str, user_id: str) -> dict:
    """
        Creates a policy to allow the access
    """
    logger.info("****generate_allow_policy()****")
    allow_policy = {
        'principalId': 'user',
        'policyDocument': {
            'Version': '2012-10-17',
            'Statement': [{
                'Action': 'execute-api:Invoke',
                'Effect': 'Allow',
                'Resource': arn
            }]
        },
        'context': {
            'keycloak_user_id': user_id
        }
    }

    return allow_policy

def generate_deny_policy(arn: str) -> dict:
    """
            Creates a policy to deny the access
    """
    logger.info("****generate_deny_policy()****")
    deny_policy = {
        'principalId': 'user',
        'policyDocument': {
            'Version': '2012-10-17',
            'Statement': [{
                'Action': 'execute-api:Invoke',
                'Effect': 'Deny',
                'Resource': arn
            }]
        }
    }

    return deny_policy
