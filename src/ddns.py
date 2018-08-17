import yaml
import json
import time
import pycurl
import argparse
import requests
import logging as log

from StringIO import StringIO

current_ip = ""
config = None
api_url = "https://api.godaddy.com/v1/domains/"
records_path = "{}{}/records/A/{}"
api_headers = ""

def set_ip_if_needed():
    global current_ip
    my_ip = get_my_ip()
    log.info("Current IP: %s", my_ip)
    log.info("Current stored IP: %s", current_ip)

    if current_ip != my_ip:
        dns_ip = get_host_ip()
        log.info("DNS IP: %s", dns_ip)
        if my_ip != dns_ip:
            log.info("IP changed; setting host IP to: %s", my_ip)
            set_host_ip(my_ip)
        log.info("Updating current_ip")
        current_ip = my_ip

def get_my_ip():
    return json.loads(requests.get('https://api.ipify.org?format=json').text)['ip']
            
def get_host_ip():
    url = records_path.format(api_url, config['domain'], config['host'])
    response = json.loads(requests.get(url, headers=api_headers).text)
    if(len(response) == 0):
        raise HostNotFound("No host returned from API")
    return response[0]['data']
    
def set_host_ip(ip):
    url = "{}{}/records/A/{}".format(api_url, config['domain'], config['host'])
    response = requests.put(url, json=[{ 'data': ip, 'ttl': 3600 }], headers=api_headers)
    log.info("Set host IP returned: %s", response.status_code)

#### Main / Startup functions ####

def configure():
    parser = argparse.ArgumentParser()
    parser.add_argument('config_file', help='Path to the configuration file.')
    args = parser.parse_args()
    return args

def main():
    global config, api_headers
    args = configure()
    config = yaml.load(open(args.config_file, 'r'))
    log.basicConfig(format='%(asctime)-15s **%(levelname)s** %(message)s', level=log.INFO)
    
    api_headers = { 'Authorization' : "sso-key {}:{}".format(config['key'], config['secret']) }
    while True:
        set_ip_if_needed()
        time.sleep(config['refresh'])

if __name__ == "__main__":
    main()
