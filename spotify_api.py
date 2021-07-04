import sys
import requests
import base64
import json
import logging
import pymysql
from aws_setting import (
    get_host, get_port, get_user, get_db_pw, get_db_name
)

client_id = "3c13c0645e2c4362a9dd432816c374e1"
client_secret = "f7ceedd980a94a91a05c1f9a6d2db220"

def main():
    logging.basicConfig(level = logging.INFO)

    # aws db connection
    conn, cursor = connectAWSdb()
    logging.info("Connected to AWS Database...")
    cursor.execute("SHOW TABLES")
    logging.info(cursor.fetchall())
    # cursor.execute("SELECT * from artist_genres")
    # logging.info(cursor.fetchall())

    # INSERT data to db
    query = "INSERT INTO artist_genres (artist_id, genre) VALUES ('%s', '%s')" % ('2345', 'pop')
    cursor.execute(query)
    conn.commit()
    logging.info("Insertion is completed...")
    sys.exit(0)

    # Get Spotify connection using client id and secret key
    header = getHeader(client_id, client_secret)

    # Spotify SearchAPI params
    params = {
        "q": "BTS",        # etc, SG Wannabe
        "type": "artist",
        "limit": "5"       # number of results
    }

    try:
        api_url = "https://api.spotify.com/v1/search"
        req = requests.get(api_url, params=params, headers=header)
    except:
        logging.error(req.text)

        # Error case reference: https://developer.spotify.com/documentation/web-api/
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
                sys.exit(1) # unsuccessful

    # Extract artist id
    id = extractID(req.text)

    # Get BTS total number of albums
    req = requests.get("https://api.spotify.com/v1/artists/{}/albums".format(id), headers=header)
    raw_data = json.loads(req.text)

    albums = []
    next = raw_data['next']
    while next:
        req = requests.get(next, headers=header)
        raw_data = json.loads(req.text)
        next = raw_data['next']
        albums.extend(raw_data['items'])
    logging.info("Total number of albums: " + str(len(albums)))

def connectAWSdb():
    host = get_host()
    port = get_port()
    usr = get_user()
    pw = get_db_pw()
    db = get_db_name()
    
    # Connect to AWS database
    try:
        conn = pymysql.connect(host=host,
                             user=usr,
                             password=pw,
                             db=db,
                             port=port,
                             use_unicode=True,
                             charset='utf8')
        cursor = conn.cursor()
    except:
        logging.error("AWS DB connection failed...")
        sys.exit(1)

    return (conn, cursor)

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
