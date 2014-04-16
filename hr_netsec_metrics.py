""" Metrics common to each site
Prints out in human-readable format """
from collections import defaultdict, Counter

def common_name(site):
	if 'bmn' in site:
		return "BugMeNot"
	elif 'fakeaccount' in site:
		return "FakeAccount"
	elif 'login2me' in site:
		return "Login2Me"
	elif 'loginz' in site:
		return "Loginz"
	elif 'pwd7' in site:
		return "Password7"
	else:
		return site

# Number of credentials scraped total (non-unique)
def total_results(rset, writeout=True):
	ret_dict = defaultdict(int)
	for result in rset:
		ret_dict[common_name(result)] += len(rset[result])
	if writeout:
		for ret in sorted(ret_dict.items()):
			print '{0: <17} {1}'.format(ret[0], ret[1])
		print "{0: <17} {1}".format("TOTAL:", sum(ret_dict.values()))
	return ret_dict

# Unique credentials per site
def total_site_results_nodup(rset, writeout=True):
	ret_dict = defaultdict(set)
	bad_accounts = defaultdict(int)
	for result in rset:
		for site in rset[result]:
			try:
				ret_dict[common_name(result)]\
				.add((site[0], site[1], site[2]))
			# improper data
			except IndexError, e:
				bad_accounts[common_name(result)] += 1
	if writeout:
		for ret in sorted(ret_dict.items()):
			print '{0: <17} {1}'.format(ret[0], len(ret[1]))
		print "{0: <17} {1}".format("TOTAL:", \
			sum([len(s) for s in ret_dict.values()]))
	return (ret_dict, bad_accounts)

# Unique credentials across all sites
def total_unique_results(rset, writeout=True):
	ret_set = set()
	bad_accounts = defaultdict(int)
	for result in rset:
		for site in rset[result]:
			try:
				ret_set.add((site[0], site[1], site[2]))
			# improper data
			except IndexError, e:
				bad_accounts[common_name(result)] += 1
	if writeout:
		print '{0: <17} {1}'.format('TOTAL ACCOUNTS:', len(ret_set))
	return (ret_set, bad_accounts)

# Most @limit popular sites
def most_popular_sites(rset, writeout=True, limit=10):
	ret_dict = defaultdict(int)
	reduce_sites = total_site_results_nodup(rset, writeout=False)[0]
	for key in reduce_sites.keys():
		for site in reduce_sites[key]:
			ret_dict[site[0]] += 1
	if writeout:
		print '{0: <17} {1}'.format("SITE", "RESULTS")
		for ret in sorted(ret_dict.items(), key=lambda x : x[1],\
		 reverse=True)[:limit]:
			print '{0: <17} {1}'.format(ret[0], ret[1])
	return ret_dict

# Number of the Alexa top 1000 per site
def alexa_results_by_site(rset, alexa_csv, writeout=True):
	ret_dict = defaultdict(set)
	alexa_set = set()
	with open(alexa_csv, 'r') as f:
		for line in f:
			alexa_set.add(line.split(',')[1].strip())
	for result in rset:
		for site in rset[result]:
			if site[0] and site[0] in alexa_set:
				ret_dict[common_name(result)].add(site[0])
	if writeout:
		total_sites = set()
		for ret in sorted(ret_dict.items()):
			print '{0: <17} {1}'.format(common_name(ret[0]), len(ret[1]))
			total_sites |= ret[1]
		print "{0: <17} {1}".format("TOTAL SITES:", len(total_sites))
	return ret_dict

# Account credentials with some form of Englush profanity
def profane_accounts(rset, writeout=True, profanities=['fuck', 'shit', \
	'damn', 'bitch', 'crap', 'piss', 'dick', 'cock', 'pussy', 'asshole',\
	'fag', 'bastard', 'slut']):
	prof_user, prof_pass = 0, 0
	reduce_sites = total_unique_results(rset, writeout=False)[0]
	#with open("bad-words.txt") as f:
	#	for l in f:
	#		if l and '#' not in l:
	#			profanities.append(l)
	#	f.close()
	for site in reduce_sites:
		for p in profanities:
			try:
				if p in site[1].lower():
					prof_user += 1
				elif p in site[2].lower():
					prof_pass += 1
			# improper data
			except IndexError, e:
				pass
	print '{0: <17} {1}'.format("Usernames:", prof_user)
	print '{0: <17} {1}'.format("Passwords:", prof_pass)
	return (prof_user, prof_pass)

# Helper function to change_over_time (MAY BE ONLY 95% ACCURATE)
def _delta_over_t(rlist, writeout, site):
	ret_list = []
	if writeout: print common_name(site)
	for i in range(0, len(rlist) - 1): # avoid index error
		sdate = rlist[i][0].split('_')[2]
		edate = rlist[i+1][0].split('_')[2]
		start_r, end_r = set(), set()
		try:
			for j in rlist[i+1][1]:
				rstr = j[:3]
				if len(rstr) < 3: rstr.append("#None#")
				end_r.add(",".join(rstr)[:-1])
			for k in rlist[i][1]:
				rstr = k[:3]
				if len(rstr) < 3: rstr.append("#None#")
				start_r.add(",".join(rstr)[:-1])
		# improper data
		except IndexError, e:
			pass
		if writeout:
			print "{0: <10} --> {1: <10} {2: >5}"\
			.format(sdate, edate, len(end_r - start_r))
		ret_list.append((sdate, edate, len(end_r - start_r)))
	return ret_list

# Change in new credentials over time
def change_over_time(rset, writeout=True):
	bmn, fa, l2m, lgz, pwd7 = [], [], [], [], []
	for result in rset.items():
		if 'bmn' in result[0]:
			bmn.append((result[0], result[1]))
		elif 'fakeaccount' in result[0]:
			fa.append((result[0], result[1]))
		elif 'login2me' in result[0]:
			l2m.append((result[0], result[1]))
		elif 'loginz' in result[0]:
			lgz.append((result[0], result[1]))
		elif 'pwd7' in result[0]:
			pwd7.append((result[0], result[1]))

	_delta_over_t(sorted(bmn), writeout, 'bmn')
	_delta_over_t(sorted(fa), writeout, 'fakeaccount')
	_delta_over_t(sorted(l2m), writeout, 'login2me')
	_delta_over_t(sorted(lgz), writeout, 'loginz')
	_delta_over_t(sorted(pwd7), writeout, 'pwd7')

# @limit sites with most votes (BMN, FA, Pwd7 only)
def most_voted_sites(rset, writeout=True, limit=10):
	ret_dict = defaultdict(int)
	perc_dict = defaultdict(int)
	for result in rset.items():
		if not "login2me" in result[0] and \
		not "loginz" in result[0]:
			for r in result[1]:
				if "bmn" in result[0]:
					vote_str = r[-2]
				else:
					vote_str = r[-1]
				if "votes" in vote_str:
					ret_dict[r[0]] += int(vote_str.split('votes')[0])
					if "bmn" in result[0]:
						perc_dict['bmn'] += int(vote_str.split('votes')[0])
					elif "fakeaccount" in result[0]:
						perc_dict['fakeaccount'] += \
						int(vote_str.split('votes')[0])
					elif "pwd7" in result[0]:
						perc_dict['pwd7'] += int(vote_str.split('votes')[0])
	if writeout:
		print '{0: <17} {1}'.format("SITE", "RESULTS")
		for ret in sorted(ret_dict.items(), key=lambda x : x[1],\
		 reverse=True)[:limit]:
			print '{0: <17} {1}'.format(ret[0], ret[1])
		print '\n',
		for s in perc_dict.items():
			print '{0: <16} {1: 0.2f}%'.format(common_name(s[0]),\
			(float(s[1]) / sum(perc_dict.values())) * 100.0)
		print "{0} votes total".format(sum(perc_dict.values()))

	return ret_dict

# @limit sites with highest votes to success % ratio (BMN, FA, Pwd7 only)
# TODO
def highest_vote_perc_ratio(rset, writeout=True, limit=50):
	vote_dict = defaultdict(list)
	perc_dict = defaultdict(list)
	ret_dict = defaultdict(float)
	for result in rset.items():
		if not "login2me" in result[0] and \
		not "loginz" in result[0]:
			for r in result[1]:
				try:
					if "bmn" in result[0]:
						vote_str = r[-2]
						perc_str = r[-3]
					else:
						vote_str = r[-1]
						perc_str = r[-2]
					if "votes" in vote_str and '%' in perc_str:
						vote_dict[r[0]].append(int(vote_str.split('votes')[0]))
						perc_dict[r[0]].append(int(perc_str.split('%')[0]))
				# improper data
				except IndexError, e:
					pass
	# keys for both should be the same
	for key in vote_dict.keys():
		#print perc_dict[key], vote_dict[key]
		if sum(perc_dict[key]) < 1 and sum(vote_dict[key]) < 1 \
		and len(perc_dict[key]) < 1 and len(vote_dict[key]) < 1:
			ret_dict[key] = 0.0
		else:
			try:
				ret_dict[key] = float(sum(perc_dict[key]) / len(perc_dict[key])) \
				 / float(sum(vote_dict[key]) / len(vote_dict[key]))
			# negligable percentage
			except ZeroDivisionError, e:
				#print key, perc_dict[key], vote_dict[key]
				pass
	for ret in sorted(ret_dict.items(), key=lambda x : x[1],\
		 reverse=True)[:limit]:
			print '{0: <17} {1: 0.2f}'.format(ret[0], ret[1])
	return ret_dict

# Checks for number of non-formed accounts by site
def non_formed_accounts(rset, writeout=True):
	ret_dict = defaultdict(int)
	# quick save of unique accounts/non-formed accounts
	uniq_result = total_site_results_nodup(rset, writeout=False) 
	# check the accounts first
	for site in uniq_result[0]:
		for val in uniq_result[0][site]:
			# user is blank 
			if not val[1].strip():
				ret_dict[site] += 1
			# or user has space in it
			elif ' ' in val[1].strip():
				ret_dict[site] += 1
			# password is blank
			elif not val[2].strip():
				ret_dict[site] += 1
			# my #None# check for BMN
			elif "#None#" in val[1] or "#None#" in val[2]:
				ret_dict[site] += 1
	# add in the non-formed accounts
	for non_formed in uniq_result[1].items():
		ret_dict[non_formed[0]] += non_formed[1]

	if writeout:
		for ret in sorted(ret_dict.items(), key=lambda x : x[1],\
		 reverse=True):
			print '{0: <17} {1}'.format(ret[0], ret[1])
	return ret_dict


# Helper class for site categorization metrics
class site_category:
	def __init__(self, csv):
		csv_spl = csv.split(',')
		self.category = csv_spl[1]
		self.subcategory = csv_spl[2]
		self.region = csv_spl[3]
		self.subregion = csv_spl[4]
	def __repr__(self):
		return list().append(self.category).append(self.subcategory)\
		.append(self.region).append(self.subregion)

# Helper function to read in categories from the file
def _site_cat_dict(cat_file):
	ret_dict = defaultdict(str)
	with open(cat_file, 'r') as f:
		for line in f:
			ret_dict[line.split(',')[0]] = site_category(line)
	return ret_dict

# overall most popular countries, by # of accounts
def ov_most_popular_countries_accs(rset, cat_file, writeout=True):
	ret_dict = defaultdict(int)
	site_dict = _site_cat_dict(cat_file)
	# proceed to read sites
	for site in total_unique_results(rset, writeout=False)[0]:
		# some sites have no region
		if site_dict[site[0]]:
			ret_dict[ site_dict[site[0]].region ] += 1
	if writeout:
		print '{0: <17} {1}'.format("REGION", "# ACCOUNTS")
		for ret in sorted(ret_dict.items(), key=lambda x : x[1],\
		 reverse=True):
			if ret[0]:
				print '{0: <17} {1}'.format(ret[0], ret[1])
			else:
				print '{0: <17} {1}'.format("No region", ret[1])
	print "{0: <17} {1}".format("TOTAL:", sum(ret_dict.values()))
	return ret_dict

# overall most popular countries, by # of accounts for sites in the region
def ov_most_popular_countries_sites(rset, cat_file, writeout=True):
	ret_dict = defaultdict(int)
	site_dict = _site_cat_dict(cat_file)
	uniq_sites = set()
	# get unique sites scraped
	for site in total_unique_results(rset, writeout=False)[0]:
		uniq_sites.add(site[0])
	# then categorize
	for uniq_site in uniq_sites:
		# some sites have no region
		if site_dict[uniq_site]:
			ret_dict[ site_dict[uniq_site].region ] += 1

	if writeout:
		print '{0: <17} {1}'.format("REGION", "# SITES")
		for ret in sorted(ret_dict.items(), key=lambda x : x[1],\
		 reverse=True):
			if ret[0]:
				print '{0: <17} {1}'.format(ret[0], ret[1])
			else:
				print '{0: <17} {1}'.format("No region", ret[1])
	print "{0: <17} {1}".format("TOTAL:", sum(ret_dict.values()))
	return ret_dict

# site's most popular countries, by # of accounts
def site_most_popular_countries_accs(rset, cat_file, writeout=True):
	ret_dict = defaultdict(Counter)
	site_dict = _site_cat_dict(cat_file)
	no_dups = total_site_results_nodup(rset, writeout=False)[0]
	# proceed to read sites
	for pw_site in no_dups:
		for site in no_dups[pw_site]:
			# some sites have no region
			if site_dict[site[0]]:
				# double layer dictionary
				(ret_dict[pw_site])[site_dict[site[0]].region] += 1
	if writeout:
		print '{0: <17} {1}'.format("REGION", "# ACCOUNTS")
		for ret in sorted(ret_dict.items(), key=lambda x : x[1],\
		 reverse=True):
			print ret[0]
			for r in sorted(ret[1].items(), key=lambda y : y[1],\
			 reverse=True):
				if r[0]:
					print '{0: <17} {1}'.format(r[0], r[1])
				else:
					print '{0: <17} {1}'.format("No region", r[1])
			print
	return ret_dict

# site's most popular countries, by # of accounts
def site_most_popular_countries_sites(rset, cat_file, writeout=True):
	ret_dict = defaultdict(Counter)
	site_dict = _site_cat_dict(cat_file)
	uniq_sites = defaultdict(set)
	# get unique sites scraped
	sav_dict = total_site_results_nodup(rset, writeout=False)[0]
	# for each password site (key for dictionary)
	for uniq_dict in sav_dict:
		# for each result site for that site
		for dict_site in sav_dict[uniq_dict]:
			# add it to a set
			uniq_sites[uniq_dict].add(dict_site[0])
	# proceed to read sites
	for pw_site in uniq_sites:
		for site in uniq_sites[pw_site]:
			# some sites have no region
			if site_dict[site]:
				# double layer dictionary
				(ret_dict[pw_site])[site_dict[site].region] += 1
	if writeout:
		print '{0: <17} {1}'.format("REGION", "# SITES")
		for ret in sorted(ret_dict.items(), key=lambda x : x[1],\
		 reverse=True):
			print ret[0]
			for r in sorted(ret[1].items(), key=lambda y : y[1],\
			 reverse=True):
				if r[0]:
					print '{0: <17} {1}'.format(r[0], r[1])
				else:
					print '{0: <17} {1}'.format("No region", r[1])
			print
	return ret_dict

# overall most popular categories, by # of accounts for sites in the region
def ov_most_popular_categories_sites(rset, cat_file, writeout=True):
	ret_dict = defaultdict(int)
	site_dict = _site_cat_dict(cat_file)
	uniq_sites = set()
	# get unique sites scraped
	for site in total_unique_results(rset, writeout=False)[0]:
		uniq_sites.add(site[0])
	# then categorize
	for uniq_site in uniq_sites:
		# some sites have no region
		if site_dict[uniq_site]:
			ret_dict[ site_dict[uniq_site].category ] += 1

	if writeout:
		print '{0: <17} {1}'.format("REGION", "# SITES")
		for ret in sorted(ret_dict.items(), key=lambda x : x[1],\
		 reverse=True):
			if ret[0]:
				print '{0: <17} {1}'.format(ret[0], ret[1])
			else:
				print '{0: <17} {1}'.format("No region", ret[1])
	print "{0: <17} {1}".format("TOTAL:", sum(ret_dict.values()))
	return ret_dict

# overall most popular categories, by # of accounts
def ov_most_popular_categories_accs(rset, cat_file, writeout=True):
	ret_dict = defaultdict(int)
	site_dict = _site_cat_dict(cat_file)
	# proceed to read sites
	for site in total_unique_results(rset, writeout=False)[0]:
		# some sites have no region
		if site_dict[site[0]]:
			ret_dict[ site_dict[site[0]].category ] += 1
	if writeout:
		print '{0: <17} {1}'.format("REGION", "# ACCOUNTS")
		for ret in sorted(ret_dict.items(), key=lambda x : x[1],\
		 reverse=True):
			if ret[0]:
				print '{0: <17} {1}'.format(ret[0], ret[1])
			else:
				print '{0: <17} {1}'.format("No category", ret[1])
	print "{0: <17} {1}".format("TOTAL:", sum(ret_dict.values()))
	return ret_dict

# site's most popular categories, by # of accounts
def site_most_popular_categories_accs(rset, cat_file, writeout=True):
	ret_dict = defaultdict(Counter)
	site_dict = _site_cat_dict(cat_file)
	no_dups = total_site_results_nodup(rset, writeout=False)[0]
	# proceed to read sites
	for pw_site in no_dups:
		for site in no_dups[pw_site]:
			# some sites have no region
			if site_dict[site[0]]:
				# double layer dictionary
				(ret_dict[pw_site])[site_dict[site[0]].category] += 1
	if writeout:
		print '{0: <17} {1}'.format("REGION", "# ACCOUNTS")
		for ret in sorted(ret_dict.items(), key=lambda x : x[1],\
		 reverse=True):
			print ret[0]
			for r in sorted(ret[1].items(), key=lambda y : y[1],\
			 reverse=True):
				if r[0]:
					print '{0: <17} {1}'.format(r[0], r[1])
				else:
					print '{0: <17} {1}'.format("No region", r[1])
			print
	return ret_dict

# site's most popular countries, by # of accounts
def site_most_popular_categories_sites(rset, cat_file, writeout=True):
	ret_dict = defaultdict(Counter)
	site_dict = _site_cat_dict(cat_file)
	uniq_sites = defaultdict(set)
	# get unique sites scraped
	sav_dict = total_site_results_nodup(rset, writeout=False)[0]
	# for each password site (key for dictionary)
	for uniq_dict in sav_dict:
		# for each result site for that site
		for dict_site in sav_dict[uniq_dict]:
			# add it to a set
			uniq_sites[uniq_dict].add(dict_site[0])
	# proceed to read sites
	for pw_site in uniq_sites:
		for site in uniq_sites[pw_site]:
			# some sites have no region
			if site_dict[site]:
				# double layer dictionary
				(ret_dict[pw_site])[site_dict[site].category] += 1
	if writeout:
		print '{0: <17} {1}'.format("REGION", "# SITES")
		for ret in sorted(ret_dict.items(), key=lambda x : x[1],\
		 reverse=True):
			print ret[0]
			for r in sorted(ret[1].items(), key=lambda y : y[1],\
			 reverse=True):
				if r[0]:
					print '{0: <17} {1}'.format(r[0], r[1])
				else:
					print '{0: <17} {1}'.format("No region", r[1])
			print
	return ret_dict
