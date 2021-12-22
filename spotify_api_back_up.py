import sys
import requests
import base64
import json
import logging
import time

client_id = "3c13c0645e2c4362a9dd432816c374e1"
client_secret = "67c82c0c10d441ffaf7b6fa6f670419f"

def main():
    header = get_headers(client_id, client_secret)

    # Spotify SearchAPI params
    params = {
        "q": "BTS",        # etc, SG Wannabe
        "type": "artist",
        "limit": "5"       # number of results
    }

    # send a request for search
    r = requests.get("https://api.spotify.com/v1/search", params=params, headers=header)
    try:
        r = requests.get("https://api.spotify.com/v1/search", params=params, headers=header)
    except:
        logging.error(r.text)
        sys.exit(1)
    print("1. r.status_code: ", r.status_code)
    # print("2. r.text: ", r.text) 
    # print("3. r.headers: ", r.headers)

    # Check for the error handling
    if r.status_code != 200:
        logging.error(json.loads(r.text))

        if r.status_code == 429: # too many requests
            retry_after = json.loads(r.headers)['Retry-After']
            time.sleep(int(retry_after))

            # retry after a certain time period
            r = requests.get("https://api.spotify.com/v1/search", params=params, headers=header)




def get_headers(client_id, client_secret):
    endpoint = "https://accounts.spotify.com/api/token"
    encoded = base64.b64encode("{}:{}".format(client_id, client_secret).encode('utf-8')).decode('ascii')
    headers = {
        "Authorization": "Basic {}".format(encoded),
        "Content-Type": "application/x-www-form-urlencoded"
    }
    payload = {
        "grant_type":"client_credentials"
    }

    req = requests.post(endpoint, data=payload, headers=headers)

    access_token = json.loads(req.text)["access_token"]

    headers = {
        "Authorization": "Bearer {}".format(access_token)
    }
    return headers


if __name__ == '__main__':
    main()
