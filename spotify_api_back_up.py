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

    # 1. Send a request for search
    r = requests.get("https://api.spotify.com/v1/search", params=params, headers=header)
    try:
        r = requests.get("https://api.spotify.com/v1/search", params=params, headers=header)
    except:
        logging.error(r.text)
        sys.exit(1)
    # print("1. r.status_code: ", r.status_code)
    # print("2. r.text: ", r.text) 
    # print("3. r.headers: ", r.headers)
    logging.info("Successfully done for search")

    # 2. Check for the error handling
    if r.status_code != 200:
        logging.error(json.loads(r.text))

        if r.status_code == 429: # too many requests
            retry_after = json.loads(r.headers)['Retry-After']
            time.sleep(int(retry_after))

            # retry after a certain time period
            r = requests.get("https://api.spotify.com/v1/search", params=params, headers=header)
        elif r.status_code == 401: # access token expired error
            headers = get_headers(client_id, client_secret)
            r = requests.get("https://api.spotify.com/v1/search", params=params, headers=header)
        else:
            sys.exit(1)

    # 3. get BTS albums
    r = requests.get("https://api.spotify.com/v1/artists/3Nrfpe0tUJi4K4DXYWgMUX/albums", headers=header)
    raw_data = json.loads(r.text)

    total = raw_data["total"]
    offset = raw_data["offset"]
    limit = raw_data["limit"]
    next = raw_data["next"]

    albums = []
    albums.extend(raw_data["items"])
    # 4. returns only 100 or less albums (pagination handlling)
    cnt = 0
    while cnt < 100 and next:
        r = requests.get(raw_data["next"], headers=header)
        raw_data = json.loads(r.text)
        next = raw_data["next"]

        albums.extend(raw_data["items"])
        cnt = len(albums)
    print(len(albums))





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
