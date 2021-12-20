#!/usr/bin/env bash
# this update script is used to update the code on the server whenever we make a change,
# so the setup script will be used for the first time, we setup the server, but it only work once
# once the server setup, you need to use the update script to pull updates or changes from git on to the server
#
set -e

# so this is the PROJECT_BASE_PATH which is the location on the server where the source code is going to be kept
PROJECT_BASE_PATH='/usr/local/apps/profiles-rest-api'
# then we run the git pull, and then we run migrate in our virtual environement,
# and then we run the collect static, in case you have added any new dependencies that add anymore static files,
# and finally we restart our supervisor process to make the changes come into affects.
git pull
$PROJECT_BASE_PATH/env/bin/python manage.py migrate
$PROJECT_BASE_PATH/env/bin/python manage.py collectstatic --noinput
supervisorctl restart profiles_api

echo "DONE! :)"
