##
# de-x.py -- delete all your tweets w/o API access
# Copyright 2023 Thorsten Schroeder
#
# Published under 2-Clause BSD License (https://opensource.org/license/bsd-2-clause/)
#
# Please see README.md for more information
##

import sys
import json
import requests

def get_tweet_ids(json_data):

    result = []
    data = json.loads(json_data)

    for d in data:
        result.append(d['tweet']['id_str'])

    return result

def parse_req_headers(request_file):

    sess = {}

    with open(request_file) as f:
        line = f.readline()
        while line:
            try:
                k,v = line.split(':', 1)
                val = v.lstrip().rstrip()
                sess[k] = val
            except:
                # ignore empty lines
                pass

            line = f.readline()

    return sess

def main(ac, av):

    if(ac != 3):
        print(f"[!] usage: {av[0]} <jsonfile> <req-headers>")
        return

    f = open(av[1], encoding='UTF-8')
    raw = f.read()
    f.close()

    # skip data until first '['
    i = raw.find('[')
    ids = get_tweet_ids(raw[i:])

    session = parse_req_headers(av[2])

    for i in ids:
        delete_tweet(session, i)
        # maybe add some random sleep here to prevent future rate-limiting


def delete_tweet(session, tweet_id):

    print(f"[*] delete tweet-id {tweet_id}")
    delete_url = "https://twitter.com/i/api/graphql/VaenaVgh5q5ih7kvyVjgtg/DeleteTweet"
    data = {"variables":{"tweet_id":tweet_id,"dark_request":False},"queryId":"VaenaVgh5q5ih7kvyVjgtg"}

    # set or re-set correct content-type header
    session["content-type"] = 'application/json'
    r = requests.post(delete_url, data=json.dumps(data), headers=session)
    print(r.status_code, r.reason)
    print(r.text[:500] + '...')

    return


if __name__ == '__main__':

    main(len(sys.argv), sys.argv)
