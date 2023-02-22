import threading
import socket
import queue
import time
import requests

proxyQueue = queue.Queue()
validProxy = []

with open("Proxy_List.txt", "r") as f:
    proxies = f.read().splitlines()
    for proxy2 in proxies:
        proxyQueue.put(proxy2)


def Check_Proxy():
    global proxyQueue
    while not proxyQueue.empty():
        proxy1 = proxyQueue.get()
        try:
            response = requests.get("http://ipinfo.io/json",
                                    proxies={"http": proxy1,
                                             "https": proxy1})
        except:
            continue

        if response.status_code == 200:
            print(proxy1)


for _ in range(10):
    threading.Thread(target=Check_Proxy).start()
