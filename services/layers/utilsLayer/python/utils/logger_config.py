"""
Module logger_config.py
-----------------------
This module provides a `setup_logger` function to configure a logger object
with the specified name and the log level specified by an environment variable.
The logger has a single handler that emits to stdout with a specific message format.
"""

import os
import sys
import logging
import sentry_sdk
from sentry_sdk.integrations.logging import LoggingIntegration
from sentry_sdk.integrations.aws_lambda import AwsLambdaIntegration

# Configuración de Sentry
sentry_logging = LoggingIntegration(
    level=logging.ERROR,        # Capture logs at ERROR level or higher
    event_level=logging.ERROR   # Send error logs as events
)

sentry_sdk.init(
    dsn="https://9400f5f338e995c83bb0faee1b0d871e@o1181837.ingest.us.sentry.io/4507251126697984",
    integrations=[AwsLambdaIntegration(), sentry_logging],
    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    traces_sample_rate=1.0,
    # Set profiles_sample_rate to 1.0 to profile 100%
    # of sampled transactions.
    # We recommend adjusting this value in production.
    profiles_sample_rate=1.0,
    environment='dev'
)


def setup_logger(name: str) -> logging.Logger:
    """
    Configures and returns a logger object with the specified name.

    Parameters
    ----------
    name : str
        The name of the logger.

    Returns
    -------
    logger : logging.Logger
        A logger object configured with the specified name and log level.

    Notes
    -----
    The log level is obtained from the 'LOG_LEVEL' environment variable. If 'LOG_LEVEL' is not
    set, 'DEBUG' is used as the default log level.
    The logger has a single handler that emits to stdout with a specific message format.
    """

    # Usa 'DEBUG' como valor predeterminado si LOG_LEVEL no está configurado
    level = os.getenv('LOG_LEVEL', 'DEBUG')
    numeric_level = getattr(logging, level.upper(), None)

    if not isinstance(numeric_level, int):
        raise ValueError(f'Invalid log level: {level}')

    logger = logging.getLogger(name)
    logger.setLevel(numeric_level)

    if not logger.handlers:
        # Evita la duplicación de logs
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    return logger

