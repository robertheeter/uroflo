#!/bin/bash

# add execute permission: chmod +x run.sh

# activate environment
# cd Documents/uroflo
source venv/bin/activate
wait 1

# run frontend
(
  cd app/frontend || exit
  npm run dev &
)

# run backend
(
  cd app/backend || exit
  python manage.py runserver &
  
)

# run system
(
  cd app/backend/system || exit
  python system/main.py &
  python system/hematuria.py &
)

# run firefox-esr
firefox-esr -private --kiosk http://localhost:5173/
  # quit firefox-esr kiosk mode: ALT+F4
  # move forward or back page in firefox-esr kiosk mode: ALT+[left arrow/right arrow]
  # install firefox-esr: sudo apt install firefox-esr

wait