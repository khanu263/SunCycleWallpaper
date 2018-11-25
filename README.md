# SunCycleWallpaper

A simple Python script to change the wallpaper in a GNOME desktop environment with location-based real-time sunrise/sunset data.

![Demonstration](demo.gif)

*Note: An internet connection is required for initial setup. If an internet connection is not available in the future, the script will update the wallpaper based on the last-known location and sunrise/sunset data.*

## Getting Started

Tested with Python 3.6.7 and GNOME Shell 3.28.3. Uses the `gsettings` command to change the wallpaper.

### Prerequisites

Make sure you have the `requests` module installed for Python 3.

```bash
$ python3 -m pip install requests
```

### Installation

1. Get four wallpapers -- one each for dusk, dawn, day and night.
2. Grab `SunCycleChanger.py` and put it anywhere on your system (preferably somewhere in the user filesystem).
3. Edit the shebang on line 1 to point to your Python executable (e.g. `/usr/bin/python3`).
4. Edit lines 17-20 in the script to point to your desired wallpapers.
5. Create a file to store sunrise/sunset and location data (e.g. `touch SunCycleData.txt`) and edit line 21 in the script to point to that file.
6. Make `SunCycleChanger.py` executable (e.g. `chmod +x /path/to/SunCycleChanger.py`)

The script is set to the following schedule:

- dawn wallpaper -- 45 min before sunrise to 30 min after sunrise
- day wallpaper -- 30 min after sunrise to 45 min before sunset
- dusk wallpaper -- 45 min before sunset to 30 min after sunset
- night wallpaper -- 30 min after sunset to 45 min before sunrise

To change this schedule, edit lines 160-163 in the script as desired.

### Automation

Although the ideal way to run the script every five minutes would be with cron, there are lots of issues with permissions and environment variables I have yet to solve.

For now, the simplest way to automate running the script is to open Startup Applications and add the following command:

```bash
/bin/bash -c "sleep 5 && while true; do /path/to/SunCycleChanger.py ; sleep 300; done"
```

## Acknowledgements

-  [requests](https://github.com/requests/requests) - for API calls
-  [ip-api.com](http://ip-api.com/) - approximating location
-  [Sunrise Sunset](https://sunrise-sunset.org/) - getting sunrise/sunset times

Originally inspired by [this](https://old.reddit.com/r/androidthemes/comments/452tfn/firewatch_with_changing_wallpapers/) Reddit post. For the wallpapers seen in the demonstration gif, go [here](https://imgur.com/gallery/D6ia1).

## Future Features

- cron compatibility
- option to log results/errors to a file
- easier/automated installation

## License

This script is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for full details.
