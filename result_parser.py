import os
import argparse
import netsec_metrics as metrics
from collections import defaultdict

# easy arg parser
def parse_args():
	parser = argparse.ArgumentParser(description=\
		'NetSec project data results parser.')
	parser.add_argument('directory', metavar='<directory>', \
		help='Results directory', type=str)
	parser.add_argument('-s', '--site',\
	 choices=['all', 'bmn', 'pwd7', 'login2me', 'fakeaccount', 'loginz'],
	 default='all', help='Pick a site (defaults to all)')
	return parser.parse_args()

# Parse out which files we want
def result_files(directory, site):
	files = [str(directory) + f for f in os.listdir(directory) if "txt" in f]
	if site is 'all':
		return sorted(files)
	else:
		return sorted([z for z in files if site in z])

def main(directory, site):
	totals = []
	webset = set()
	files = result_files(directory, site)
	for f in files:
		with open(f, 'r') as f2:
			site = f.split('_')[0]
			for line in f2:
				if line.strip():
					data = line.split(',')
					rsets[f].append([item.strip() for item in data])

	print "##### Total per site #####"
	metrics.total_results(rsets)
	print "##### Total unique results per site #####"
	metrics.total_site_results_nodup(rsets)
	print "##### Total unique accounts #####"
	metrics.total_unique_results(rsets)
	print "##### Most popular sites #####"
	metrics.most_popular_sites(rsets, limit=10)
	print "##### Alexa results by site #####"
	metrics.alexa_results_by_site(rsets)
	print "##### Accounts with profanity #####"
	metrics.profane_accounts(rsets, profanities=['fuck'])
	print "##### Change over time, by site #####"
	metrics.change_over_time(rsets)

	"""
	bmn_set = rsets[3][1].difference(rsets[2][1])
	print "bmn change:", len(bmn_set)

	loginz_set = rsets[14][1].difference(rsets[15][1])
	print "loginz change:", len(loginz_set)
	"""

if __name__ == '__main__':
	args = parse_args()
	main(args.directory, args.site)