#!/path/to/python/executable

## Imports
import requests
import json
import socket
from os import system
from datetime import datetime

## File paths
wallpaper_dawn = "file:///absolute/path/to/dawn/file"
wallpaper_day = "file:///absolute/path/to/day/file"
wallpaper_dusk = "file:///absolute/path/to/dusk/file"
wallpaper_night = "file:///absolute/path/to/night/file"
data_path = "/absolute/path/to/data/file"



### UTILITY FUNCTIONS ###

# Function to check if internet connection is available
def check_connection():

	# Attempt to connect to Google
	try:
		socket.create_connection(("www.google.com", 80))
		return True
	except OSError:
		pass
	return False

# Function to get the given digit of a number
def get_digit(number, n):
	return number // 10**n % 10

# Function to add numbers (under 60) as minutes
def add(original, to_add):

	# Add the numbers normally, and roll over if necessary
	actual = original + to_add

	if get_digit(actual, 1) > 5 or get_digit(actual, 2) != get_digit(original, 2):
		actual += 40

	# Account for crossing past 2400
	if actual > 2400:
		return actual - 2400

	return actual

# Function to subtract numbers (under 60) as minutes
def subtract(original, to_sub):

	# Subtract the numbers normally, and roll over if necessary
	actual = original - to_sub

	if get_digit(actual, 1) > 5 or get_digit(actual, 2) != get_digit(original, 2):
		actual -= 40

	# Account for crossing below 0
	if actual < 0:
		return actual + 2400

	return actual



### UPDATE FUNCTIONS ###

# Function to check if the current data file needs to be updated
def update_required(new_lat, new_lon, new_date):

	# Open and parse the old file
	old_file = open(data_path, "r")
	old_coor = old_file.readline().split(",")
	old_lat = float(old_coor[0])
	old_lon = float(old_coor[1])
	old_date = old_file.readline().rstrip()
	old_file.close()

	# Calculate differences
	lat_diff = abs(round(new_lat - old_lat, 1))
	lon_diff = abs(round(new_lon - old_lon, 1))

	# Determine if update is necessary
	if lat_diff > 0.2 or lon_diff > 0.2 or new_date != old_date:
		return True

	return False

# Function to update the background based on values in data_path
def update_background():

	# Get the current time
	current_time = int(str(datetime.time(datetime.utcnow()))[:5].replace(':', ''))

	# Read data from file
	data_file = open(data_path, "r")
	data = data_file.readlines()
	times, files = [None] * 4, [None] * 4
	times[0], files[0] = int(data[2]), wallpaper_dawn
	times[1], files[1] = int(data[3]), wallpaper_day
	times[2], files[2] = int(data[4]), wallpaper_dusk
	times[3], files[3] = int(data[5]), wallpaper_night
	data_file.close()

	# Sort times and periods (based on times)
	together = zip(times, files)
	after_sort = sorted(together)
	times, files = zip(*after_sort)
	times, files = list(times), list(files)

	# Get the appropriate file name based on current time
	file = ""
	if current_time >= times[0] and current_time < times[1]:
		file = files[0]
	elif current_time >= times[1] and current_time < times[2]:
		file = files[1]
	elif current_time >= times[2] and current_time < times[3]:
		file = files[2]
	else:
		file = files[3]

	# Update background
	system("gsettings set org.gnome.desktop.background picture-uri " + file)
	system("gsettings set org.gnome.desktop.screensaver picture-uri " + file)



### UPDATE ROUTINE ###

# If there is an internet connection, try getting fresh data
result = check_connection()

if result:

	# Get the current location coordinates
	ip_data = json.loads(requests.get("http://ip-api.com/json").text)
	lat = round(ip_data["lat"], 1)
	lon = round(ip_data["lon"], 1)

	# Get the current date
	date = datetime.today().strftime("%Y-%m-%d")

	# Check if an update is required
	if update_required(lat, lon, date):

		# Get the new sunrise and sunset times
		sun_data = json.loads(requests.get("https://api.sunrise-sunset.org/json?lat=" + str(lat) + "&lng=" + str(lon) + "&formatted=0", verify = False).text)
		sunrise = int(str(sun_data["results"]["sunrise"][11:16].replace(':', '')))
		sunset = int(str(sun_data["results"]["sunset"][11:16].replace(':', '')))

		# Calculate dawn/dusk changes
		change_to_dawn = subtract(sunrise, 45)
		change_to_day = add(sunrise, 30)
		change_to_dusk = subtract(sunset, 45)
		change_to_night = add(sunset, 30)

		# Write data to file
		file = open(data_path, "w")
		file.write(str(lat) + "," + str(lon) + "\n" + date + "\n" + str(change_to_dawn) + "\n" + str(change_to_day) + "\n" + str(change_to_dusk) + "\n" + str(change_to_night) + "\n")
		file.close()

# Update the background based on the times in the file
update_background()