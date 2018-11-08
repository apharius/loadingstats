all: updatestats threadgraphs

updatestats:
	python3 loadingscraper.py

FORCE: ;

loadingstats.csv:
	python3 loadingscraper.py

topp_15_tradar_utan_bsl.png tradar_per_datum.png tradar_per_anvandare.png tradar_per_timme.png: loadingstats.csv
	Rscript graphs.r

threadgraphs: tradar_per_datum.png tradar_per_anvandare.png tradar_per_timme.png topp_15_tradar_utan_bsl.png


