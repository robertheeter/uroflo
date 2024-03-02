# UroFlo
Design of an automated continuous bladder irrigation device at Rice University in partnership with Texas Children's Hospital and Baylor College of Medicine.

## Software Installation
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

cd uroflo
python -m venv venv/
source venv/bin/activate

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

### Add execute permission to /uroflo/run.sh run script
```
cd ../..
chmod +x run.sh
```

### Run app with /uroflo/run.sh run script
```
./run.sh
```
This should run the system scripts (main.py and hematuria.py), Django backend server, React frontend server, and FireFox ESR kiosk browser.

## Folders & Files
- [`app/`](app/): scripts for integrated device software and interface web application
- [`docs/`](docs/): project-related documents
