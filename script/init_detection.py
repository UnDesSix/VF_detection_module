import psycopg2
import csv

from routine import change_country, change_city, save_log
from build_csv_country import build_csv_countries
from build_list_city import build_list_city
from build_list_15yo import build_list_15yo

from variables import countries_csv_path, countries_txt_path, cities_txt_path, players_txt_path

def create_tables():

	# Connect to DB
	conn = psycopg2.connect(database='virtuadata_db',
							user='root', password='root',
							host='postgres', port='5432')

	# Close communication with the database
	conn.autocommit = True

	# Open a cursor to perform database operations
	cursor = conn.cursor()

	# Delete existing tables and create new ones
	cursor.execute("DROP TABLE IF EXISTS country_detect, player_detect;")
	cursor.execute("CREATE TABLE country_detect (id VARCHAR(255) NOT NULL PRIMARY KEY, name VARCHAR(255) NOT NULL, clubs_nb INTEGER NOT NULL, contracts_nb INTEGER NOT NULL, visited BOOLEAN NOT NULL, price INTEGER NOT NULL, is_vip BOOLEAN NOT NULL);\
					CREATE TABLE player_detect (country_id VARCHAR(255) NOT NULL REFERENCES country_detect(id), city_id VARCHAR(255) NOT NULL, id INTEGER NOT NULL, age INTEGER NOT NULL, name VARCHAR(255) NOT NULL, position VARCHAR(255) NOT NULL, instruction VARCHAR(255) NOT NULL, note INTEGER NOT NULL);")

	# Open CSV files parse each line and insert values
	# with open('csv/countries.csv', 'r') as f: DEBUG
	with open(countries_csv_path, 'r') as f:
		reader = csv.reader(f)
		next(reader) # Skip the header row.
		for row in reader:
			cursor.execute(
			"INSERT INTO country_detect (id, name, clubs_nb ,contracts_nb ,visited ,price ,is_vip) VALUES (%s, %s, %s, %s, %s, %s, %s);",
			row
		)

	# with open(players_csv_path, 'r') as f:
	# 	reader = csv.reader(f)
	# 	next(reader) # Skip the header row.
	# 	for row in reader:
	# 		cursor.execute(
	# 		"INSERT INTO player_detect (country_id, city_id, id, age, name, position, instruction, note) VALUES (%s, %s, %s, %s, %s, %s, %s, %s);",
	# 		row
	# 	)

	# Close cursor and communication with the database
	cursor.close()
	conn.close()


def init_trip():
	build_csv_countries()
	# create_tables()

	# sort_countries() and return a file with countires ID
	# In the mid time build a list of countries
	with open(countries_txt_path, 'w') as f:
		f.write('bn\nws\nge\ncz\nir\nmt\nsi\naz\nzw\n')

	# Go to the first country in the list
	with open(countries_txt_path, 'r') as f:
		countries = [line.strip() for line in f]
	country_id = countries[0]
	change_country(country_id)

	# Build cities list and go to the first city in the list
	build_list_city()
	with open(cities_txt_path, 'r') as f:
		cities = [line.strip() for line in f]
	city_id = cities[0]
	change_city(city_id)

	# Build players list
	build_list_15yo()
	with open(players_txt_path, 'r') as f:
		players = [line.strip() for line in f]
	player_id = players[0]

	# Initialize the log file
	save_log(country_id, city_id, player_id)