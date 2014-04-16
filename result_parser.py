import os
import argparse
import hr_netsec_metrics as metrics
from collections import defaultdict

def parse_args():
	parser = argparse.ArgumentParser(description=\
		'NetSec project data results parser.')
	parser.add_argument('directory', metavar='<directory>', \
		help='Results directory', type=str)
	parser.add_argument('-s', '--site',\
	 choices=['all', 'bmn', 'pwd7', 'login2me', 'fakeaccount', 'loginz'],
	 default='all', help='Pick a site (defaults to all)')
	parser.add_argument('-c', '--categories',\
	 default=None, help='Categories CSV file', type=str)
	parser.add_argument('--alexa', metavar='alexa',\
	 default=None, help='Alexa top 1000 CSV file', type=str)
	return parser.parse_args()

# Parse out which files we want
def result_files(directory, site):
	files = [str(directory) + f for f in os.listdir(directory) if "txt" in f]
	if site is 'all':
		return sorted(files)
	else:
		return sorted([z for z in files if site in z])

# Get data from the files
def get_result_set(directory, site):
	rsets = defaultdict(list)
	files = result_files(directory, site)
	for f in files:
		with open(f, 'r') as f2:
			for line in f2:
				if line.strip():
					data = line.split(',')
					rsets[f].append([item.strip() for item in data])
			f2.close()
	# { password sharing site file : [list of credentials] }
	return rsets

def main(directory, site, categories_csv=None, alexa_csv=None):
	rsets = get_result_set(directory, site)
	print "##### Total per site #####"
	#metrics.total_results(rsets)
	print "##### Total unique results per site #####"
	#metrics.total_site_results_nodup(rsets)[0]
	print "##### Total unique accounts #####"
	#metrics.total_unique_results(rsets)[0]
	print "##### Most popular sites #####"
	#metrics.most_popular_sites(rsets, limit=10)
	print "##### Alexa results by site #####"
	#metrics.alexa_results_by_site(rsets, alexa_csv)
	print "##### Accounts with profanity #####"
	#metrics.profane_accounts(rsets)
	print "##### Change over time #####"
	#metrics.change_over_time(rsets)
	print "##### Most voted on sites #####"
	#metrics.most_voted_sites(rsets)
	#print "##### Highest vote to success percentage ratio #####"
	#metrics.highest_vote_perc_ratio(rsets)
	print "##### Non-formed accounts #####"
	#metrics.non_formed_accounts(rsets)
	if categories_csv:
		print "##### Popular sites (countries, overall, by # sites) #####"
		#metrics.ov_most_popular_countries_sites(rsets, categories_csv)
		print "##### Popular sites (countries, overall, by # accounts) #####"
		#metrics.ov_most_popular_countries_accs(rsets, categories_csv)
		print "##### Popular sites (countries, per site, by # sites) #####"
		#metrics.site_most_popular_countries_sites(rsets, categories_csv)
		print "##### Popular sites (countries, per site, by # accounts) #####"
		#metrics.site_most_popular_countries_accs(rsets, categories_csv)
		print "##### Popular sites (categories, overall, by # sites) #####"
		#metrics.ov_most_popular_categories_sites(rsets, categories_csv)
		print "##### Popular sites (categories, overall, by # accounts) #####"
		#metrics.ov_most_popular_categories_accs(rsets, categories_csv)
		print "##### Popular sites (categories, per site, by # sites) #####"
		metrics.site_most_popular_categories_accs(rsets, categories_csv)
		print "##### Popular sites (categories, per site, by # accounts) #####"
		metrics.site_most_popular_categories_accs(rsets, categories_csv)
		#metrics.popular_sites_by_country(rsets, categories_csv)
		#metrics.popular_sites_by_category(rsets, categories_csv)
		#metrics.popular_sites_by_category2(rsets, categories_csv)

if __name__ == '__main__':
	args = parse_args()
	main(args.directory, args.site, args.categories, args.alexa)