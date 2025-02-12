"""Module performing API calls to Scopus."""
# pylint: disable=locally-disabled, line-too-long, invalid-name
import requests

API_KEY = "754810bbc14f298dcb929584abbe5f50"

def get_paper_details(DOI: str):
    """Function to search for paper details using DOI"""
    url = f"https://api.elsevier.com/content/article/doi/{DOI}"
    params = {"httpAccept": "application/json",
              "apiKey": API_KEY,
              "view": "META_ABS"}
    response = requests.get(url, params=params, timeout=1000)
    return [response.json(), response.url]

# print(get_paper_details("10.1021/acs.nanolett.9b00544")[1])
