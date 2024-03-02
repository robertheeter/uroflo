# UroFlo
Design of an automated continuous bladder irrigation device at Rice University in partnership with Texas Children's Hospital and Baylor College of Medicine.

## Architecture
To be added.

## User interface
![Screenshot of the UroFlo user interface dashboard.](/docs/user_interface.jpg)

## Installation
Perform the following commands in a new terminal on Raspberry Pi 4B.

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

### Clone repository, create virtual environment, and install backend dependencies in /uroflo
```
cd /home/[user]/Documents
git clone https://github.com/teamuroflo/uroflo
```
```
cd uroflo
python -m venv venv/
source venv/bin/activate
```
```
pip install -r requirements.txt
pip install django-cors-headers ## ADD THIS TO REQUIREMENTS.TXT, and check if requirements.txt is comprehensive
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

### Run app with /uroflo/run.sh
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
Kill the 3 Python processes (main.py, hematuria.py, Django backend server) and Node frontend server processes. A list of processes can be viewed with the `ps` command. Alternatively, reboot the Raspberry Pi.

## Folders
- [`app/`](app/): scripts for integrated device software and interface web application
- [`docs/`](docs/): project-related documents
