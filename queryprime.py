#!/usr/bin/env python3

import configparser
from pprint import pprint
import json

import requests
import argparse


def api_request(path, config):
    url = 'https://' + config.get('PRIME', 'API_HOST') + path
    out = dict()
    r = requests.get(
        url,
        verify=False,
        auth=(config.get('PRIME', 'API_USER'), config.get('PRIME', 'API_PASSWORD')))
    try:
        out['json_response'] = r.json()
    except ValueError:
        out['error'] = 'An error occured. Please check back again later.'
        out['error_detail'] = 'Unexpected response from controller. Not json!'
    return out

def main():
    config = configparser.ConfigParser()
    config.read('config.ini')
    host = config.get('PRIME', 'API_HOST')
    
    ap_data = api_request('/webacs/api/v2/data/AccessPoints.json?.full=true&.maxResults=1000',
                          config)['json_response']['queryResponse']['entity']
    
    dump_data = [{"mac": ap['accessPointsDTO']['macAddress'],
                  "name": ap['accessPointsDTO']['name'],
                  "location": ap['accessPointsDTO']['location'],
                  "clients": ap['accessPointsDTO']['clientCount'],
                  "clients2.4": ap['accessPointsDTO']['clientCount_2_4GHz'],
                  "clients5": ap['accessPointsDTO']['clientCount_5GHz'],
                 } for ap in ap_data]
    dump_data.sort(key=lambda d: d['name'])
    
    print(json.dumps(dump_data))
        

if __name__ == '__main__':
    main()