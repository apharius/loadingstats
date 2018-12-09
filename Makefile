all: updatestats publishgraphs publishstats

updatestats:
	python3 loadingscraper.py

FORCE: ;

threads.csv posts.csv:
	python3 loadingscraper.py

topp_15_tradar_utan_bsl.png tradar_per_datum.png tradar_per_anvandare.png tradar_per_timme.png: threads.csv
	Rscript graphs.r

inlagg_per_anvandare.png inlagg_per_timme.png inlagg_per_datum.png: posts.csv

threadgraphs: tradar_per_datum.png tradar_per_anvandare.png tradar_per_timme.png topp_15_tradar_utan_bsl.png

postgraphs: inlagg_per_anvandare.png inlagg_per_timme.png inlagg_per_datum.png

publishgraphs: threadgraphs postgraphs
	mv *.png /var/www/html/loading-graphs/

publishstats: threads.csv posts.csv
	mv *.csv /var/www/html/loading-graphs/
