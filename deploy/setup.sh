#!/usr/bin/env bash

set -e

# TODO: Set to URL of git repo.
PROJECT_GIT_URL='https://github.com/kienyiep/profile-rest-api.git'

PROJECT_BASE_PATH='/usr/local/apps/profiles-rest-api'

echo "Installing dependencies..."
apt-get update
apt-get install -y python3-dev python3-venv sqlite python-pip supervisor nginx git

# Create project directory
mkdir -p $PROJECT_BASE_PATH
git clone $PROJECT_GIT_URL $PROJECT_BASE_PATH

# Create virtual environment
mkdir -p $PROJECT_BASE_PATH/env
python3 -m venv $PROJECT_BASE_PATH/env

# Install python packages
$PROJECT_BASE_PATH/env/bin/pip install -r $PROJECT_BASE_PATH/requirements.txt
$PROJECT_BASE_PATH/env/bin/pip install uwsgi==2.0.18

# Run migrations and collectstatic
# we run the collectstatic command to gather all of the static file for all of the apps in our project into one directory.
# when we use the django management server, it does this autimatically for you.
# but since we will not be using the django development server on production,
# we need to create a location with all the static files which can be used to serve the CSS and Javascript for the django admin and the django rest framework browsable api.
# we need to tell django where to store the statics files when we run this command, we do this by setting the static root in the setting.py file

cd $PROJECT_BASE_PATH
$PROJECT_BASE_PATH/env/bin/python manage.py migrate
$PROJECT_BASE_PATH/env/bin/python manage.py collectstatic --noinput


# Configure supervisor
# supervisor is an application on linux that allows you to manage processess, which will manage the python process or our uWSGI server.
# so we will need to copy the the supervisor profiles api configuration.config file into the location of the server where the supervisor is kept.
cp $PROJECT_BASE_PATH/deploy/supervisor_profiles_api.conf /etc/supervisor/conf.d/profiles_api.conf
# we run the reread to update these supervisor configuration files
supervisorctl reread
# we run update to update all the processess
supervisorctl update
#we restart our profiles api to make sure our service is started.
supervisorctl restart profiles_api


# Configure nginx
#we need to create a location for the configuration file and we copy that configuration file that we have added here nginx_profiles_api.conf
# to the site available directory nginx, then we remove the default configuration that is provided  when you install nginx,
# and we add the symbolic link from our sites available to our sited enabled to enable our site.
# finally we restart the nigix service and then the script exist with this message here saying done.
cp $PROJECT_BASE_PATH/deploy/nginx_profiles_api.conf /etc/nginx/sites-available/profiles_api.conf
rm /etc/nginx/sites-enabled/default
ln -s /etc/nginx/sites-available/profiles_api.conf /etc/nginx/sites-enabled/profiles_api.conf
systemctl restart nginx.service

echo "DONE! :)"
