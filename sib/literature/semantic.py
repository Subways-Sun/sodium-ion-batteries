"""Module performing API calls to Semantic Scholar."""
# pylint: disable=locally-disabled, line-too-long, invalid-name

import time
import requests

def search(query: str, **kwargs):
    """Function to search for papers"""
    limit = kwargs.get('limit', None)
    fields = kwargs.get('fields', None)
    offset = kwargs.get('offset', None)
    publication_types = kwargs.get('publicationTypes', None)

    url = "https://api.semanticscholar.org/graph/v1/paper/search"

    if limit == "":
        limit = None
    if fields == "":
        fields = None
    if offset == "":
        offset = None
    if publication_types == "":
        publication_types = None
    
    params = {"query": query,
              "limit": limit,
              "fields": fields,
              "offset": offset,
              "publicationTypes": publication_types}

    response = requests.get(url, params=params, timeout=1000)
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
    return [result, response.url]

def search_bulk_token(query: str, **kwargs):
    """Function to search for papers using bulk search"""
    fields = kwargs.get('fields', None)
    publication_types = kwargs.get('publicationTypes', None)
    token = kwargs.get('token', None)
    year = kwargs.get('year', None)

    if fields == "":
        fields = None
    if publication_types == "":
        publication_types = None
    if token == "":
        token = None
    if year == "":
        year = None

    url = "https://api.semanticscholar.org/graph/v1/paper/search/bulk"

    params = {"query": query,
              "fields": fields,
              "publicationTypes": publication_types,
              "token": token,
              "year": year}

    response = requests.get(url, params=params, timeout=1000)
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
    return [result, response.url, result_token]

def search_bulk(query: str, count: int, **kwargs):
    """Function to search for papers using bulk search with token"""
    fields = kwargs.get('fields', None)
    publication_types = kwargs.get('publicationTypes', None)
    year = kwargs.get('year', None)

    result = []
    url_list = []
    token = ""
    for i in range(0, count, 1000):
        result_temp = search_bulk_token(query, fields = fields, publicationTypes = publication_types, token = token, year = year)
        temp = result_temp[0]
        url = result_temp[1]
        for item in temp:
            result.append(item)
        url_list.append(url)
        time.sleep(2)

        # Break when token is None (no more papers to retrieve)
        if result_temp[2] is None:
            token = ""
            break
        token = result_temp[2]

    return [result, url_list]

def search_paper_details(DOI: str, **kwargs):
    """
    Function to search for papers using bulk search
    Example: search_paper_details("10.1021/acsami.1c01994", fields = "title,abstract,authors,year")
    """
    fields = kwargs.get('fields', None)
    # publication_types = kwargs.get('publicationTypes', None)
    # token = kwargs.get('token', None)
    # year = kwargs.get('year', None)

    base_url = "https://api.semanticscholar.org/graph/v1/paper"

    d = "/DOI:" + DOI
    f = ""
    # pt = ""
    # t = ""
    # y = ""

    if fields is not (None or ""):
        f = "?fields=" + fields
    # if publication_types is not (None or ""):
    #     pt = "&publicationTypes=" + publication_types
    # if token is not (None or ""):
    #     t = "&token=" + token
    # if year is not (None or ""):
    #     y = "&year=" + year

    url = f"{base_url}{d}{f}"

    response = requests.get(url, timeout=1000)
    result = {}
    result_token = ""

    if response.status_code == 200:
        result = response.json()
    elif response.status_code == 400:
        result = [response.json()]
    elif response.status_code == 429:
        time.sleep(2)
        return search_bulk(DOI, **kwargs)
    else:
        result = [response.status_code]
    return [result, url, result_token]
