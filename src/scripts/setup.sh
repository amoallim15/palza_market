# Prepare server..
sudo apt-get update
sudo apt-get install -y make
sudo apt-get install -y zip unzip
sudo apt-get install -y python3
sudo apt-get install -y python3-pip
sudo apt-get install -y python3-setuptools
sudo apt-get install -y python3-venv
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