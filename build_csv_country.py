import requests
import re
from utils import convert_price, write_into_csv_file
from variables import cookies, headers, countries_csv_path

# Get each part of codes where infos are stored
# Return those parts as a list
def get_htlml_line_content(page_content):
	list = re.findall(r'<tr><td>(.*?)</tr>', page_content)
	return list

# Get each information from country lines
# Return those list of information as a list
def parse_page(html_content):
	list = []
	# get country_id
	country_id = re.findall(r'flag-(.*?)\"', html_content)
	list.append(country_id[0])
	# get name
	name = re.findall(r'\"></span> (.*?)<', html_content)
	list.append(name[0])

	clubs_contracts_visited = re.findall(r'class="w40 alc">(.*?)<', html_content)
	# get clubs_nb
	list.append(clubs_contracts_visited[0]) if clubs_contracts_visited[0] != '-' else list.append('0')
	# get contracts
	list.append(clubs_contracts_visited[1]) if clubs_contracts_visited[1] != '-' else list.append('0')
	# get visited
	list.append('false') if clubs_contracts_visited[3] == '-' else list.append('true')

	# get price
	price = re.findall(r'\"cv\">(.*?)€', html_content)
	list.append(str(convert_price(price[0])))
	# get is_vip
	is_vip = re.findall(r'href="#(.*?)\?', html_content)
	list.append('true') if is_vip[0] == 'vfstore' else list.append('false')
	return list

# Create countries csv file
def build_csv_countries():	
	# Create csv file with header 
	csv_file = open(countries_csv_path, 'w')
	csv_file.write('id,name,clubs_nb,contracts,visited,price,is_vip\n')

	# Get HTML page and split into group of html
	response = requests.get('https://www.virtuafoot.com/formation.php?detect&change_nation', headers=headers, cookies=cookies)
	content_with_html = get_htlml_line_content(response.text)

	# Iterate through each transfer line until current_trasnfer_id is less than last transfer ID in DB
	for item in content_with_html:
		content_html_free = parse_page(item)
		write_into_csv_file(content_html_free, csv_file)

	csv_file.close()