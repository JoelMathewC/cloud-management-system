# Running the server

## Installs
Installing fastapi
```
sudo pip install fastapi
```

Installing uvicorn
```
sudo pip install uvicorn[standard]
```

**Note:** All the installs here are done on the root user since the root user needs to run the server on startup.

## Running
Running the backend on the child vm's IP on port 8000
```
uvicorn main:app --host 0.0.0.0 --port 8000
```
