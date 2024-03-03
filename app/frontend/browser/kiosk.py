import os

url = "http://localhost:5173/landing"

os.system(f"firefox-esr -private --kiosk {url}")

# quit firefox-esr kiosk mode: ALT+F4
# move forward or back page in firefox-esr kiosk mode: ALT+[left arrow/right arrow]
# install firefox-esr: sudo apt install firefox-esr