"""This File includes commons functions that can call in any place of the hermes2-bff project
"""
# pylint: disable=missing-function-docstring
# pylint: disable=undefined-variable
# pylint: disable=no-else-return
# pylint: disable=invalid-name
# pylint: disable=too-many-branches

import base64
import calendar
from dateutil import tz
import datetime
import decimal
import json
import os
import re
from typing import Any, Optional

from .logger_config import setup_logger

logger = setup_logger(__name__)

RESPONSE_CODES = {
    200: 'sucessfull',
    201: 'sucessfull creation',
    202: 'sucessfull accepted',
    422: 'unprocessable entity',
    404: 'NOT FOUND',
    400: 'Bad Request',
    401: 'Unauthorized',
    500: 'Internal Server Error'
}

def return_formatted_response(
    headers: Optional[dict],
    status: int,
    data: Any,
    message_given: str = '',
    use_camel_case: bool = False,
):
    """
    _summary_
    Args:
        headers (dict): You must provide the headers for the reponse,
        if none is provided it will set to default {'Content-Type': 'application/json'}
        status (int): HTTP Response status code
        data (Any): You must provide all the data to be sent through the body of the response
        message_given (str): Additional message that is added to the message of the http method
        use_camel_case (bool): Indicates if the response should be in camel case.

    Returns:
        dict: Formatted Response
    """
    logger.info("****return_formatted_response()****")
    acces_control_allow_origin = os.environ.get('ACCESS_CONTROL_ALLOW_ORIGIN', '*')
    message = RESPONSE_CODES.get(status, 'Internal Server Error')
    message = message + ' ' + message_given
    headers = (
        {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': acces_control_allow_origin,
            'Access-Control-Allow-Headers': '*',
            'Access-Control-Allow-Methods': 'OPTIONS, GET, PUT, POST, DELETE, PATCH, HEAD',
        }
        if not headers
        else headers
    )
    data = data if not use_camel_case else convert_to_camel_case(data)
    body = {'status': status, 'message': message, 'data': data}

    return {'headers': headers, 'statusCode': status, 'body': json.dumps(body)}

def convert_to_camel_case(data):
    """
    Convert all keys in a dictionary to camel case format.

    Args:
        data (dict, list, or any): The dictionary to convert.

    Returns:
        dict, list, or any: The converted dictionary.

    """
    if isinstance(data, dict):
        new_dict = {}
        for key, value in data.items():
            words = key.split('_')
            new_key = words[0] + ''.join(word.capitalize() for word in words[1:])
            if new_key[0].isupper():
                new_key = new_key[0].lower() + new_key[1:]
            new_dict[new_key] = convert_to_camel_case(value)
        return new_dict
    if isinstance(data, list):
        return [convert_to_camel_case(item) for item in data]
    return data

def return_formatted_response_stepfunction(
    status: int,
    data: Any,
    message_given: str = '',
    use_camel_case: bool = True,
):
    """
    _summary_
    Args:
        status (int): HTTP Response status code
        data (Any): You must provide all the data to be sent through the body of the response
        message_given (str): Additional message that is added to the message of the http method
        use_camel_case (bool): Indicates if response should be camel case

    Returns:
        dict: Formatted Response
    """
    logger.info("****return_formatted_response_stepfunction()****")
    message = RESPONSE_CODES.get(status, 'Internal Server Error')
    message = message + ' ' + message_given
    data = data if not use_camel_case else convert_to_camel_case(data)
    return {'status': status, 'message': message, 'data': data}

def return_formatted_response_error_when_missing_key(missing_key: str) -> dict:
    """
    _summary_
    Args:
        missing_key (str): the key missing in the request
    Returns:
        dict: Formatted Response
    """
    logger.error('No Parameters were send: %s', missing_key)
    message = 'No ' + str(missing_key) + ' param given'
    response = return_formatted_response({}, 400, [], message)
    return response


def change_data_type(data, current_type, new_type):
    """
    This function changes the data type of a variable.
    Args:
        data (any)          : Data structure containing the values to change.
        current_type (any)  : The current data type of the values in 'data'.
        new_type (any)      : The new data type to assign to the values in 'data'.

    Returns:
        any: The 'data' data structure with the values changed to the specified new data type.
    """
    if isinstance(data, current_type):
        return new_type(data)
    if isinstance(data, list):
        return [change_data_type(i, current_type, new_type) for i in data]
    if isinstance(data, tuple):
        return tuple(change_data_type(i, current_type, new_type) for i in data)
    if isinstance(data, dict):
        return {k: change_data_type(v, current_type, new_type) for k, v in data.items()}
    return data

def create_customer_from_json(customer_str: str):
    """_summary_

    Args:
        customer_str (str): It is the customer object who must come in a
        correct JSON format, it will be parsed to be converted into a
        dictionary and returned

    Returns:
        dict: Returns the customer in dict type
    """
    logger.debug("****create_customer_from_json()****")
    try:
        customer = json.loads(customer_str)
        customer = {k[0].capitalize() + k[1:]: v for k, v in customer.items()}
        return customer
    except SyntaxError as error:
        # pylint: disable=broad-exception-raised
        logger.error('Error al evaluar el cuerpo del customer: %s', error)
        raise Exception('Error al evaluar el cuerpo del customer: ' + str(error)) from error

def validate_body(tuples, body):
    """The purpose of this function is to validate the body of a request.
    The body is represented as a dictionary, and the validation is performed by comparing
    the keys and values of the body with a list of tuples,
    where each tuple represents a required key-value pair in the body.

    Args:
        tuples (_type_): list of tuples, where each tuple contains a key string and a data
        type as its second element. These are used as the required keys and expected data
        types in the body.
        body (_type_): dictionary, representing the body of a request.

    Returns:
        body: dictionary if all required keys are present and have the correct data type,
        or a string indicating the missing key or incorrect data type if the validation fails.
    """
    logger.info("****validate_body()****")
    for element in tuples:
        if element[0] not in list(body.keys()):
            return f'Falta elemento {element[0]} en la peticion'

    for body_element in body:
        for telement in tuples:
            if body_element == telement[0]:
                if not isinstance(body[body_element], telement[1]):
                    return f'Elemento {body_element} debe ser de tipo {str(telement[1])}'

    return body

def filter_by_key(list_of_dicts, key, value):
    """
    Searches a list of dictionaries for a specific key and value.

    Args:
        list_of_dicts(list) : the list of dictionaries to search
        key(str)            : the key to search for
        value(any)          : the value to search for

    Returns:
        A list of dictionaries or the only dictionary that contain the specific key and value.
    """
    logger.info("****filter_by_key()****")
    results = [dictionary for dictionary in list_of_dicts if dictionary.get(key) == value]
    return results[0] if len(results) == 1 else results
    
def convert_date_to_string(date: datetime.datetime, formatt: str):
    """Convert a date object into string with the format
    sent through formatt

    Args:
        date (datetime.datetime): date to be converted
        formatt (str): output format in wich you want to be parsed

    Returns:
        str: converted date into str
    """
    return date.strftime(formatt)

def parse_response_fields_to_str(body_fields: dict):
    """This fuction has the object of parse diferents value types
        because json.dumbs() usually throw error trying to parse
        some values.

        You can add more type of castings here.

    Args:
        body_fields (dict): contais de key, value pairs of some
        response of legacy sofware

    Returns:
        dict: return the dictionary with its values parsed
    """
    logger.info("****parse_response_fields_to_str()****")
    for key, value in body_fields.items():
        if isinstance(value, datetime.datetime):
            value = convert_date_to_string(value, '%Y/%m/%d %H:%M:%S')
        body_fields[key] = value
    return body_fields

def reformat_camel_case_init_char(data):
    """
    Reformat camel case keys with first letter in uppercase.

    Args:
        data (dict, list, or any): The dictionary to convert.

    Returns:
        dict, list, or any: The converted dictionary.

    """
    logger.info("****reformat_camel_case_init_char()****")
    if isinstance(data, dict):
        transformed_dict = {}
        for key, value in data.items():
            if isinstance(value, (dict, list)):
                transformed_value = reformat_camel_case_init_char(value)
            else:
                transformed_value = value

            transformed_key = key[0].upper() + key[1:]
            transformed_dict[transformed_key] = transformed_value

        return transformed_dict

    if isinstance(data, list):
        transformed_list = []
        for item in data:
            transformed_item = reformat_camel_case_init_char(item)
            transformed_list.append(transformed_item)

        return transformed_list
    return data

def get_current_time_utc():
    """get current time

    Returns:
        datetime
    """
    logger.info("****get_current_time_utc()****")
    now = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%S')
    current_time = datetime.datetime.strptime(now, '%Y-%m-%dT%H:%M:%S')
    return current_time

def order_customer_search_result(agent: dict, customers: list) -> list:
    """
    Order the customer search result by agent state, then by state and finally by name
    Args:
        agent: the agent that is searching
        customers: the list of customers to be ordered

    Returns:
        the list of customers ordered

    """
    logger.info("****order_customer_search_result()****")
    customers_from_agent_state = [customer for customer in customers if
                                  customer['state'] == agent['AgentState']]
    customers_from_agent_state.sort(key=lambda x: (x['city'], x['name'],
                                                   x['firstLastName'], x['secondLastName']),
                                    reverse=False)
    customers_from_other_states = [customer for customer in customers if
                                   customer['state'] != agent['AgentState']
                                   and customer['state'] != ''
                                   and customer['city'] != '']
    customers_from_other_states.sort(key=lambda x: (x['state'], x['city'], x['name'],
                                                    x['firstLastName'], x['secondLastName']),
                                     reverse=False)
    customers_without_state = [customer for customer in customers if
                               customer['state'] == ''
                               and customer['city'] == '']
    customers_without_state.sort(key=lambda x: (x['name'], x['firstLastName'],
                                                x['secondLastName']), reverse=False)
    final_customers = customers_from_agent_state + customers_from_other_states \
                      + customers_without_state
    return final_customers

class DecimalEncoder(json.JSONEncoder):
    """Custom class to decode decimal in json response"""

    def default(self, o):
        """_summary_

        Args:
            o (object): current object in json

        Returns:
            json: json object with decoded decimal fields
        """
        if isinstance(o, decimal.Decimal):
            return float(o)
        return super().default(o)

def datetime_to_ms(date: datetime, timezone: Optional[str] = None) -> int:
    """
    Convert a datetime to milliseconds
    Args:
        date: datetime to convert
        timezone: timezone to convert the datetime

    Returns:
        milliseconds
    """
    logger.info("****datetime_to_ms()****")
    if timezone:
        date = date.replace(tzinfo=tz.gettz(timezone))
    return calendar.timegm(date.utctimetuple()) * 1000



def camel_to_pascal(key_name:str):
    """
    This function converts a string from camelCase to PascalCase.
    It assumes that the input string is in camelCase
    Args:
        key_name(str): key value in camelCase

    Returns:
        str: key value in PascalCase
    """
    return key_name[0].capitalize() + key_name[1:]


def keys_camel_to_pascal(input_dict):
    """
    This function converts and dictionary with camelCase convention to
    PascalCase convention, this is very usefull when the legacy software
    require the parameters in PascalCase and frontend give us in camelCase.

    Args:
        input_dict (dict): Dict with its key in camelCase 
        convention

    Returns:
        dict: dict with all keys in PascalCase
    """
    pascal_case_dict = {}
    for key, value in input_dict.items():
        pascal_case_key = camel_to_pascal(key)
        pascal_case_dict[pascal_case_key] = value
    return pascal_case_dict


def clean_body_strings(body: dict) -> dict:
    """
    Method to remove unnecessary spaces from a strings inside
    body dictionary
    Args:
        body: json request from any endpoint

    Returns:
        body: json request with clean strings
    """
    logger.info("****clean_body_strings()****")
    for key in body:
        element = body[key]
        if isinstance(element, str):
            clean_string = re.sub(r'\s+', ' ', element).strip()
            body[key] = clean_string
        elif isinstance(element, dict):
            clean_body_strings(element)
    return body


def datetime_instances_parser(obj, datetime_format):
    """
    This functions is responsible to verify if an object contains a datetime
    object and return its value like string representation.

    Validates if:
        1. Datetime format is a valid value
        2. Validates case when the object is a list with nested lists
        3. Validates case when object has nested dictionaries
        4. Validates case when object is a list of dictionaries or nested dictionaries
        5. Validates case when object is a dictionary with lists.
    """
    logger.info("****datetime_instances_parser()****")
    if not isinstance(datetime_format, str):
        raise ValueError('Datetime format must be a string')

    # Recursively parse object
    def recursive_parser(obj):
        if isinstance(obj, dict):
            for key, value in list(obj.items()):
                if isinstance(value, datetime.datetime):
                    obj[key] = convert_date_to_string(value, datetime_format)
                elif isinstance(value, (list, dict)):
                    obj[key] = recursive_parser(value)
        elif isinstance(obj, list):
            for idx, item in enumerate(obj):
                if isinstance(item, datetime.datetime):
                    obj[idx] = convert_date_to_string(item, datetime_format)
                elif isinstance(item, (list, dict)):
                    obj[idx] = recursive_parser(item)
        return obj

    return recursive_parser(obj)


def convert_bytes_to_json_serializable(data: dict) -> dict:
    """
    Method to convert bytes to string in a dictionary
    Args:
        data: dictionary with bytes values

    Returns:
        data: dictionary with string values
    """
    logger.info("****convert_bytes_to_json_serializable()****")
    for key in data:
        element = data[key]
        if isinstance(element, bytes):
            data[key] = base64.b64encode(element).decode('utf-8')
        elif isinstance(element, dict):
            convert_bytes_to_json_serializable(element)
    return data