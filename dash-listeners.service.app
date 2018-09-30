[Unit]
Description=Amazon Dash Button Listener (Python)

[Service]
PIDFile=/var/run/dash_listener-99.pid
User=root
Group=root
Restart=always
KillSignal=SIGQUIT
WorkingDirectory=/home/sdlynx/repos/dash-listeners/
ExecStart=/usr/bin/python3 ./arp_listener.py | /usr/bin/python3 ./hue_adapter.py

[Install]
WantedBy=multi-user.target
