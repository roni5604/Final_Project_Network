import requests
import threading
import queue
import time
import socket
import json

with open("ValidProxyList.txt", "r") as f:
    proxies = f.read().splitlines()

sites_to_check = ["http://ipinfo.io/json", "http://httpbin.org/ip"]

counter = 0
for site in sites_to_check:
    try:
        print(f"Using the proxy: {proxies[counter]}")
        response = requests.get(site, proxies={"http": proxies[counter],"https": proxies[counter]})
        print(response.status_code)
        print(response.text)
    except:
        print("Error")
    finally:
        counter += 1
        counter %= len(proxies) # This is to make sure that the counter doesn't go out of range