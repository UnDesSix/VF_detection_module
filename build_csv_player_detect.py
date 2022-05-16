import requests
import random
import time
import re

def sleep_random():
	random_time = round(random.uniform(6.00, 8.00), 2)
	time.sleep(random_time)

def parse_page(html_content, country_id, city_id, player_id):
	print(country_id, city_id, player_id)
	list = []

	print(country_id, city_id, player_id)
	# get country_id
	list.append(country_id)
	# get city_id
	list.append(city_id)
	# get player_id
	list.append(player_id)

	all = re.findall(r'<div class=\"td\">(.*?)</div>', html_content)

	# get age
	age = all[1]
	list.append(age)
	# get name
	name = all[0]
	list.append(name)
	# get position
	postition = re.findall(r'\">(.*?)<', all[4])[0]
	list.append(postition)
	# get instruction
	instruction = all[5]
	list.append(instruction)
	# get note (0 - 100)
	note = str(int(float(all[6].split(' /')[0]) * 10))
	list.append(note)
	return list

def build_player_detect_lists(country_id, city_id, player_id):
	cookies = {
		'lang': 'fr',
		'firebase_token': 'null',
		'partner': '1',
    'sessid': '3853081975022313880',
    'auth': 'uid=564504&secret=TGVQaGVuaXg%3D',
		'minichat_date': 'null',
	}
	headers = {
		'User-Agent': 'Mozilla/5.0 (X11; Fedora; Linux x86_64; rv:98.0) Gecko/20100101 Firefox/98.0',
		'Accept': '*/*',
		'Accept-Language': 'fr-FR',
		'Accept-Encoding': 'gzip, deflate, br',
		'Content-Type': 'application/x-www-form-urlencoded',
		'X-Requested-With': 'XMLHttpRequest',
		'X-Lang': 'fr',
    'X-Storage': 'sessid=3853081975022313880&auth=uid%3D564504%26secret%3DTGVQaGVuaXg%253D',
    'X-Sessid': '3853081975022313880',
		'Connection': 'keep-alive',
		'Referer': 'https://www.virtuafoot.com/',
		'Sec-Fetch-Dest': 'empty',
		'Sec-Fetch-Mode': 'cors',
		'Sec-Fetch-Site': 'same-origin',
		'Pragma': 'no-cache',
		'Cache-Control': 'no-cache',
	}

	url =  'https://www.virtuafoot.com/formation.php?detect&id=' + player_id
	requests.get(url, headers=headers, cookies=cookies)
	sleep_random()
	response = requests.get(url, headers=headers, cookies=cookies)
	content_html_free = parse_page(response.text, country_id, city_id, player_id)
	return content_html_free