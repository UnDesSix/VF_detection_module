import random
import requests
import os
from build_list_city import build_list_city
from build_list_15yo import build_list_15yo
from build_csv_player_detect import build_player_detect_lists
from utils import write_into_csv_file

# PRODUCTION VARIABLES
log_file_name = 'detection_tools/file.log'
countries_file_name = 'detection_tools/list/countries.txt'
cities_file_name = 'detection_tools/list/cities.txt'
players_file_name = 'detection_tools/list/players.txt'

# TEST VARIABLES
# log_file_name = 'file.log'
# countries_file_name = 'list/countries.txt'
# cities_file_name = 'list/cities.txt'
# players_file_name = 'list/players.txt'

# Read the log file and return 3 values:
# country, city and player IDs
def read_log():
	with open(log_file_name, 'r') as f:
		infos = [line.strip() for line in f]
	return infos[0], infos[1], infos[2]

# Save into the log file 3 values:
# country, city and player IDs
def save_log(country_id, city_id, player_id):
	with open(log_file_name, 'w') as f:
		log_mess = country_id + '\n' + city_id + '\n' + player_id
		f.write(log_mess)

# Change the country of detection given an ID
def change_country(country_id):
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
		'X-Storage': 'lang=fr&partner=1&sessid=5836350246581579583&auth=uid%3D564504%26secret%3DTGVQaGVuaXg%253D',
		'X-Sessid': '5836350246581579583',
		'Connection': 'keep-alive',
		'Referer': 'https://www.virtuafoot.com/',
		'Sec-Fetch-Dest': 'empty',
		'Sec-Fetch-Mode': 'cors',
		'Sec-Fetch-Site': 'same-origin',
		'Pragma': 'no-cache',
		'Cache-Control': 'no-cache',
	}
	

	requests.get('https://www.virtuafoot.com/formation.php?detect&change_nation=1&nation=' + country_id, headers=headers, cookies=cookies)

# Change the city of detection given an ID
def change_city(city_id):
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
		'X-Storage': 'lang=fr&partner=1&sessid=5836350246581579583&auth=uid%3D564504%26secret%3DTGVQaGVuaXg%253D',
		'X-Sessid': '5836350246581579583',
		'Connection': 'keep-alive',
		'Referer': 'https://www.virtuafoot.com/',
		'Sec-Fetch-Dest': 'empty',
		'Sec-Fetch-Mode': 'cors',
		'Sec-Fetch-Site': 'same-origin',
		'Pragma': 'no-cache',
		'Cache-Control': 'no-cache',
	}

	requests.get('https://www.virtuafoot.com/formation.php?detect&change_city=1&city_id=' + city_id, headers=headers, cookies=cookies)

# Get next country, city and players IDs
# Called if last city is reached
def get_next_country(country_id, city_id, player_id):
	# Save all IDs in a list and find the index that match the current ID
	with open(countries_file_name, 'r') as f:
		countries = [line.strip() for line in f]
	index = countries.index(country_id)
	
	# Save the new country ID in country_ID 
	country_id = countries[index+1]

	# Change country and update cities list
	# Get first city ID from the text files
	change_country(country_id)
	build_list_city()
	with open(cities_file_name, 'r') as f:
		cities = [line.strip() for line in f]
	city_id = cities[0]

	# Change city and update players list
	# Get first player ID from the text files
	change_city(city_id)
	build_list_15yo()
	
	with open(players_file_name, 'r') as f:
		players = [line.strip() for line in f]
	player_id = players[0]

	return country_id, city_id, player_id
	
# Get next city and players IDs
# Called if last players is reached
def get_next_city(country_id, city_id, player_id):
	# Save all IDs in a list and find the index that match the current ID
	with open(cities_file_name, 'r') as f:
		cities = [line.strip() for line in f]
	index = cities.index(city_id)

	# Check if the current ID is the last one.
	# If so, call next_country function and return the result
	if index + 1 == len(cities):
		return get_next_country(country_id, city_id, player_id)

	# Otherwise save the new city ID in city_ID 
	city_id = cities[index + 1]

	# Change city and update players list
	change_city(city_id)
	build_list_15yo()

	# Recursive in order to fix empty players file
	if os.stat(players_file_name).st_size == 0:
		return get_next_city(country_id, city_id, player_id)

	# Get first player ID from the text file
	with open(players_file_name, 'r') as f:
		players = [line.strip() for line in f]
	player_id = players[0]

	return country_id, city_id, player_id

# Get next player ID given the current country, city and player IDs
def get_next_player(country_id, city_id, player_id):
	with open(players_file_name, 'r') as f:
		players = [line.strip() for line in f]
	index = players.index(player_id)
	if index + 1 == len(players):
		return get_next_city(country_id, city_id, player_id)
	player_id = players[index + 1]
	return country_id, city_id, player_id

# Scrap an random amount of players in the the range [500,600]
# Store the result in a CSV file and save the last country, city and player IDs
def routine():
	# detect_nb = random.randint(500, 600)
	detect_nb = random.randint(5, 8)

	# Create csv file with header
	# csv_file = open('csv/player_detect_log.csv', 'w') DEBUG
	csv_file = open('detection_tools/csv/player_detect_log.csv', 'w')
	csv_file.write('country_id,city_id,id,age,name,position,instruction,note\n')

	# Create list to contain the players detected (in order to write it all at once in csv file)
	players_detect_lists = []

	# Get the starting point and start iterate:
	# - first append the list of player infos to the players_detect_lists
	# - get next player
	country_id, city_id, player_id = read_log()
	for i in range(detect_nb):
		players_detect_lists.append(build_player_detect_lists(country_id, city_id, player_id))
		country_id, city_id, player_id = get_next_player(country_id, city_id, player_id)

	# Save list of players detected into csv_file
	for list in players_detect_lists:
		write_into_csv_file(list, csv_file)	
	csv_file.close()
	
	# Save the starting point for next scraping session
	save_log(country_id, city_id, player_id)