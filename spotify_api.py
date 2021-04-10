import sys
import requests
import base64
import json
import logging

client_id = "3c13c0645e2c4362a9dd432816c374e1"
clinet_secret =

def main():
    endpoint_url = "https://accounts.spotify.com/api/token"

    # encoding format url: https://developer.spotify.com/documentation/general/guides/authorization-guide/
    encoded = base64.b64encode("{}:{}".format(client_id, clinet_secret).encode('utf-8')).decode('ascii')
    header = {
        "Authorization": "Basic {}".format(encoded)
    }
    body_param = {
        "grant_type": "client_credentials"
    }

    req = requests.post(endpoint_url, data=body_param, headers=header)
    access_token = json.loads(req.text)['access_token']


if __name__ == '__main__':
    main()
