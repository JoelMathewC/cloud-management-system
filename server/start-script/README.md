# Steps
### Making the startup script
1. Put server-startup.sh in /usr/bin
2. Run the following command to make the script and executable
```
chmod +x server-startup.sh
```

3. Verify if the script executes with 
```
sudo ./server-startup
```

### Making the service
1. Go to /lib/systemd/system and paste the server-startup.service file

### Enable the service to run on startup
1. Run the following
```
sudo systemctl daemon-reload 
sudo systemctl enable server-startup.service
sudo systemctl start server-startup.service 
```

2. Check status with
```
sudo systemctl status server-startup.service
```