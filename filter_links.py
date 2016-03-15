import sys

banned = (".jpg", ".png", ".gif", ".mp3")

for url in sys.stdin:
    url_lc = url.lower().strip()
    if url_lc.endswith(banned):
        continue
    else:
        print(url_lc)
