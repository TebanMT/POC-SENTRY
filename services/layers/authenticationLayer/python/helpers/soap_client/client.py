"""
Helper that exports the soap client that manages the translation between SOAP and REST operations
"""
import os
from utils.logger_config import setup_logger

from zeep import Client

logger = setup_logger(__name__)

__CLIENTS = {}

def get_client(version: str = "1", transport = None):
    """Initializes singleton SOAP instance

    Params:
        version (str, default=1): The version of the api soap

    Returns:
        suds.Client: the suds initialized client with the soap configuration
    """
    logger.info("****get_client() AUthLayer****")
        
    endpoints_url = {
        "1": os.environ.get('LEGACY_FRONT_OFFICE1', ''),
        "2": os.environ.get('LEGACY_FRONT_OFFICE2', ''),
        "ReportExecution2005": os.environ.get('REPORTING_SERVICES_WSDL', ''),
        "erp": os.environ.get('ERP_SERVICES_WSDL', ''),
        "billpayment": os.environ.get("BILLPAYMENT_SERVICE", ''),
        "general_billpayment": os.environ.get("BILLPAYMENT_SERVICE", ''),
        "collection_payments": os.environ.get("COLLECTION_PAYMENTS_WSDL", '')
    }

    if version in __CLIENTS:
        return __CLIENTS[version]

    soap_url = endpoints_url.get(version, None)
    logger.info(f"Layer Using the version {version} of the api hermes: {soap_url}")

    if not soap_url:
        logger.error("Api url hermes 1 version not found")
        raise ValueError("Api url hermes 1 version not found")

    if transport:
        __CLIENTS[version] = Client(f'{soap_url}?wsdl', transport=transport)
        return __CLIENTS[version]

    __CLIENTS[version] = Client(f'{soap_url}?WSDL')
    logger.info(f"_CLIENTS=>{__CLIENTS}")
    return __CLIENTS[version]
