import psycopg2
import csv

def update_table():
	conn = psycopg2.connect(database='virtuadata_db',
							user='root', password='root',
							host='postgres', port='5432')

	conn.autocommit = True
	cursor = conn.cursor()

	# UPDATE CLUBS
	with open('detection_tools/csv/player_detect_log.csv', 'r') as f:
		reader = csv.reader(f)
		next(reader) # Skip the header row.
		for row in reader:
			cursor.execute(
			"INSERT INTO player_detect (country_id, city_id, id, age, name, position, instruction, note) VALUES (%s, %s, %s, %s, %s, %s, %s, %s);",
			row
		)

	conn.commit()
	conn.close()
