"""
Utility functions used for querying the Open5e API using inputs
read from discord messages.
Author: Maxwell Herron
Python Version: 3.8.6
"""

import os
import logging
import json

import urllib3
from dotenv import load_dotenv

# Creating access to environment variables
load_dotenv()
DND_URL = os.getenv('DND_URL')

logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)

class RequestExecutionError(Exception):
    """Custom exception raised when errors occur during Open5e requests"""
    pass


def get_spell_details(spell: str) -> dict:
    """Makes a request to Open5e to access all details on the given spell.

    Params:
        spell (str): Name of the spell formatted for the GET request.

    Returns:
        formatted_details (dict): Dictionary representation of all spell details.
    
    Raises:
        RequestExecutionError
    """
    http = urllib3.PoolManager()
    endpoint = f"{DND_URL}/spells/{spell}/"
    LOGGER.info("Request: %s", endpoint)
    res = http.request('GET', endpoint)
    details = json.loads(res.data.decode('utf-8'))
    LOGGER.info("GET REQUEST RESPONSE CODE: %d", res.status)
    if res.status != 200:
        LOGGER.error("Request failed with error message: %s", details['detail'])
        raise RequestExecutionError

    # Trimming unneeded details from result
    junk_keys = ["slug", "document__slug", "document__title", "document__license_url"]
    [details.pop(key) for key in junk_keys]

    # Cleaning up field names for a pretty print
    formatted_details = {field.replace("_", " ").capitalize(): details[field] for field in details}
    LOGGER.info(formatted_details)
    return formatted_details
