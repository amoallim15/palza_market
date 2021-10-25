# Prepare server..
wget -qO - https://www.mongodb.org/static/pgp/server-5.0.asc | sudo apt-key add -
echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu focal/mongodb-org/5.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-5.0.list
sudo apt-get update
sudo apt-get install -y make
sudo apt-get install -y zip unzip
sudo apt-get install -y python3
sudo apt-get install -y python3-pip
sudo apt-get install -y python3-setuptools
sudo apt-get install -y python3-venv
sudo apt-get install -y python3-wheel
sudo apt-get install -y python3-dev
sudo apt-get install -y mongodb-org
# sudo apt-get install -y nginx


sudo tee /etc/systemd/system/palza_market.service <<EOF
[Unit]
Description=Palza Market
After=network.target

[Service]
ExecStart=/bin/bash -c 'source /home/ubuntu/project/venv/bin/activate && gunicorn -k uvicorn.workers.UvicornWorker src.server:app -w 4 --bind 0.0.0.0:8080'
KillMode=process
Restart=on-failure
RestartSec=42s
User=ubuntu
Environment="ENV=PROD"
WorkingDirectory=/home/ubuntu/project

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl daemon-reload
sudo systemctl unmask palza_market.service
sudo systemctl enable palza_market.service
sudo systemctl restart palza_market.service
sudo systemctl status palza_market.service