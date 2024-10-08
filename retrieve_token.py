from re import L
import requests, json, time, getopt, sys, configparser, os

base_URL = 'https://api.refinitiv.com'
category_URL = '/auth/oauth2'
AUTHENTICATION = "/v1"
endpoint_URL = '/token'

CREDENTIALS_FILE = 'credentials.json'
TOKEN_FILE = 'token.txt'

def load_credentials(api_no = 0):
    if os.path.exists(CREDENTIALS_FILE):
        with open(CREDENTIALS_FILE, 'r') as json_file:
            credentials = json.load(json_file)
            USERNAME = credentials['username'][api_no]
            PASSWORD = credentials['password'][api_no]
            KEY = credentials['key'][api_no]
            json_file.close()
    else:
        print("Need to set credentials by creating credentials.json")
    return USERNAME, PASSWORD, KEY

def request_token(refresh_token = None, api_no = 0):
    USERNAME, PASSWORD, KEY = load_credentials(api_no)

    TOKEN_ENDPOINT = base_URL + category_URL + AUTHENTICATION + endpoint_URL
    if refresh_token is None:
        tData = {
            "username": USERNAME,
            "password": PASSWORD,
            "grant_type": "password",
            "scope": "trapi",
            "takeExclusiveSignOnControl": "true"
        }
    else:
        tData = {
            "refresh_token": refresh_token,
            "grant_type": "refresh_token"
        }
    response = requests.post(
        TOKEN_ENDPOINT,
        headers = {
            "Accpet": "application/json"
        },
        data = tData,
        auth = (
            KEY,
            ""
        )
    )
    if (response.status_code == 400) & ('invalid_grant' in response.text):
        print("Error: grant unsuccessful")
        return None
    
    if response.status_code != 200:
        raise Exception(f"Failed to get access token {0} - {1}".format(response.status_code, response.text))
    
    return json.loads(response.text)

def save_token(token):
    tf = open(TOKEN_FILE, "w+")
    token['expiry_tm'] = time.time() + int(token['expires_in']) - 10
    json.dump(token, tf, indent = 4)
    tf.close()

def load_token():
    token = None
    try:
        tf = open(TOKEN_FILE, "r+")
        token = json.load(tf)
        tf.close()
    except Exception:
        pass
    return token

def get_token(api_no = 0):
    token = load_token()
    if token is not None:
        if token['expiry_tm'] > time.time():
            return token['access_token']
        token = request_token(refresh_token = token['refresh_token'], api_no = api_no)
        if token is None:
            token = request_token(api_no = api_no)
    else:
        token = request_token(api_no = api_no)
    save_token(token)
    return token['access_token']

if __name__ == "__main__":    
    access_token = get_token(api_no = 1)