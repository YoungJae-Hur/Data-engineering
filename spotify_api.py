import sys
import requests
import base64
import json
import logging

client_id = "3c13c0645e2c4362a9dd432816c374e1"
client_secret =

def main():
    header = getHeader(client_id, client_secret)

    # Spotify SearchAPI
    params = {
        "q": "BTS",
        "type": "artist",
        "limit": "5" # number of results
    }
    api_url = "https://api.spotify.com/v1/search"
    req = requests.get(api_url, params=params, headers=header)
    # print("3. req status code: ", req.status_code)
    # print("4. req text: ", req.text)

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
    access_token = json.loads(req.text)['access_token']
    return_header = {
        "Authorization": "Bearer {}".format(access_token)
    }
    return return_header


if __name__ == '__main__':
    main()
