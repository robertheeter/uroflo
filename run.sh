#!/bin/bash

# add execute permission: chmod +x run.sh

# activate environment
# cd Documents/uroflo
source venv/bin/activate

# run system
(
  cd app/backend/system || exit
  python main.py &
  python hematuria.py &
  sleep 2
)

# run backend
(
  cd app/backend || exit
  python manage.py runserver &
  sleep 2
)

# run frontend
(
  cd app/frontend || exit
  npm run dev &
  sleep 2
)

# run browser
(
  cd app/frontend/browser || exit
  python kiosk.py
  sleep 2
)

wait