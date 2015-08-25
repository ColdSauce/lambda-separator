import time
import os
from subprocess import check_output
import requests
def get_pid(name):
	return check_output(['pidof', name])
while 1:
	time.sleep(5)
	try:
		os.kill(int(get_pid("mpg321")),0)
	except:
		requests.get("http://127.0.0.1:7573/start_sound")
		
		
	
	
