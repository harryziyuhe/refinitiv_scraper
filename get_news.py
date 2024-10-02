import requests
import retrieve_token
import json

base_URL = 'https://api.refinitiv.com'
category_URL = '/data/news/v1'
headlines_URL = '/headlines'
stories_URL = '/stories'
topnews_URL = '/top-news'

def get_headlines(ticker = None, 
                  language = None, 
                  country = None, 
                  source = None, 
                  page = None):
    access_token = retrieve_token.get_token()
    ENDPOINT = base_URL + category_URL + headlines_URL
    query = []
    if ticker is not None:
        query.append(f'R:{ticker}')
    if language is not None:
        query.append(f'L:{language.upper()}')
    if country is not None:
        query.append(f'G:{country.upper}')
    if source is not None:
        query.append(f'NS:{source}')
    #query = ' AND '.join(query)
    query = "NGS and l:en and EUROP"
    #params = {
    #    "query": query,
    #    "limit": "50"
    #}
    params = {
        "query": "TOPNEWS"
    }

    response = requests.get(ENDPOINT, headers = {"Authorization": "Bearer " + access_token}, params = params)
    if response.status_code != 200:
        print(f"Error occurred: response status {response.status_code}")
    else:
        headlines = json.loads(response)
        with open('headlines.json', 'w') as json_file:
            json.dump(json_file, headlines, indent = 4)

def get_topnews():
    accessToken = retrieve_token.get_token()
    print("Invoking data request")
    ENDPOINT = base_URL + category_URL + topnews_URL
    print(ENDPOINT)
    response = requests.get(ENDPOINT, headers = {"Authorization": "Bearer " + accessToken})
    if response.status_code != 200:
        print(f"Error occurred: response status {response.status_code}, {response.text}")
    else:
        topnews = json.loads(response)
        with open('topnews.json', 'w') as json_file:
            json.dump(json_file, topnews, indent = 4)

if __name__ == "__main__":
    get_topnews()
    #get_headlines(ticker = "MSFT.O", language = "EN", source = "RTRS")

