"""Module performing API calls to Semantic Scholar"""

# Include DOI
# Publication data
# Different query and merge result
# No review papers
# Restrict publisher
# BatteryBERT
# Bulk Search

import requests

def search(query, **kwargs):
    """Function to search for papers"""
    limit = kwargs.get('limit', None)
    fields = kwargs.get('fields', None)
    offset = kwargs.get('offset', None)
    publication_types = kwargs.get('publicationTypes', None)

    base_url = "https://api.semanticscholar.org/graph/v1/paper/search"

    q = "?query=" + query
    l = ""
    f = ""
    o = ""
    pt = ""

    if limit is not None:
        l = "&limit=" + str(limit)
    if fields is not None:
        f = "&fields=" + fields
    if offset is not None:
        o = "&offset=" + str(offset)
    if publication_types is not None:
        pt = "&publicationTypes=" + publication_types

    url = f"{base_url}{q}{o}{l}{f}{pt}"

    response = requests.get(url, timeout=1000)
    result = {}

    if response.status_code == 200:
        result = response.json()['data']
    elif response.status_code == 429:
        result = response.json()['message']
    elif response.status_code == 400:
        result = response.json()['error']
    else:
        result = response.status_code
    return [result, url]

def search_bulk(query, **kwargs):
    """Function to search for papers using bulk search"""
    fields = kwargs.get('fields', None)
    publication_types = kwargs.get('publicationTypes', None)
    token = kwargs.get('token', None)

    base_url = "https://api.semanticscholar.org/graph/v1/paper/search/bulk"

    q = "?query=" + query
    f = ""
    pt = ""
    t = ""

    if fields is not None:
        f = "&fields=" + fields
    if publication_types is not None:
        pt = "&publicationTypes=" + publication_types
    if token is not None:
        t = "&token=" + token

    url = f"{base_url}{q}{f}{pt}{t}"

    response = requests.get(url, timeout=1000)
    result = {}
    result_token = ""

    if response.status_code == 200:
        result = response.json()['data']
        result_token = response.json()['token']
    elif response.status_code == 429:
        result = response.json()['message']
    elif response.status_code == 400:
        result = response.json()['error']
    else:
        result = response.status_code
    return [result, url, result_token]
