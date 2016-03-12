import sys
from bs4 import BeautifulSoup, SoupStrainer

# td_urls = SoupStrainer('td', {'class':'url'})
# soup = BeautifulSoup(sys.stdin.read(), parse_only = td_urls)

soup = BeautifulSoup(sys.stdin.read())
print("Found all links", file = sys.stderr)

# with open(sys.argv[1], 'w') as parsed_f:
    # parsed_f.write(soup.prettify())

for a in soup.findAll('a', href = True):
    url = a['href']
    url = url.replace("/*/", "/2002/")
    print("http://web.archive.org" + url)
