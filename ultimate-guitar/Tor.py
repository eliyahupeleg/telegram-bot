import json
import os
import socket
import time
import urllib.request

import requests
import socks

socks.setdefaultproxy(proxy_type=socks.PROXY_TYPE_SOCKS5, addr="127.0.0.1", port=9050)

socket.socket = socks.socksocket

i = 0
while i <= 5:
    try:
        os.system("sudo service tor restart")
        time.sleep(10)
        ip = requests.get("http://icanhazip.com").text

        ipaddress = ip.encode('ascii', 'ignore').strip("\n")
        print(ipaddress)

        url = "http://ipinfo.io/" + ipaddress + "/json"
        print(url)
        response = urllib.request.urlopen(url)
        data = json.load(response)
        org = data['org']
        city = data['city']
        country = data['country']
        region = data['region']
        location = data['loc']

        print('Your IP detail')
        print(
            'IP : {4} \nRegion : {1} \nCountry : {2} \nCity : {3} \nService Provider : {0} \nLatitude,Longitude : {5}'.format(
                org, region, country, city, ip, location))
        print('\n##############################################\n')
        i = i + 1
    except Exception as e:
        print(e)
