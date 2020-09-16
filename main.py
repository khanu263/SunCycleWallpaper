# SunCycleWallpaper
# by Umair Khan

# Change the wallpaper in a GNOME desktop environment with
# location-based real-time sunrise/sunset data.

# Uses the ip-api (https://ip-api.com/) to get location data
# based on the Internet connection and Sunrise Sunset
# (https://sunrise-sunset.org/api) to get sun timings.

# Imports
import os
import json
import requests
import datetime as dt
import dateutil.parser as dup
import dateutil.relativedelta as dur
import dateutil.utils as duu
import subprocess

# Load and verify configuration file
def load_config():

    # Load file
    with open("config.json", "r") as f:
        config = json.load(f)

    # Check for correct fields
    fields = {"dawn", "day", "dusk", "night", "dawn_window", "dusk_window"}
    assert fields.issubset(config), "Required fields not present."

    # Check for valid data in fields
    assert os.path.isfile(config["dawn"]), "Path for 'dawn' is not valid."
    assert os.path.isfile(config["day"]), "Path for 'day' is not valid."
    assert os.path.isfile(config["dusk"]), "Path for 'dusk' is not valid."
    assert os.path.isfile(config["night"]), "Path for 'night' is not valid."
    assert type(config["dawn_window"]) == int and config["dawn_window"] > 0, "Dawn window must be a positive integer."
    assert type(config["dusk_window"]) == int and config["dusk_window"] > 0, "Dusk window must be a positive integer."

    # If everything checks out, return the configuration
    return config

# Load and verify data file
def load_data():

    # Load file
    with open("data.json", "r") as f:
        data = json.load(f)

    # Check for correct fields
    fields = {"date", "lat", "lon", "sunrise", "sunset"}
    assert fields.issubset(data), "Required fields not present."

    # Check for valid lat/lon
    assert type(data["lat"]) == float and -90 <= data["lat"] <= 90, "Field 'lat' must be a float between -90 and +90."
    assert type(data["lon"]) == float and -180 <= data["lon"] <= 180, "Field 'lon' must be a float between -180 and +180."
    
    # Check for valid dates and times
    try:
        dup.parse(data["date"])
        dup.parse(data["sunrise"])
        dup.parse(data["sunset"])
    except:
        assert False, "At least one of the 'date', 'sunrise', or 'sunset' fields could not be parsed."
    
    # If everything checks out, return the data
    return data

# Figure out if an update is required
def update_required():

    # Grab the latest data
    try:
        curr_data = load_data()
    except:
        return True, "Data file missing or corrupted. Update required."

    # Check if the date has changed
    new_date = str(dt.datetime.now())[:10]
    if new_date != curr_data["date"]:
        return True, "Date has changed. Update required."

    # If the date is the same, get the current location
    try:
        ip_data = json.loads(requests.get("http://ip-api.com/json").text)
        new_lat = round(ip_data["lat"], 1)
        new_lon = round(ip_data["lon"], 1)
    except:
        return False, "Unable to acquire latitude and longitude information. No data update will be performed."

    # Check if the location has changed significantly
    lat_diff = abs(new_lat - curr_data["lat"])
    lon_diff = abs(new_lon - curr_data["lon"])
    if lat_diff > 0.2 or lon_diff > 0.2:
        return True, "Location has changed. Update required."

    # If nothing has triggered, no update required
    return False, "No update required."

# Update the data file with latest information
def update_data():

    # Initialize dictionary with system date
    data = {}
    data["date"] = str(dt.datetime.now())[:10]

    # Get the current latitude and longitde
    try:
        ip_data = json.loads(requests.get("http://ip-api.com/json").text)
        data["lat"] = round(ip_data["lat"], 1)
        data["lon"] = round(ip_data["lon"], 1)
    except:
        return "Unable to acquire latitude and longitude information."

    # Get sunrise and sunset times (UTC) for current date (system) and location
    try:
        api_str = f"https://api.sunrise-sunset.org/json?date={data['date']}&lat={data['lat']}&lng={data['lon']}&formatted=0"
        sun_data = json.loads(requests.get(api_str).text)
        data["sunrise"] = sun_data["results"]["sunrise"]
        data["sunset"] = sun_data["results"]["sunset"]
    except:
        return "Unable to acquire sunrise and sunset information."

    # Write dictionary to file as JSON
    try:
        with open("data.json", "w", encoding = "utf-8") as f:
            json.dump(data, f, ensure_ascii = False, indent = 2)
        return "Data update successful."
    except:
        return "Unable to write new data to file."

# Update the wallpaper based on the current configuration and data.
def update_wallpaper():

    # Grab the configuration
    try:
        config = load_config()
    except AssertionError as e:
        return f"Unable to load configuration file. {str(e)}"
    except:
        return "Unable to load configuration file. Unknown error."

    # Grab the latest data
    try:
        data = load_data()
    except AssertionError as e:
        return f"Unable to load data file. {str(e)}"
    except:
        return "Unable to load data file. Unknown error."

    # Get the current time (UTC), create deltas, and parse sunrise/sunset times
    now = dt.datetime.now(dt.timezone.utc)
    dawn_delta = dt.timedelta(minutes = config["dawn_window"])
    dusk_delta = dt.timedelta(minutes = config["dusk_window"])
    sunrise = dup.parse(data["sunrise"])
    sunset = dup.parse(data["sunset"])
    
    while (sunrise + dt.timedelta (hours = 23) < now):
        now = now - dt.timedelta (days = 1)
    
    # Pick the correct wallpaper
    wallpaper = ""
    if duu.within_delta(now, sunrise, dawn_delta):
        wallpaper = config["dawn"]
    elif duu.within_delta(now, sunset, dusk_delta):
        wallpaper = config["dusk"]
    elif sunrise < now < sunset:
        wallpaper = config["day"]
    elif now < sunrise or sunset < now:
        wallpaper = config["night"]

    # Make sure a wallpaper is picked
    if wallpaper == "":
        return "Could not change wallpaper. Logical error in time calculations."

    # Change the wallpaper
    subprocess.call(f"gsettings set org.gnome.desktop.background picture-uri file://{wallpaper}", shell = True)
    subprocess.call(f"gsettings set org.gnome.desktop.screensaver picture-uri file://{wallpaper}", shell = True)
    return f"Wallpaper and screensaver changed to {wallpaper}."

# Main script
if __name__ == "__main__":

    # Print current date and time
    print(f"Starting run at {str(dt.datetime.now())}.")

    # Check if an update is required
    print("Determining if data update required...")
    update, update_message = update_required()
    print(update_message)

    # If an update is required, update data
    if update:
        print("Attempting to update data...")
        print(update_data())

    # Change wallpaper based on current data
    print("Attempting to update wallpaper...")
    print(update_wallpaper())
