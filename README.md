# polbox_crawler

Projekt zaliczeniowy na Inteligentne Systemy Informacyjne 2016
Cel: zcrawlować nieistniejący serwis www.polbox.com przez archive.org.

Zarys etapów do zrealizowania:

1) Wyciągnięcie listy linków do zcrawlowania - ZROBIONE.

Przez aria2c ściągnęłam stronę (links.html), zawierającą wszystkie linki wylistowane na serwisie archive.org.
Skryptem extract_links.py wyciągnęłam i zparsowałam linki do pełnej postaci (links.txt).
Jeżeli istnieje tylko 1 wersja linku na archive.org, to jest on w pełni rozwinięty.
Jeżeli istnieje kilka, to bierze najbliższej zarejestrowany link w stosunku do 2002 roku (archive.org samo przekieruje do odpowiedniego capture).

2) Odsianie linków:
	a) usunięcie ewidentnych obrazków itp.
	b) usunięcie linków nieaktywnych/nieistniejących (?)
3) Zdobycie listy proxy, przez które linki będą crawlowane.
4) Zrobienie listy komend aria2c do crawlowania poszczególnych stron.
5) Zcrawlowanie całego polbox.com
