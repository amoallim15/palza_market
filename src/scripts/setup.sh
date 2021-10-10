# Prepare server..
sudo apt-get update
sudo apt-get install -y make
sudo apt-get install -y zip unzip
sudo apt-get install -y python3
sudo apt-get install -y python3-pip
sudo apt-get install -y python3-setuptools
sudo apt-get install -y python3-venv
sudo apt-get install -y supervisor 

# Prepare supervisord..
sudo rm -rf /etc/supervisor
sudo mkdir /etc/supervisor
sudo mkdir /etc/supervisor/conf.d
sudo echo_supervisord_conf | sudo tee /etc/supervisor/supervisord.conf
sudo tee -a /etc/supervisor/supervisord.conf <<EOF
[include]
files=conf.d/*.conf
EOF

# Prepare systemctl..
sudo rm /etc/systemd/system/supervisord.service
sudo tee /etc/systemd/system/supervisord.service <<EOF
[Unit]
Description=Supervisor daemon
Documentation=http://supervisord.org
After=network.target

[Service]
ExecStart=/usr/bin/supervisord -n -c /etc/supervisor/supervisord.conf
ExecStop=/usr/bin/supervisorctl $OPTIONS shutdown
ExecReload=/usr/bin/supervisorctl $OPTIONS reload
KillMode=process
Restart=on-failure
RestartSec=42s
User=ubuntu

[Install]
WantedBy=multi-user.target
Alias=supervisord.service
EOF

# Restart supervisord..
sudo systemctl daemon-reload
sudo systemctl unmask supervisord.service
sudo systemctl enable supervisord.service
sudo systemctl restart supervisord.service
sudo systemctl status supervisord.service