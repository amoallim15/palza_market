# Copy files..
sudo rm -rf project
mkdir project
unzip project.zip -d ./project/

# Navigate to project folder..
cd ./project

# Install dependencies..
sudo make py.setup;

# Update supervisord config
sudo cp /home/ubuntu/project/src/config/palza_market.conf /etc/supervisor/conf.d/palza_market.conf

# Restart supervisord..
sudo systemctl restart supervisord.service
sudo systemctl status supervisord.service
