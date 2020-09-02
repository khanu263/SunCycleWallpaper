#!/usr/bin/env bash

# Initial information
echo ""
echo "This script will install everything to ~/.scw, guide you through the initial"
echo "configuration, and add a cron job to run things every fifth minute each hour."
echo ""
echo "If you wish to change anything after running this script, please directly"
echo "edit the files in ~/.scw or use crontab -e as required."
echo ""

# Copy over files
mkdir ~/.scw
echo "Created ~/.scw directory."
cp main.py ~/.scw/
cp run.sh ~/.scw/
echo "Copied main.py and run.sh to ~/.scw."
chmod +x ~/.scw/run.sh
echo "Made ~/.scw/run.sh executable."
echo ""

# Create initial configuration file
echo "For the following prompts, please enter the FULL path to the image"
echo "file -- nothing using the ~ home directory shortcut."
echo ""
echo "{" >> ~/.scw/config.json
for period in dawn day dusk night; do
    read -p "Full path to '$period' wallpaper: " wall
    echo "  \"$period\": \"$wall\"," >> ~/.scw/config.json
done
echo ""
echo "The following prompts determine the window in which the dawn and dusk"
echo "wallpapers will be shown."
echo ""
read -p "Minutes before/after sunrise to show dawn wallpaper: " dawn_window
read -p "Minutes before/after sunset to show dusk wallpaper: " dusk_window
echo "  \"dawn_window\": $dawn_window," >> ~/.scw/config.json
echo "  \"dusk_window\": $dusk_window" >> ~/.scw/config.json
echo "}" >> ~/.scw/config.json
echo ""

# Add cron job
echo "Adding cron job..."
crontab -l > ~/.scw/cron.bak
cp ~/.scw/cron.bak ~/.scw/newcron
echo "*/5 * * * * ~/.scw/run.sh" >> ~/.scw/newcron
crontab ~/.scw/newcron
rm ~/.scw/newcron
echo "New cron file installed. Old file available as ~/.scw/cron.bak."
echo ""

# Final words
echo "Installation process complete! For more information, please view"
echo "the README.md file here or at github.com/khanu263/SunCycleWallpaper."
echo ""
