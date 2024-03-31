#!/bin/bash

# add execute permission: chmod +x run.sh

# activate environment
cd /home/uroflo/Documents/uroflo
source venv/bin/activate

# delete all existing databases
cd app/backend/system
sudo rm -r data
sleep 1.0
sudo mkdir data
cd ../..
sleep 1.0

# run frontend
(
  cd frontend || exit
  npm run dev &
  sleep 1.0
)

# run system
(
  cd backend/system || exit
  python main.py &
  python hematuria.py &
  sleep 1.0
)

# run backend
(
  cd backend || exit
  python manage.py runserver &
  sleep 1.0
)

# run browser
(
  cd frontend/browser || exit
  python kiosk.py
  sleep 1.0
)

wait