"""Module performing API calls to Semantic Scholar"""

import requests

def search(query, **kwargs):
    """Function to search for papers"""

    limit = kwargs.get('limit', None)
    fields = kwargs.get('fields', None)

    base_url = "https://api.semanticscholar.org/graph/v1/paper/search"

    q = "?query=" + query
    l = ""
    f = ""
    if limit is not None:
        l = "&limit=" + str(limit)
    if fields is not None:
        f = "&fields=" + fields

    url = f"{base_url}{q}{l}{f}"

    response = requests.get(url, timeout=100)
    result = {}

    if response.status_code == 200:
        result = response.json()

    return result
