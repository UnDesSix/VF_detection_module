import requests
import re
from variables import cookies, headers, cities_txt_path

# Get each cities ID
# Return a list of the ID
def parse_page(html_content):
	# get id
	id = re.findall(r'city_id=(.*?)\"', html_content)
	return id

# Create text file with all ID of cities in the first page
# (not all cities of the country)
def build_list_city():
	# Create text file 
	txt_file = open(cities_txt_path, 'w')

	# Get HTML page
	response = requests.get('https://www.virtuafoot.com/formation.php?detect&change_city', headers=headers, cookies=cookies)
	content_html_free = parse_page(response.text)

	# Iterate through each ID line until and write it in text file
	for item in content_html_free:
		txt_file.write((item) + '\n')

	txt_file.close()