# polbox_crawler

Projekt zaliczeniowy na Inteligentne Systemy Informacyjne 2016

Cel: zcrawlować nieistniejący serwis www.polbox.com przez archive.org.
Efekt: skrypt do crawlowania całych domen z archive.org.

Skrypty:
a) extract_links.py - parsuje listę wszystkich linków domeny ze strony archive.org
b) crawl_archive.py - crawluje domenę na podstawie listy linków

Crawlowanie dowolnego serwisu z archive.org na podstawie polbox.com:

1) Ściągamy wgetem stronę ze wszystkimi linkami domeny np.

wget https://web.archive.org/web/*/polbox.com/* links.html

2) Parsujemy listę linków z pliku html skryptem extract_links.py:
Może to trwać trochę przy dużej ilości linków, dlatego skrypt jest osobno.

python3 extract_links.py < links.html > links.txt

3) Tworzymy szybko listę proxy:

	a) Wchodzimy na HideMyAss:
	http://proxylist.hidemyass.com/
	b) Kopiujemy dużą listę proxy HTTPS do schowka (po prostu zaznaczamy i kopiujemy wszystko, jak leci).
	c) Filtrujemy listę proxy przez stronę:
	http://www.checker.freeproxy.ru/filter_lite/
	d) Zapisujemy do proxies.txt.

4) Zaczynamy crawling całej domeny.

python3 crawl_archive.py -p proxies.txt -d polbox.com -o DATA2/ -l links.txt -m 30 2002 1998 2005

-p = plik z listą proxy HTTPS

-d = domena do ściągnięcia ('esencja', bez http, www itp.)

-o = katalog, do którego wszystkie zcrawlowane strony mają trafić

-l = plik z listą sparsowanych linków

-m = ilość ściąganych linków naraz (ilość procesów w multiprocessing Pool)

Wyrazy wolne tworzą listę roczników, które zostaną zcrawlowane. KOLEJNOŚĆ MA ZNACZENIE. Najpierw zostaną zcrawlowane strony wg rocznika 2002, następnie, jeżeli strona nie została ściągnięta w roczniku 2002, a będzie istniała w 1998, to zostanie docrawlowana. 

Jak crawluje skrypt crawl_archive.py:

1) Odfiltruj linki z nieinteresujących nas plików.
2) Weź link np.

http://web.archive.org/web/*/http://www.polbox.com:80/

3) Podmień /*/ na interesujący nas rocznik.

http://web.archive.org/web/2002/http://www.polbox.com:80/

4) Jeżeli istnieje plik danego linku, to uznajemy, że strona została już ściągnięta - przerywamy.

5) Jeżeli nie istnieje plik, podejmij 3 próby ściągnięcia strony.
Jeżeli ściągnięcie się nie udało, losuj nowe proxy, 
zrób przerwę 1-3 sekundową i ponów próbę. 
Jeżeli zwracany status code jest typu "400", przerwij (strona nie istnieje).
Po 3 próbach, przerwij.

6) Wyciągnij metadane i w zależności, czy link prowadzi do strony czy pliku, dodaj dane do pliku files.tsv/pages.tsv.

Metadane składają się z:
link nazwa_pliku bajty rok miesiąc dzień godzina minuty sekundy

7) Zapisz ściągnięty link do pliku (nazwa to link z "_" zamiast "/"):

	a) Jeżeli jest to strona, to usuń toolbar Archive.org i zapisz wersję tekstową.


	b) Jeżeli jest to plik, to zapisz wersję binarną.

Powyższa metoda jest stosowana dla wszystkich linków dla wszystkich roczników podanych w parametrach. Z każdym kolejnym rocznikiem, jest coraz mniej linków do docrawlowania:
2002 - większość, 1998, pareset/tysiąc coś, 2005 - 2 strony

Teoretycznie program został dostowowany do crawlowania dowolnej domeny z archive.org.

