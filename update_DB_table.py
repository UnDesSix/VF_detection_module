import psycopg2
import csv

from variables import players_csv_path

def update_table():
	conn = psycopg2.connect(database='virtuadata_db',
							user='root', password='root',
							host='postgres', port='5432')

	conn.autocommit = True
	cursor = conn.cursor()

	# UPDATE CLUBS
	with open(players_csv_path, 'r') as f:
		reader = csv.reader(f)
		next(reader) # Skip the header row.
		for row in reader:
			cursor.execute(
			"INSERT INTO player_detect (country_id, city_id, id, age, name, position, instruction, note) VALUES (%s, %s, %s, %s, %s, %s, %s, %s);",
			row
		)

	conn.commit()
	conn.close()
