import requests
import random
import time
import re
# from variables import cookies
from variables import cookies, headers

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
	url =  'https://www.virtuafoot.com/formation.php?detect&id=' + player_id
	requests.get(url, headers=headers, cookies=cookies)
	sleep_random()
	response = requests.get(url, headers=headers, cookies=cookies)
	content_html_free = parse_page(response.text, country_id, city_id, player_id)
	return content_html_free