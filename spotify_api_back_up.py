import sys
import requests
import base64
import json
import logging

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
    api_url = "https://api.spotify.com/v1/search"
    r = requests.get(api_url, params=params, headers=header)


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
