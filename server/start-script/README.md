# Steps

1. Put server-startup.sh in /usr/bin
2. run
```
chmod +x server-startup.sh
```
3. verify if it executes with 
```
sudo ./server-startup
```
4. Go to /lib/systemd/system and paste the server-startup.service file
5. Make sure the paths are correct
6. Run the following
```
sudo systemctl daemon-reload 
sudo systemctl enable server-startup.service
sudo systemctl start server-startup.service 
```
7. Check status with
```
sudo systemctl status server-startup.service
```