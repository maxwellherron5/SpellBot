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
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


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
        error = f"Oops, looks like the database doesn't have an entry for that spell :( not my fault ¯\_(ツ)_/¯"
        LOGGER.error(error)
        raise RequestExecutionError(error)

    # Trimming unneeded details from result
    junk_keys = ["slug", "document__slug", "document__title", "document__license_url"]
    [details.pop(key) for key in junk_keys]

    # Cleaning up field names for a pretty print
    formatted_details = {field.replace("_", " ").capitalize(): details[field] for field in details}
    LOGGER.info(formatted_details)
    return formatted_details


def get_monster_details(monster: str) -> dict:
    """Makes a request to Open5e to access all details on the given monster.

    Params:
        monster (str): Name of the monster formatted for the GET request.

    Returns:
        formatted_details (dict): Dictionary representation of all monster details.

    Raises:
        RequestExecutionError
    """
    http = urllib3.PoolManager()
    endpoint = f"{DND_URL}/monsters/{monster}/"
    LOGGER.info("Request: %s", endpoint)
    res = http.request('GET', endpoint)
    details = json.loads(res.data.decode('utf-8'))
    LOGGER.info("GET REQUEST RESPONSE CODE: %d", res.status)
    if res.status != 200:
        error = f"Oops, looks like the database doesn't have an entry for that monster :( not my fault ¯\_(ツ)_/¯"
        LOGGER.error(error)
        raise RequestExecutionError(error)

    # Trimming unneeded details from result
    junk_keys = ["img_main", "document__slug", "document__title", "document__license_url"]
    [details.pop(key) for key in junk_keys]

    # Cleaning up field names for a pretty print
    formatted_details = {field.replace("_", " ").capitalize(): details[field] for field in details}

    # Normalizing list or dictionary attributes into strings
    normalized_details = {}
    for field in formatted_details:
        if isinstance(formatted_details[field], dict):
            normalized_details[field] = '\n'.join("%s: %s" % tup for tup in formatted_details[field].items())
            LOGGER.info("Dict converted to %s", normalized_details[field])
        elif isinstance(formatted_details[field], list):
            normalized_details[field] = '\n'.join(['\n'.join("%s: %s" % tup for tup in subfield.items()) for subfield in formatted_details[field]])
            LOGGER.info("List converted to %s", normalized_details[field])
        else:
            normalized_details[field] = formatted_details[field]

    LOGGER.info(normalized_details)
    return normalized_details
