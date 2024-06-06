"""
Utils for aws clients
"""
import json
import os
from typing import Optional  # pylint: disable=unused-import

import boto3
import botocore
from botocore.exceptions import ClientError

from utils.logger_config import setup_logger

__APP_CONFIG = None
logger = setup_logger(__name__)

# pylint: disable=too-many-instance-attributes,too-few-public-methods
class AppConfig:
    """Application configuration singletone"""

    def __init__(self):
        self.region_name = os.environ.get('AWS_REGION', '')
        self.dynamo_db_session = os.environ.get('DYNAMO_BD_SESSION', '')
        self.ssm_front_office = os.environ.get('LEGACY_FRONT_OFFICE1', '')
        self.ssm_front_office_v2 = os.environ.get('LEGACY_FRONT_OFFICE2', '')
        self.dynamo_url_atm = os.environ.get('DYNAMO_URL_ATM', '')
        self.base_api_rest_hermes1 = os.environ.get('BASE_API_REST_HERMES1', '')
        self.dynamo_db_bearer_token = os.environ.get('DYNAMO_BD_BEARER_TOKEN', '')
        self.es_cities_api_rest = os.environ.get('ES_CITIES_URI')
        self.reporting_services_user = os.environ.get('REPORTING_SERVICES_USER', '')
        self.reporting_services_password = os.environ.get('REPORTING_SERVICES_PASSWORD', '')
        self.reporting_services_wsdl = os.environ.get('REPORTING_SERVICES_WSDL', '')
        self.reporting_services_qr_url = os.environ.get('REPORTING_SERVICES_QR_URL', '')
        self.reporting_services_bucket_name = os.environ.get("REPORTING_SERVICES_BUCKET_NAME", "")
        self.keycloak_url = os.environ.get('BASE_API_REST_KEYCLOAK', '')
        self.keycloak_realm = os.environ.get('REALM_KEYCLOAK')
        self.test_auth_user = os.environ.get('TEST_AUTH_USER', '')
        self.test_auth_password = os.environ.get('TEST_AUTH_PASSWORD', '')
        self.env_name = os.environ.get('ENVIRONMENT_VAR', '')
        self.base_url_elasticsearch_search_customer = os.environ.get(
            'BASE_URL_ELASTICSEARCH_SEARCH_CUSTOMER', ''
        )
        self.erp_services_wsdl = os.environ.get('ERP_SERVICES_WSDL', '')
        self.file_storage_url  = os.environ.get("FILE_STORAGE_URL", '')
        self.base_api_maxi_checks  = os.environ.get("BASE_API_MAXI_CHECKS", '')
        self.ssm_billpayment  = os.environ.get("BILLPAYMENT_SERVICE", '')
        self.ssm_general_billpayment  = os.environ.get("GENERAL_BILLPAYMENT_SERVICE ", '')
        self.collection_payments_wsdl = os.environ.get("COLLECTION_PAYMENTS_WSDL", '')
        self.ttl_dynamo_records = os.environ.get("TTL_DYNAMO_RECORDS", '1800')

def get_configuration() -> AppConfig:
    """Returns an application configuration object"""
    logger.info("****AppConfig.get_configuration()****")
    global __APP_CONFIG  # pylint: disable=global-statement

    if __APP_CONFIG is None:
        __APP_CONFIG = AppConfig()

    return __APP_CONFIG


def get_secrets(secret_name):
    """Function to retrieve credentials from aws secrets managerr

    Raises:
        error_e (ClientError): error that boto3 client may have
    """
    logger.info("****AppConfig.get_secrets()****")
    secrets_manager = boto3.client(
        service_name='secretsmanager', region_name=get_configuration().region_name
    )
    try:
        get_secret_value_response = secrets_manager.get_secret_value(SecretId=secret_name)
    except ClientError as error_e:
        # For a list of exceptions thrown, see
        # https://docs.aws.amazon.com/secretsmanager/latest/apireference/API_GetSecretValue.html
        logger.error(error_e)
        raise error_e

    # Decrypts secret using the associated KMS key.
    secret = get_secret_value_response['SecretString']

    return secret


def get_ssm_parameter(ssm_parameter_name):
    """
    Function to obtain values from Parameter Store
    from AWS System Manager
    Args:
        ssm_parameter_name:
    Returns:
        string: value of the parameter
    """
    logger.info('****utils_aws.get_ssm_parameter()****')
    parameter_value = None
    try:
        stage_name = os.environ.get('ENVIRONMENT_VAR', '')
        parameter_name = f'/terraform/hermes2/{stage_name}/{ssm_parameter_name}'
        ssm_client = boto3.client(service_name='ssm', region_name=get_configuration().region_name)
        response = ssm_client.get_parameter(Name=parameter_name, WithDecryption=True)
        if 'Parameter' in response:
            parameter_value = response['Parameter']['Value']
    except ClientError as error:
        logger.error('Error retrieving ssm param: %s', str(error))
    return parameter_value


class DynamoDB:
    """DynamoDB class"""
    def __init__(self, table_name: str):
        self.table_name = table_name
        self.dynamodb = boto3.resource('dynamodb', region_name=get_configuration().region_name)
        self.dynamodb_client = boto3.client('dynamodb', region_name=get_configuration().region_name)
        self.table = self.dynamodb.Table(self.table_name)

    def get_items(self,
                  index_name: str,
                  attribute_name: str,
                  attribute_value: str) -> Optional[dict]:
        """Gets an item from the table, for now only by one key"""
        logger.info("****DynamoDB.get_items()****")
        if not attribute_value:
            logger.error('Error: El valor de la clave no puede ser una cadena vacía.')
            return None
        try:
            response = self.table.query(
                IndexName=index_name,
                KeyConditionExpression=f'{attribute_name} = :val1',
                ExpressionAttributeValues={':val1': attribute_value}
            )
            return response['Items']
        except Exception as error:  # pylint: disable=broad-except
            logger.error('Error getting item: %s', str(error))
            return None

    def update_item(self,
                    primary_key: dict,
                    update_expression: str,
                    expression_attribute_values: dict) -> bool:
        """Updates an item from the table"""
        try:
            response = self.table.update_item(
                Key=primary_key,
                UpdateExpression=update_expression,
                ExpressionAttributeValues=expression_attribute_values,
                ReturnValues='UPDATED_NEW'
            )
            return response
        except Exception as error:  # pylint: disable=broad-except
            logger.error('Error updating item: %s', str(error))
            return False

    def insert_item(self,
                    item: dict, table_name) -> bool:
        """Insert or update an object into a Dynamo Table without no complex
         configuration in the condtion

        Warnings: when you perform an update with this method you must send all
        the fields, because if some attribute is doesn´t sent it will be removed form
        the item
        """
        logger.info("****DynamoDB.insert_item()****")
        item = generate_body_for_insert_item(item)
        try:
            response = self.dynamodb_client.put_item(
                TableName=table_name,
                Item=item
            )
            logger.debug("PutItem succeeded: %s", response)
            logger.debug("Updated Resource:  %s", str(response))
            return True
        except ClientError as error:
            logger.error("Error trying to insert or update the item in DynamoDB: %s", str(item))
            logger.error("ERROR: %s", str(error))
            return False

    def delete_item_by_id(self, primary_key):
        """
        Function for delete items in dynamoDB
        Args:
            primary_key: {'id': '1234567890'}
        Returns:
             dict: with status of the request to dynamo
        """
        logger.info("****DynamoDB.delete_item_by_id()****")
        return self.table.delete_item(Key=primary_key)

    def get_item(self, key: dict):
        """
        Return a single item from dynamos table.

        Parameters:
            key (dict): Dictionary to indicate the filters to get the item.

        Return:
            dict: A dictionary with the items

        Exceptions:
            ValueError: if key parameter is not provide
            Exception: if a general exception occurs
        """
        if not key:
            logger.error('Error: the key must not be empty.')
            raise ValueError('Error: the key must not be empty.')
        try:
            response = self.table.get_item(
                Key=key
            )
            if 'Item' in response:
                return response['Item']
            else:
                return None
        except ClientError as client_error:
            if client_error.response['Error']['Code'] == 'ResourceNotFoundException':
                logger.info("Resource %s not found", key)
                return None
        except Exception as error:  #pylint: disable=broad-except
            logger.error('Error getting item: %s', str(error))
            raise Exception('Error getting item: '+ str(error)) from error #pylint: disable=broad-exception-raised


def generate_body_for_insert_item(item: dict, deep: int = 0):  # pylint: disable=no-else-return
    # pylint: disable=too-many-return-statements
    """
    This function will be used ir orden to format the
    object to be well inserted in Dynamo Tables.

    This fuction also could be extended for fulfill
    all the acepted types in dyanmo fiedls.

    Args:
        item: object will all the fields
        deep: due the object could have many types dynamo requires
              some type of attribute like N,S, M is necesary track the
              deep of the tree
    Returns:
        dict: well formated dict with the type of each field
    """
    deep = deep + 1

    if isinstance(item, bool):  # pylint: disable=too-many-return-statements
        return {'BOOL': item}
    if isinstance(item, int):
        return {'N': str(item)}
    if isinstance(item, str):
        return {'S': item}
    if isinstance(item, dict):
        if deep == 1:
            return {key: generate_body_for_insert_item(value, deep)
                    for key, value in item.items()}
        return {'M': {key: generate_body_for_insert_item(value, deep)
                      for key, value in item.items()}}
    if isinstance(item, list):
        return {'L': [generate_body_for_insert_item(item, deep) for item in item]}
    return {'NULL': True}


def upload_to_s3(bucket_name, file_name, file_obj, content_type):
    """Function to upload a file in the bucket provided by
    bucket_name.
    Args:
        bucket_name (str): Name of the bucket to save the file
        file_name (str): Name of the file to upload
        file_obj (bytes): Array of bytes that represents the file
        content_type (str): Content type of the file
    """
    logger.info("****utils_aws.upload_to_s3()****")
    s3 = boto3.client('s3')

    try:
        s3.put_object(Bucket=bucket_name, Key=file_name, Body=file_obj, ContentType=content_type)
        return True
    except Exception as err:  # pylint: disable=broad-except
        logger.error('Error al subir archivo a S3: %s', str(err))
        return False


def fetch_content_s3_file(bucket_name: str, file_name: str):
    """ Method to read the s3 file content

    Parameters:
    bucket_name (str): The name of bucket where file is.
    file_name (str): The name of file
    
    Returns:
        file_name, result (tuple): The name of file and its content
    """
    s3, result = boto3.client('s3'), None
    env_name = os.environ.get('ENVIRONMENT_VAR')
    bucket_name = "hermes2" + env_name + bucket_name

    try:
        response = s3.get_object(Bucket=bucket_name, Key=file_name)
        object_content = json.loads(response['Body'].read().decode('utf-8'))
        result = object_content
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == 404:
            logger.error("Object does not exist.")
        logger.error("Error: %s", e)
    return file_name, result

def create_cloudwatch_metric_external(namespace, start_timestamp, end_timestamp):
    duration_seconds = end_timestamp - start_timestamp
    cloudwatch_client = boto3.client('cloudwatch')
    cloudwatch_client.put_metric_data(
        Namespace=namespace,
        MetricData=[
            {
                'MetricName': 'ColdStart',
                'Value': 1,
                'Unit': 'Count',
                'Timestamp': start_timestamp,
                'Dimensions': [{
                    'Name': 'Environment',
                    'Value': os.environ.get('ENVIRONMENT_VAR', 'dev')
                }]
            },
            {
                'MetricName': 'Hermes1InitializationTime',
                'Value': duration_seconds,
                'Unit': 'Seconds',
                'Timestamp': end_timestamp,
                'Dimensions': [{
                    'Name': 'Service',
                    'Value': 'Hermes1'
                }]
            }
        ]
    )