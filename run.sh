#!/bin/bash

# activate environment
# cd Documents/uroflo
source venv/bin/activate

# run in parallel
# (
  # cd app/backend || exit
  # python manage.py runserver
  # python system/main.py &
  # python system/hematuria.py &
  # python system/mass.py &
# )

(
  cd app/frontend || exit
  npm run dev &
)

firefox-esr -private --kiosk “http://localhost:5173/“ # quit firefox-esr kiosk mode via ALT+F4; install firefox-esr via 'sudo apt install firefox-esr'

wait