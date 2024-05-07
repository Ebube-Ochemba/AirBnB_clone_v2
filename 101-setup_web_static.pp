# A manifest that sets up your web servers for the deployment of web_static.

# Update server
exec {'update':
  command => '/usr/bin/apt-get update',
}

# Install Nginx if not already installed
-> package { 'nginx':
  ensure => installed,
}

# Create necessary folders if they don't exist
-> exec { 'directories':
  command => '/usr/bin/mkdir -p "/data/web_static/releases/test/" "/data/web_static/shared/"',
}

# Create a fake HTML file
-> exec { 'test html content':
  command => '/usr/bin/echo "Holberton School" | sudo tee /data/web_static/releases/test/index.html > /dev/null',
}

# Delete symbolic link
-> exec { 'del sym link':
  command => '/usr/bin/rm -rf /data/web_static/current',
}

# Create symbolic link
-> exec { 'create sym lnk':
  command => '/usr/bin/ln -s /data/web_static/releases/test/ /data/web_static/current',
}

# Give ownership to the ubuntu user and group
-> exec { 'user and group':
  command => '/usr/bin/chown -R ubuntu:ubuntu /data/',
}

# Update Nginx configuration
-> exec { 'nginx config':
  command => 'sudo sed -i "/^server {/a \ \n\tlocation \/hbnb_static {alias /data/web_static/current/;index index.html;}" /etc/nginx/sites-enabled/default',
  provider => shell,
}

# Restart Nginx
-> exec { 'nginx restart':
  command => '/usr/sbin/service nginx restart',
}
