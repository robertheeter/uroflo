# UroFlo
Design of an automated continuous bladder irrigation device at Rice University in partnership with Texas Children's Hospital and Baylor College of Medicine.


## Architecture
To be added.


## User interface
![Screenshot of the UroFlo user interface.](/docs/user_interface.jpg)


## Installation
Perform the following commands in a new terminal on Raspberry Pi 4B.

### Configuration modifications
The following should be added to the bottom of `/boot/config.txt` via `sudo nano /boot/config.txt` to operate the touchscreen and remove the splash background on boot.
```
hdmi_force_edid_audio=1
max_usb_current=1
hdmi_force_hotplug=1
config_hdmi_boost=7
hdmi_group=2
hdmi_mode=87
hdmi_drive=2
display_rotate=0
hdmi_timings=1024 1 150 18 150 600 1 15 3 15 0 0 0 60 0 60000000 3

disable_overscan=1
disable_splash=1
```

### Install base dependencies
```
sudo apt update
sudo apt upgrade
sudo apt install python3
sudo apt install python3-pip
sudo apt install nodejs npm
sudo apt install firefox-esr
```
This should install Python, the Node Package Manager (NPM), and the Firefox ESR browser.

### Clone repository and create virtual environment in /uroflo
```
cd /home/[user]/Documents
git clone https://github.com/teamuroflo/uroflo
```
```
cd uroflo
python -m venv venv/
source venv/bin/activate
```

### Install backend dependencies in /uroflo
```
pip install -r requirements.txt
```
This should install all of the required backend (Python) packages.

### Install frontend dependencies in /uroflo/app/frontend
```
cd /app/frontend
npm install
```
This should install all of the required frontend (JavaScript/CSS) packages.

### Add execute permission to /uroflo/run.sh
```
cd ../..
chmod +x run.sh
```

### Run demo.uroflo.io interface (OPTIONAL)
Run the following bash commands in a new terminal.
```
curl https://get.telebit.io/ | bash
~/telebit http 8000
```
`8000` refers to the port that is used for the local Django backend server. The arbitrary forwarding URL that Telebit generates should be copied into the API_URL variable in the `src/config.js` file in the `uroflo-remote` repository where the demo.uroflo.io webpage is created.
```
const API_URL = "https://telebit-url-here.telebit.io";
```

### Run app with /uroflo/run.sh
Run the following 
```
./run.sh
```
This should run the system scripts (main.py and hematuria.py), Django backend server, React frontend server, and FireFox ESR kiosk browser.

### Quit app
Use `ALT+F4` to exit the FireFox ESR kiosk browser.
```
ps
kill [process ID]
```
Kill the 3 Python processes (main.py, hematuria.py, Django backend server) and Node frontend server processes. A list of processes can be viewed with the `ps` command. Alternatively, use `kill -9 -1` to reset the device to the login screen or reboot the Raspberry Pi.

### Run on boot (OPTIONAL)
The following should be added to the bottom of `/home/[user]/.bashrc` via `sudo nano ~/.bashrc` to run the application on boot. Ensure that `run.sh` has execute permission (see above).
```
DISPLAY=:0 /home/[user]/Documents/uroflo/run.sh &
```
To quit the program after running on boot, use `kill -9 -1`, which should reset the device to the login screen, after which the `.bashrc` file can be reverted to not run the application on boot.

## Folders
- [`app/`](app/): scripts for integrated device software and interface web application
- [`docs/`](docs/): project-related documents
