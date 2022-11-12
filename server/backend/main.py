from fastapi import FastAPI

app = FastAPI()

def fibonacci(n):
	if n == 0:
		return 0
	if n == 1:
		return 1
	return fibonacci(n - 1) + fibonacci(n - 2)

@app.get("/")
async def root():
	return {"message": "Hello World"}

@app.get("/{n}")
async def root(n):
	n = int(n)
	if n < 0:
		return {"message": "Invalid Requests"}
    
    # The server label holds the name of the vm that sends the response
	return {"input" : n ,"result" : fibonacci(n), "server" : "vm1"}