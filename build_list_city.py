import requests
import re
from utils import write_into_csv_file

# Get each cities ID
# Return a list of the ID
def parse_page(html_content):
	# get id
	id = re.findall(r'city_id=(.*?)\"', html_content)
	return id

# Create text file with all ID of cities in the first page
# (not all cities of the country)
def build_list_city():
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
	

	# Create text file 
	# txt_file = open('list/cities.txt', 'w') DEBUG
	txt_file = open('detection_tools/list/cities.txt', 'w')

	# Get HTML page
	response = requests.get('https://www.virtuafoot.com/formation.php?detect&change_city', headers=headers, cookies=cookies)
	content_html_free = parse_page(response.text)

	# Iterate through each ID line until and write it in text file
	for item in content_html_free:
		txt_file.write((item) + '\n')

	txt_file.close()