[Unit]
Description=Amazon Dash Button Listener (Python)

[Service]
PIDFile=/var/run/dash_listener-99.pid
User=root
Group=root
Restart=always
KillSignal=SIGQUIT
WorkingDirectory=/home/sdlynx/repos/dash-listeners/
ExecStart=/bin/sh ./service.sh

[Install]
WantedBy=multi-user.target
