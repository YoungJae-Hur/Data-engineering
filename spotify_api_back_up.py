import sys
import requests
import base64
import json
import logging

client_id = "3c13c0645e2c4362a9dd432816c374e1"
client_secret = "67c82c0c10d441ffaf7b6fa6f670419f"

def main():
    endpoint = "https://accounts.spotify.com/api/token"
    encoded = base64.b64encode("{}:{}".format(client_id, client_secret).encode('utf-8')).decode('ascii')
    headers = {
        "Authorization": "Basic {}".format(encoded),
        "Content-Type": "application/x-www-form-urlencoded"
    }
    payload = {
        "grant_type":"client_credentials"
    }
    print("1. encoded: ", encoded)
    req = requests.post(endpoint, data=payload, headers=headers)
    print("2. req: ", req, req.text)
    # if there is no error until this moment, exit the program
    sys.exit(0)

    access_token = json.loads(req.text)["access_token"]
    print("3. access_token: ", access_token)

if __name__ == '__main__':
    main()
