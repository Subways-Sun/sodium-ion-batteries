"""Script to retrive relevant paper"""
# pylint: disable=locally-disabled, line-too-long, invalid-name, logging-fstring-interpolation
import os
import time
import logging
from datetime import datetime
from sib.literature import semantic as ss
from sib.literature import scopus as sc
from sib.literature import springer as sp
from sib.literature import lit_processing as lp

logging.basicConfig(
    filename = f"logs/info_search_{time.strftime('%Y-%m-%d_%H%M%S')}.log",
    encoding = "utf-8",
    filemode = "a",
    format = "{asctime} - {levelname} - {message}",
    style = "{",
    datefmt = "%Y-%m-%d %H:%M:%S",
    level = logging.INFO
)

# Define search parameters
# query_list = ["sodium+ion+battery+anode",
#               "sodium+ion+battery+cathode",
#               "sodium+ion+battery+electrode",
#               "sib+cathode",
#               "sib+anode",
#               "sib+electrode"]
query_list = ["lithium+ion+battery+anode",
              "lithium+ion+battery+cathode",
              "lithium+ion+battery+electrode"]

fields = "externalIds,title,abstract,publicationTypes,publicationDate"
count = 30 # Number of papers to retrieve for each keyword
publication_types = "JournalArticle" # Only retrieve journal articles
year = "2016-" # Only retrieve papers published after 2016

result = list([])
url_list = list([])

# Search for relevant papers
for query in query_list:
    # result_temp = ss.search_bulk(query, count, fields = fields, publicationTypes = publication_types, year = year)
    result_temp = ss.search(query, fields = fields, publicationTypes = publication_types, year = year, limit = count)
    data = result_temp[0]
    url = result_temp[1]
    logging.info(f"Number of papers retrieved for '{query.replace('+', ' ')}': {len(data)}")
    result.extend(data)
    url_list.append(url)
logging.info(f"Finished initial search, number of papers retrieved: {len(result)}")

# Remove duplicates
result = lp.remove_duplicates(result)
logging.info(f"Number of papers after removing duplicates: {len(result)}")

# Only keep papers from select publishers
# publishers = ["10.1039", # RSC
#               "10.1016", # Elsevier
#               "10.1021", # ACS
#               "10.1002", # Wiley
#               "10.1007", # Springer
#               "10.1080", # Taylor & Francis
#               "10.1038"] # Nature
# result = lp.keep_select_publishers(result, publishers)
# logging.info(f"Number of papers from select publishers: {len(result)}")

# Retrieve abstract from Scopus and Springer
for paper in result:
    doi = paper.get("externalIds").get("DOI")
    if doi[:7] == "10.1016":
        logging.info(f"Retrieving abstract for {doi} from Scopus")
        abstract = sc.get_paper_details(doi)[0]["full-text-retrieval-response"]["coredata"]["dc:description"]
        if abstract:
            paper["abstract"] = abstract.strip()
    elif doi[:7] == "10.1007" or doi[:7] == "10.1038":
        logging.info(f"Retrieving abstract for {doi} from Springer")
        abstract = sp.get_paper_details(doi)[0]["records"][0]["abstract"]
        if abstract:
            paper["abstract"] = abstract
        time.sleep(0.7) # Sleep for 0.7 seconds to avoid exceeding the rate limit

# Remove papers with no abstract
result = lp.remove_no_abstract(result)
logging.info(f"Number of papers after removing papers with no abstract: {len(result)}")

# Save the search parameters to a json file
current_time = datetime.now().strftime("%Y%m%d-%H%M%S")
params = {"searchKeywords": query_list, "fields": fields, "count": count, "publicationTypes": publication_types, "year": year, "result_len": len(result), "urls": url_list}
params_path = os.path.join(os.getcwd(), "data", f"search_{current_time}_params.json")
lp.write_json(params_path, params)

# Print the number of papers retrieved
logging.info(f"Number of papers retrieved: {len(result)}")

# Save the result to a json file
result_path = os.path.join(os.getcwd(), "data", f"search_{current_time}.json")
lp.write_json(result_path, result)
