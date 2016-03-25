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

with open(sys.argv[2]) as g:
    downloaded = [x.strip() for x in g.readlines()]
    downloaded = set(downloaded)

links = [link for link in links if link not in downloaded]

def crawl_page(url):
    # print(url, url in downloaded, file = sys.stderr)
    if url in downloaded:
        return 0
    nice_url = re.search("((http://)?(www.)?polbox.com.+)", url) 
    if nice_url is None:
        print(url)
        return 0
    else:
        splitted = nice_url.group(1).strip("http://").split("/")
        filename = splitted[-1]
        if len(filename) < 1:
            filename = "index.html"
        path = "DATA/" + "/".join(splitted[1:-1])

    retry = 0
    while retry < 2:
        try:
            proxy_https = proxies[randint(0, len(proxies) - 1)]
            proxy_dict = {"https" : proxy_https}
            r = requests.get(url, proxies = proxy_dict, timeout = 20.0)
            r.raise_for_status()
            data = clean_page(r.text)
            save_page(nice_url.group(1), path, filename, data)
            print(url)
            sys.stdout.flush()
            return 0
        except requests.exceptions.RequestException as s:
            # print("NIE UDALO SIE", s, file = sys.stderr)
            retry += 1
            if retry == 2:
                # print(url, file = sys.stderr)
                print(url)
                sys.stdout.flush()
            time.sleep(retry)
        except socket.timeout as s:
            # print("NIE UDALO SIE", s, file = sys.stderr)
            retry += 1
            if retry == 2:
                # print(url, file = sys.stderr)
                print(url)
                sys.stdout.flush()
            time.sleep(retry)

def clean_page(content):
    no_archive = re.sub("<!-- BEGIN WAYBACK TOOLBAR INSERT -->.*<!-- END WAYBACK TOOLBAR INSERT -->", "", content, flags=re.DOTALL)
    return no_archive

def save_page(url, path, filename, content):
    full_path = "DATA/" + url.replace("/", "_")
    # print(full_path, file = sys.stderr)
    with open(full_path, 'w') as content_f:
        content_f.write(content)



processes = 30
pool = mp.Pool(processes = processes)
pool.map(crawl_page, links)
# pool.close()
# pool.join()

