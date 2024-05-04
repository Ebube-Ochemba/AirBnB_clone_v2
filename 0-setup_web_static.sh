#!/usr/bin/env bash

# Install Nginx if not already installed
sudo apt-get -y update
sudo apt-get -y install nginx

# Create necessary folders if they don't exist
sudo mkdir -p /data/web_static/releases/test/
sudo mkdir -p /data/web_static/shared/

# Create a fake HTML file
echo "<html><head></head><body>Holberton School</body></html>" | sudo tee /data/web_static/releases/test/index.html > /dev/null

# Create symbolic link
rm -rf /data/web_static/current
sudo ln -sf /data/web_static/releases/test/ /data/web_static/current

# Give ownership to the ubuntu user and group
sudo chown -hR ubuntu:ubuntu /data/

# Update Nginx configuration
sudo sed -i '/^}/i \\n\tlocation /hbnb_static {\n\t\talias /data/web_static/current/;\n\t\tindex index.html;\n\t}\n' /etc/nginx/sites-available/default

# Restart Nginx
sudo service nginx restart
