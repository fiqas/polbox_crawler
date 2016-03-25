import sys
import requests
import multiprocessing as mp
from random import randint
import os
import re
from bs4 import BeautifulSoup
import time
import socket

# proxies = sys.argv[1].readlines()
links = [link.strip() for link in sys.stdin.readlines()]

with open(sys.argv[1]) as f:
    proxies = f.readlines()

def crawl_page(url):
    nice_url = re.search("((http://)?(www.)?polbox.com.+)", url) 
    if nice_url is None:
        print(url)
        return 0
    full_path = "DATA/" + nice_url.group(1).replace("/", "_")
    if os.path.isfile(full_path):
        print("File exists!", file = sys.stderr)
        return 0
    retry = 0
    while retry < 2:
        r = None
        try:
            proxy_https = proxies[randint(0, len(proxies) - 1)]
            proxy_dict = {"https" : proxy_https}
            r = requests.get(url, proxies = proxy_dict, timeout = 20.0)
            r.raise_for_status()
            data = clean_page(r.text)
            save_page(nice_url.group(1), data)
            print("TAK!", url)
            sys.stdout.flush()
            return 0
        except requests.exceptions.RequestException as s:
            if r is not None and str(r.status_code)[0] == "4":
                return 0
            # print("NIE UDALO SIE", s, file = sys.stderr)
            retry += 1
            if retry == 2:
                # print(url, file = sys.stderr)
                print("NIE!", url)
                sys.stdout.flush()
            time.sleep(retry)
        except socket.timeout as s:
            # print("NIE UDALO SIE", s, file = sys.stderr)
            retry += 1
            if retry == 2:
                # print(url, file = sys.stderr)
                print("NIE!", url)
                sys.stdout.flush()
            time.sleep(retry)

def clean_page(content):
    no_archive = re.sub("<!-- BEGIN WAYBACK TOOLBAR INSERT -->.*<!-- END WAYBACK TOOLBAR INSERT -->", "", content, flags=re.DOTALL)
    return no_archive

def save_page(url, content):
    full_path = "DATA/" + url.replace("/", "_")
    with open(full_path, 'w') as content_f:
        content_f.write(content)



processes = 30
pool = mp.Pool(processes = processes)
pool.map(crawl_page, links)
# pool.close()
# pool.join()

