#!/usr/bin/env bash
# A script that sets up my server
if ! command -v nginx &> /dev/null; then
    # Install Nginx
    sudo apt-get update
    sudo apt-get install nginx -y
fi
#create the directory
for dir in /data/web_static/releases/test /data/web_static/shared; do
  if [ ! -d "$dir" ]; then
    sudo mkdir -p "$dir"
  fi
done
#create the test html
echo "<html>
  <head>
  </head>
  <body>
    Holberton School
  </body>
</html>" | sudo tee /data/web_static/releases/test/index.html > /dev/null

# Create symbolic link 
sudo ln -sf /data/web_static/releases/test/ /data/web_static/current

#give owner ship
sudo chown -R ubuntu:ubuntu /data/

# Update Nginx configuration
if ! grep -q "location /hbnb_static" /etc/nginx/sites-available/default; then
    # If it doesn't exist, add the directive
    sudo sed -i '/server_name _;/a\\tlocation /hbnb_static {\n\t\talias /data/web_static/current/;\n\t}' /etc/nginx/sites-available/default
fi
# restart Nginx
sudo service nginx restart
