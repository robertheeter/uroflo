# uroflo
Scripts for running automated CBI device.

## Setup
Run on the following commands on the Raspberry Pi to clone the repository, setup a virtual environment, and install the required packages:

```
git clone https://github.com/teamuroflo/uroflo.git
cd uroflo/
python -m venv protoenv/
source protoenv/bin/activate
pip install -r requirements.txt
```

## Files/Folders
The folders contain the following contents:
* ```pump/```: scripts for peristaltic pump
* ```scale/```: scripts for weight scale
