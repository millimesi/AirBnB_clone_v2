#!/usr/bin/env bash
# A bash script that sets up my web servers for the deployment of web_static

# update
sudo apt-get -y update

# Install nginx if not installed
if [ ! -e /etc/nginx ]; then
  sudo apt-get -y install nginx
fi

# start nginx
sudo service nginx start

# Create necessary directory structure under /data/web_static
for dir in /data/web_static/releases/test /data/web_static/shared; do
  if [ ! -d "$dir" ]; then
    sudo mkdir -p "$dir"
  fi
done

# Create a fake HTML file /data/web_static/releases/test/index.html (with simple content, to test your Nginx configuration)
sudo touch /data/web_static/releases/test/index.html
echo "<html>
  <head>
  </head>
  <body>
    Holberton School
  </body>
</html>" | sudo tee /data/web_static/releases/test/index.html > /dev/null

# Create symbolic link /data/web_static/current linked to the /data/web_static/releases/test/ folder
sudo ln -sf /data/web_static/releases/test/ /data/web_static/current

# Give ownership of the /data/ folder to the ubuntu user AND group
sudo chown -R ubuntu:ubuntu /data/

# Update Nginx configuration
sudo sed -i '/server_name _;/a\\tlocation /hbnb_static {\n\t\talias /data/web_static/current/;\n\t}' /etc/nginx/sites-available/default

# restart Nginx
sudo service nginx restart
