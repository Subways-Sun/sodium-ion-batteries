"""Module performing API calls to Semantic Scholar."""

# OK Include DOI
# OK Publication data
# WIP Different query and merge result
# WIP No review papers
# WIP Restrict publisher
# WIP BatteryBERT
# OK Bulk Search

import time
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
    if fields is not (None or ""):
        f = "&fields=" + fields
    if offset is not None:
        o = "&offset=" + str(offset)
    if publication_types is not (None or ""):
        pt = "&publicationTypes=" + publication_types

    url = f"{base_url}{q}{o}{l}{f}{pt}"

    response = requests.get(url, timeout=1000)
    result = {}

    if response.status_code == 200:
        result = response.json()['data']
    elif response.status_code == 400:
        result = [response.json()]
    elif response.status_code == 429:
        time.sleep(2)
        return search(query, **kwargs)
    else:
        result = [response.status_code]
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

    if fields is not (None or ""):
        f = "&fields=" + fields
    if publication_types is not (None or ""):
        pt = "&publicationTypes=" + publication_types
    if token is not (None or ""):
        t = "&token=" + token

    url = f"{base_url}{q}{f}{pt}{t}"

    response = requests.get(url, timeout=1000)
    result = {}
    result_token = ""

    if response.status_code == 200:
        result = response.json()['data']
        result_token = response.json()['token']
    elif response.status_code == 400:
        result = [response.json()]
    elif response.status_code == 429:
        time.sleep(2)
        return search_bulk(query, **kwargs)
    else:
        result = [response.status_code]
    return [result, url, result_token]
