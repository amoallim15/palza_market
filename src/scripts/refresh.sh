# Copy files..
sudo rm -rf project
sudo mkdir project
sudo unzip project.zip -d ./project/

# Navigate to project folder..
cd ./project

# Install dependencies..
sudo make py.setup;

# Restart the project..
sudo systemctl restart palza_market.service
sudo systemctl status palza_market.service
