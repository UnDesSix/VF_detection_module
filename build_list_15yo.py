import requests
import re
from utils import write_into_csv_file

# Get final page, which equal to the number of pages to scrape
def get_pages_nb(html_content):
	final_page = re.findall(r'setpage=1\"  >(.*?)<', html_content)
	if len(final_page) == 0:
		return 1
	elif len(final_page) == 1:
		return 2
	elif len(final_page) == 2:
		return 3
	return int(final_page[2])

# Get each part of codes where infos are stored
# Return those parts as a list
def get_htlml_line_content(page_content):
	list = re.findall(r'<tr><td>(.*?)</tr>', page_content)
	return list

# Get each information from country lines
# Return those list of information as a list
def parse_page(html_content):
	list = []
	for item in html_content:
		age = re.findall(r'></td><td class="w50 alc">(.*?)<', item)
		if age[0] == '15':
			id = re.findall(r'&amp;id=(.*?)&', item)
			list.append(id[0])
	return list

# Create text file with all ID of 15 years old players
def build_list_15yo():
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
	# txt_file = open('list/players.txt', 'w') DEBUG
	txt_file = open('detection_tools/list/players.txt', 'w')

	# Get page number
	response = requests.get('https://www.virtuafoot.com/formation.php?detect', headers=headers, cookies=cookies)
	pages = get_pages_nb(response.text)

	# Main routine :
	#     - get html page until pages number is reached
	#     - split it into each line infos
	#     - write data into text file
	for i in range(pages):
		# Get HTML page, split into group of html and split into list of players id
		response = requests.get('https://www.virtuafoot.com/formation.php?detect&setpage=1&page=' + str(i+1), headers=headers, cookies=cookies)
		content_with_html = get_htlml_line_content(response.text)
		content_html_free = parse_page(content_with_html)
		# Iterate through each transfer line until current_trasnfer_id is less than last transfer ID in DB
		for item in content_html_free:
			txt_file.write((item) + '\n')

	txt_file.close()
