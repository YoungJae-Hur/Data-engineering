import sys
import requests
import base64
import json
import logging
import time
import pymysql
from aws_credential import getDataBase, getPassword, getPort, getUserName, getHost
from spotify_credential import get_ClientSecret

client_id = "3c13c0645e2c4362a9dd432816c374e1"
client_secret = get_ClientSecret()

def main():
    # 1. Connect pymysql  with AWS RDS
    try:
        connection = pymysql.connect(
            host=getHost(),
            user=getUserName(),
            password=getPassword(),
            database=getDataBase(),
            port=getPort(),
            use_unicode=True,
            charset='utf8'
        )
        cursor = connection.cursor()
    except:
        logging.error("AWS RDS connection failed...")
        sys.exit(1) # 1 meaning no success, 0 meaning success

    # use cursor for queries
    # cursor.execute("SHOW TABLES")
    # print(cursor.fetchall())

    # query = "INSERT INTO artist_genres (artist_id, genre) VALUES ('{}', '{}')".format('2345', 'hip-hop')
    # cursor.execute(query)
    # connection.commit() # to see it directly
    # sys.exit(0)


    header = get_headers(client_id, client_secret)

    # Spotify SearchAPI params
    params = {
        "q": "BTS",        # etc, SG Wannabe
        "type": "artist",
        "limit": "1"       # number of results
    }

    # 2. Send a request for search
    r = requests.get("https://api.spotify.com/v1/search", params=params, headers=header)
    raw = json.loads(r.text)
    # print("raw: ", raw['artists'].keys())
    # print("keys under the level of artists: ", raw['artists']['items'])

    artist_raw = raw['artists']['items'][0]
    if artist_raw['name'] == params['q']:
        artist = {
            'id': artist_raw['id'],
            'name': artist_raw['name'],
            'followers': artist_raw['followers']['total'],
            'popularity': artist_raw['popularity'],
            'url': artist_raw['external_urls']['spotify'],
            'image_url': artist_raw['images'][0]['url'],
        }
        print("1. artist data: ", artist)

        query = """
            INSERT INTO artists (id, name, followers, popularity, url, image_url)
            VALUES ('{}', '{}', {}, {}, '{}', '{}')
            ON DUPLICATE KEY UPDATE id='{}', name='{}', followers={}, popularity={}, url='{}', image_url='{}'
        """.format(
            artist['id'],
            artist['name'],
            artist['followers'],
            artist['popularity'],
            artist['url'],
            artist['image_url'],
            artist['id'],
            artist['name'],
            artist['followers'],
            artist['popularity'],
            artist['url'],
            artist['image_url'],
        )
        cursor.execute(query)
        connection.commit()
        sys.exit(0)


    try:
        r = requests.get("https://api.spotify.com/v1/search", params=params, headers=header)
    except:
        logging.error(r.text)
        sys.exit(1)
    logging.info("Successfully done for search")

    # 3. Check for the error handling
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

    # 4. get BTS albums
    r = requests.get("https://api.spotify.com/v1/artists/3Nrfpe0tUJi4K4DXYWgMUX/albums", headers=header)
    raw_data = json.loads(r.text)

    total = raw_data["total"]
    offset = raw_data["offset"]
    limit = raw_data["limit"]
    next = raw_data["next"]

    albums = []
    albums.extend(raw_data["items"])

    # 5. returns only 100 or less albums (pagination handlling)
    cnt = 0
    while cnt < 100 and next:
        r = requests.get(raw_data["next"], headers=header)
        raw_data = json.loads(r.text)
        next = raw_data["next"]

        albums.extend(raw_data["items"])
        cnt = len(albums)
    # print("Length of album is : ", len(albums))

 






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
