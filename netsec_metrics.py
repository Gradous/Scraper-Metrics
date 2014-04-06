""" Metrics common to each site """
from collections import defaultdict
from operator import itemgetter

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
	for result in rset:
		for site in rset[result]:
			try:
				ret_dict[common_name(result)]\
				.add((site[0], site[1], site[2]))
			# improper data
			except IndexError, e:
				pass
	if writeout:
		for ret in sorted(ret_dict.items()):
			print '{0: <17} {1}'.format(ret[0], len(ret[1]))
		print "{0: <17} {1}".format("TOTAL:", \
			sum([len(s) for s in ret_dict.values()]))
	return ret_dict

# Unique credentials across all sites
def total_unique_results(rset, writeout=True):
	ret_set = set()
	for result in rset:
		for site in rset[result]:
			try:
				ret_set.add((site[0], site[1], site[2]))
			# improper data
			except IndexError, e:
				pass
	if writeout:
		print '{0: <17} {1}'.format('TOTAL ACCOUNTS:', len(ret_set))
	return ret_set

# Most @limit popular sites
def most_popular_sites(rset, writeout=True, limit=10):
	ret_dict = defaultdict(int)
	reduce_sites = total_site_results_nodup(rset, writeout=False)
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
def alexa_results_by_site(rset, writeout=True):
	ret_dict = defaultdict(set)
	for result in rset:
		for site in rset[result]:
			if site[0]:
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
	reduce_sites = total_unique_results(rset, writeout=False)
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
	print '{0: <17} {1}'.format("Passwords:", prof_user)
	return (prof_user, prof_pass)

# Helper function to change_over_time (IN PROGRESS)
def _delta(rlist, writeout, site):
	if writeout:
		print common_name(site) + ":"
	fmt_string = "{0: <10} --> {1: <10} {2: >5}"
	for i in range(0, len(rlist) - 1): # avoid index error
		sdate = rlist[i][0].split('_')[2]
		edate = rlist[i+1][0].split('_')[2]
		if writeout:
			start_r, end_r = set(), set()
			try:
				for j in rlist[i+1][1]:
					end_r.add((j[0], j[1], j[2]))
				for k in rlist[i][1]:
					start_r.add((k[0], k[1], k[2]))
			# improper data
			except IndexError, e:
				pass
			print fmt_string.format(sdate, edate,\
				 len(end_r - start_r))

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

	_delta(sorted(bmn), writeout, 'bmn')
	_delta(sorted(fa), writeout, 'fakeaccount')
	_delta(sorted(l2m), writeout, 'login2me')
	_delta(sorted(lgz), writeout, 'loginz')
	_delta(sorted(pwd7), writeout, 'pwd7')

	