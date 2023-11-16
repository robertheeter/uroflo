# uroflo
Scripts for running automated CBI device.

## Setup on local computer
Run on the following commands on your *local computer* to clone the repository, create a virtual environment, and install the required packages:

```
git clone https://github.com/teamuroflo/uroflo.git
cd uroflo/
python -m venv protoenv/
source protoenv/bin/activate
pip install -r requirements.txt
```

## Setup on Raspberry Pi
1. Install [GitHub CLI](https://github.com/cli/cli/blob/trunk/docs/install_linux.md)
2. Run `gh auth login`
   * Use *GitHub.com*
   * Use *HTTPS*
   * Select *yes*, use GitHub credentials to authenticate Git
   * Login with a web browser to authenticate and use one-time code
3. Run the following commands to clone repository, create a virtual environment, and install the requirement packages:
  ```
  cd Documents/
  gh repo clone teamuroflo/uroflo
  cd uroflo/
  python -m venv protoenv/
  source protoenv/bin/activate
  pip install -r requirements.txt
  ```



## Folders
The folders contain the following contents:
* ```pump/```: scripts for peristaltic pump
* ```scale/```: scripts for weight scale
* ```hematuria/```: scripts for hematuria measurement
* ```notif/```: scripts for notification system
