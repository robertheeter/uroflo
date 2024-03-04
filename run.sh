#!/bin/bash

# add execute permission: chmod +x run.sh

# activate environment
cd /home/uroflo/Documents/uroflo
source venv/bin/activate

# TEMPORARY delete all existing databases
python app/backend/system/data.py
sleep 0.1

# run frontend
(
  cd app/frontend || exit
  npm run dev &
  sleep 1.0
)

# run system
(
  cd app/backend/system || exit
  python main.py &
  python hematuria.py &
  sleep 0.1
)

# run backend
(
  cd app/backend || exit
  python manage.py runserver &
  sleep 0.1
)

# run browser
(
  cd app/frontend/browser || exit
  python kiosk.py
  sleep 0.1
)

wait