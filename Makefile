all: updatestats publishgraphs

updatestats:
	python3 loadingscraper.py

FORCE: ;

loadingstats.csv:
	python3 loadingscraper.py

tradar_per_datum.png tradar_per_anvandare.png tradar_per_timme.png: loadingstats.csv
	Rscript graphs.r

threadgraphs: tradar_per_datum.png tradar_per_anvandare.png tradar_per_timme.png

publishgraphs: threadgraphs
	mv *.png /var/www/html/loading-graphs/
