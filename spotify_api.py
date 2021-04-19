import sys
import requests
import base64
import json
import logging

client_id = "3c13c0645e2c4362a9dd432816c374e1" # 3c13c0645e2c4362a9dd432816c374e1
client_secret =

def main():
    header = getHeader(client_id, client_secret)

    # Spotify SearchAPI
    params = {
        "q": "BTS",
        "type": "artist",
        "limit": "5" # number of results
    }

    try:
        api_url = "https://api.spotify.com/v1/search"
        req = requests.get(api_url, params=params, headers=header)
    except:
        logging.error(req.text)

        # Error cases reference: https://developer.spotify.com/documentation/web-api/
        if req.status_code != 200:
            logging.error(json.loads(req.text))

            # "Too Many Requests - Rate limiting has been applied."
            if req.status_code == 429:
                retry_after = json.loads(req.headers)['Retry-After']
                time.sleep(int(retry_after))
                req = requests.get(api_url, params=params, headers=header)

            # access token is denied
            elif req.status_code == 401:
                logging.error("Access token is denied. Retring...")
                header = getHeader(client_id, client_secret)
                req = requests.get(api_url, params=params, headers=header)

            else:
                sys.exit(1)

    # Extract artist id
    id = extractID(req.text)
    # print("1. id: ", id)

def extractID(text):
    try:
        id = json.loads(text)['artists']['items'][0]['id']
    except:
        logging.error("Extracting id failed.")
    return id


def getHeader(client_id, client_secret):
    endpoint_url = "https://accounts.spotify.com/api/token"

    # encoding format url: https://developer.spotify.com/documentation/general/guides/authorization-guide/
    encoded = base64.b64encode("{}:{}".format(client_id, client_secret).encode('utf-8')).decode('ascii')
    header = {
        "Authorization": "Basic {}".format(encoded)
    }
    body_param = {
        "grant_type": "client_credentials"
    }

    req = requests.post(endpoint_url, data=body_param, headers=header)

    try:
        access_token = json.loads(req.text)['access_token']
    except:
        logging.error("Valid access token required")
        sys.exit(1)

    return_header = {
        "Authorization": "Bearer {}".format(access_token)
    }
    return return_header


if __name__ == '__main__':
    main()
