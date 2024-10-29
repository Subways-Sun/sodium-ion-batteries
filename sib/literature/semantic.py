"""Module performing API calls to Semantic Scholar"""

import requests

def search(query, **kwargs):
    """Function to search for papers"""
    limit = kwargs.get('limit', None)
    fields = kwargs.get('fields', None)
    offset = kwargs.get('offset', None)

    base_url = "https://api.semanticscholar.org/graph/v1/paper/search"

    q = "?query=" + query
    l = ""
    f = ""
    o = ""
    if limit is not None:
        l = "&limit=" + str(limit)
    if fields is not None:
        f = "&fields=" + fields
    if offset is not None:
        o = "&offset=" + str(offset)

    url = f"{base_url}{q}{o}{l}{f}"

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
