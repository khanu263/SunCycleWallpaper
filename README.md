# SunCycleWallpaper

A simple Python script to change the wallpaper in a GNOME desktop environment according to location-based real-time sunrise/sunset data.

![demo](demo.gif)

*Note: An internet connection is required. If the connection is lost, the wallpaper will be updated based on the last-known location and sunrise/sunset data.*

### Prerequisites

This script was developed with Python 3.8.2 and GNOME Shell 3.36.4, but things should work with any version of Python 3 and any reasonably modern version of the GNOME shell, since the `gsettings` command is used to change the wallpaper.

Before getting started, make sure you have the `requests` and `dateutil` modules installed for Python 3. In particular, these modules should be accessible from your "base" version of Python 3, outside of any environments.

### Installation

1. Clone this repository somewhere on your computer.
2. Run `install.sh` and follow the prompts.

### How things work

By default, everything is installed to `~/.scw`. The installation script will add cron jobs to run the updater every fifth minute of every hour, and at boot, so you should start seeing results pretty soon. The output from every run of the updater is stored at `~/.scw/log.txt`.

The configuration data entered during the installation process is formatted as JSON and stored in `~/.scw/config.json`. If you want to change the wallpaper paths or dawn/dusk windows, this is the file to edit.

The updater stores location and sunrise/sunset information in `~/.scw/data.json`. You shouldn't need to touch this file, but it is human-readable, so if weird things are happening and you can't make sense of the log file, check out this file. The `date` field should match your system's date, and the sunrise/sunset times should be stored as UTC timestamps. This data is only updated if the date or location changes, so for most updater runs this file remains unchanged.

Note that the cron job doesn't actually run the Python script itself -- it runs `~/.scw/run.sh`, which sets up the environment variable to allow the `gsettings` command to work and then runs the Python script and redirects output to the log file. If you ever need to run the script manually, you can navigate to `~/.scw` and run `python3 main.py`, which will print the output instead of putting it in the log file.

### Acknowledgements

-  [requests](https://requests.readthedocs.io/en/master/) -- for API calls
-  [dateutil](https://dateutil.readthedocs.io/en/stable/) -- for date/time calculations
-  [ip-api.com](http://ip-api.com/) -- approximating location
-  [Sunrise Sunset](https://sunrise-sunset.org/) -- getting sunrise/sunset times

For the wallpapers seen in the demonstration, go [here](https://imgur.com/gallery/D6ia1).

### License

This repository is under the GNU GPLv3 license -- see [COPYING](COPYING) for full details.
