"""Module performing API calls to Scopus."""
# pylint: disable=locally-disabled, line-too-long, invalid-name
import requests

API_KEY = "7e2e02f53d5387dcdb65448f2fee2074"

def get_paper_details(DOI: str):
    """Function to search for paper details using DOI"""
    url = "https://api.springernature.com/meta/v2/json"
    params = {"api_key": API_KEY,
              "q": f"doi:{DOI}"}
    response = requests.get(url, params=params, timeout=1000)
    return [response.json(), response.url]
