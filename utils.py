import pandas as pd
import sqlalchemy

# # Return a string of the last transfer ID registered in the database
# def get_id_last_transfer():
#     engine = sqlalchemy.create_engine('postgresql://root:root@postgres:5432/virtuadata_db')
#     dbConnection = engine.connect()

#     #line to get the last transfer ID
#     dataFrame = pd.read_sql('SELECT id FROM transfer ORDER BY id DESC', dbConnection)
#     last_id = dataFrame['id'][0]

#     dbConnection.close()
#     return last_id

# Construct params variable as a tuple, essential for building request
def construct_params_tuple(string, id):
	params = (
		(string, id),
	)
	return params

# Construct params variable as a dictionnary, essential for building request
def construct_params_dic(string, id):
	params = {
		string: str(id),
	}
	return params

# Iterate through items and write into file with CSV formatting
def write_into_csv_file(items, f):
	buffer = ""
	for i, item in enumerate(items):
		if i < len(items) - 1:
			buffer += item + ','
		else:
			buffer += item + '\n'
	f.write(buffer)

# Convert price format from xx€, xxK€ or xx.xM€ into integer format
def	convert_price(price):
	if price[-1] == 'k':
		return int(price[:-1]) * 1000
	if price[-1] == 'M':
		return int(float(price[:-1]) * 1000000)
	return int(price)