import sys
import requests
import multiprocessing as mp
from random import randint
import os
import re
from bs4 import BeautifulSoup
import time
import socket
import argparse
import shutil

parser = argparse.ArgumentParser(description='Script to crawl domain archived at archive.org through proxies.')
parser.add_argument("-p", "--proxies", required = True, help = "Path to file with proxies")
parser.add_argument("-d", "--domain", required = True, help = "Main URL without http and www e.g. polbox.com")
parser.add_argument("-o", "--output", required = True, help = "Path to output directory")
parser.add_argument("-l", "--links", required = True, help = "Path to file with links")
parser.add_argument("-m", "--multi", required = True, help = "How many processes in multiprocessing pool")
parser.add_argument('years', nargs='*')
args = parser.parse_args()

print(args)

class ArchiveCrawler:
    def __init__(self):
        self.banned = (".avi", ".css", ".bmp", ".jpg", ".png", ".gif", ".mp3", ".mid", ".mov", ".mpg", ".swf", ".tif", ".wav", ".wma")  
        
        self.load_proxies()
        self.load_links()
        self.filter_links()

        for year in args.years:
            print("Started crawling year:", year, file = sys.stderr)
            self.year = year
            pool = mp.Pool(processes = int(args.multi))
            pool.map(self.crawl_page, self.links)
        


    def load_proxies(self):
        with open(args.proxies) as proxies_f:
            self.proxies = [x.strip() for x in proxies_f.readlines()]


    def load_links(self):
        with open(args.links) as links_f:
            self.links = [x.lower().strip() for x in links_f.readlines()]

    
    def filter_links(self):
        self.links = [link for link in self.links if not link.endswith(self.banned)]

    
    def clean_page(self, content):
        no_archive = re.sub("<!-- BEGIN WAYBACK TOOLBAR INSERT -->.*<!-- END WAYBACK TOOLBAR INSERT -->", "", content, flags=re.DOTALL)
        return no_archive

    
    def save_page_html(self, full_path, content):
        with open(full_path, 'w') as content_f:
            content_f.write(content)
        
    
    def save_page_file(self, full_path, raw):
        with open(full_path, 'wb') as content_f:
            content_f.write(raw)
    

    def save_metadata(self, url, nice_url, length, file_or_page):
        date_regex = "/(\d{14})/"
        crawling_date = re.search(date_regex, url).group(1)
        year = crawling_date[0:4]
        month = crawling_date[4:6]
        day = crawling_date[6:8]
        hour = crawling_date[8:10]
        minute = crawling_date[10:12]
        second = crawling_date[12:]
        file_name = nice_url.replace("/", "_")

        to_save = [nice_url, file_name, str(length), year, month, day, hour, minute, second]

        if file_or_page:
            path = args.output + "files.tsv"
        else:
            path = args.output + "pages.tsv"
        
        with open(path, 'a') as metadata_f:
            metadata_f.write("\t".join(to_save) + "\n")

    
    def crawl_page(self, url):
        regex = "((http://)?(www.)?" + args.domain + ".+)"
        nice_url = re.search(regex, url)

        
        if nice_url is None:
            print(url)
            return 0
        
        url = url.replace("/*/", "/" + self.year + "/")
        full_path = args.output + nice_url.group(1).replace("/", "_")
        
        if os.path.isfile(full_path):
            # print("File exists!", file = sys.stderr)
            return 0

        retry = 0
        while retry < 2:
            r = None
            try:
                proxy_https = self.proxies[randint(0, len(self.proxies) - 1)]
                proxy_dict = {"https" : proxy_https}
                r = requests.get(url, proxies = proxy_dict, timeout = 20.0)
                r.raise_for_status()
                url = r.url

                if "text/html" in r.headers["content-type"]:
                    if "response at crawl time" in r.text:
                        return 0
                    data = self.clean_page(r.text)
                    self.save_page_html(full_path, data)
                    self.save_metadata(url, nice_url.group(1), len(r.content), False)
                    print("TAK!", url)
                    sys.stdout.flush()
                else:
                    self.save_page_file(full_path, r.content)
                    self.save_metadata(url, nice_url.group(1), len(r.content), True)
                    print("TAK!", url)
                    sys.stdout.flush()

                return 0
            except requests.exceptions.RequestException as s:
                if r is not None and str(r.status_code)[0] == "4":
                    return 0
                retry += 1
                if retry == 2:
                    print("NIE!", url)
                    sys.stdout.flush()
                    return 0
                time.sleep(retry)
            except socket.timeout as s:
                # print("NIE UDALO SIE", s, file = sys.stderr)
                retry += 1
                if retry == 2:
                    print("NIE!", url)
                    sys.stdout.flush()
                    return 0
                time.sleep(retry)

    

crawler = ArchiveCrawler()
