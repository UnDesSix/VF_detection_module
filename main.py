import os
from init_detection import init_trip
from update_DB_table import update_table

from routine import routine, log_file_name

# Main function:
# - check if lof is empty, if so initialize the log file
# - then run routine
if os.stat(log_file_name).st_size == 0:
	init_trip()
routine()
update_table()