import requests
import re
from variables import players_txt_path, headers, cookies

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
		if age[0] == '15' or age[0] == '16':
			id = re.findall(r'&amp;id=(.*?)&', item)
			list.append(id[0])
	return list

# Create text file with all ID of 15 years old players
def build_list_15yo():
	# Create text file 
	txt_file = open(players_txt_path, 'w')

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
