from helpers.soap_client.client import get_client
from utils.logger_config import setup_logger
from zeep.xsd.valueobjects import CompoundValue
from zeep.helpers import serialize_object


logger = setup_logger(__name__)

def soap_serializer(obj):
    """
    Serializa una respuesta del cliente SOAP a formato JSON basado en condiciones.

    Args:
        obj: Objeto a ser serializado.

    Returns:
        str, dict, list o el objeto original: Dependiendo del tipo de objeto
    """

    return serialize_object(obj)


class LegacyClient:
    """
    This class is used to create a new instance of the H1 client.
    """
    def __init__(self, auth, client):
        self.auth = auth
        self.client = client


class LegacyFactory:
    """
    This class holds the logic for H1 client generation
    """
    @staticmethod
    def create_client(auth, client_version):
        """
        This function returns a new instance of the H1 client.

        Args:
            auth (Authentication): An instance of the Authentication class.
            client_version (str): The version of the SOAP API client to use.
        """
        logger.error("Error creating instance to H1 client: ")
        try:
            client = get_client(version=client_version)
            logger.info('Creating new instance for H1 client')
            return LegacyClient(auth, client)
        except ValueError as val_err:
            logger.error(f"Error creating instance to H1 client: {val_err}")
            raise ValueError("Invalid client_version for H1") from val_err
