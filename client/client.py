import requests
import threading
import time
import random
from datetime import datetime
from multiprocessing.connection import Listener

# APIs for the backend
api_list = ["http://192.168.122.150:8000/"]
secondary_vm_api = "http://192.168.122.151:8000/"

# Flag to stop sending requests when VM1 is already overloaded
launchingVMFlag = False

# Class of threads that make backend calls
class ClientThread (threading.Thread):
    def __init__(self, threadID, name, api):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.api = api

    def run(self):
        '''
            Makes a request to the backend and 
            prints the result to the screen
        '''
        print("Starting " + self.name)

        response = requests.get(f"{self.api}")
        if response.status_code == 200:
            data = response.json()
            print("{} Log: Fibonacci({}) = {}   |   Server: {}  |   Response Time: {}".format(self.name,data["input"],data["result"],data["server"],response.elapsed.total_seconds()))
        else:
            print("{} Log: {} error with your request".format(self.name,response.status_code))

        print("Exiting " + self.name)
        
# Class of threads that communicate with the autoscaller
class ListenerThread (threading.Thread):
    def __init__(self, threadID, name, port):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.port = port

    def run(self):
        '''
            Listens at a particular port for a message and manupilates 
            certain global variables based on those messages
        '''
        print("Starting " + self.name)

        global launchingVMFlag
        address = ('localhost', self.port)
        listener = Listener(address, authkey=b'secret password')
        conn = listener.accept()
        print('connection accepted from' + str(listener.last_accepted))
        msg = conn.recv()
        conn.close()
        listener.close()

        if msg == "VM Launched":
            print("RECIEVED MESSAGE FROM AUTOSCALER: " + msg)
            launchingVMFlag = False
            api_list.append(secondary_vm_api)

        elif msg == "VM Launching":
            print("RECIEVED MESSAGE FROM AUTOSCALER: VM Overloaded, waiting for scaling")
            launchingVMFlag = True
        else:
            print("RECIEVED MESSAGE FROM AUTOSCALER: " + msg)

        print("Exiting " + self.name)


def low_mode():
    '''
        Low mode client that generates a small amount of 
        requests that does not overload the VM
    '''
    threadList = []
    num_threads = 5
    random.seed(datetime.now())
	
    now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    print("[{}] CLIENT: STARTING IN LOW MODE".format(now))

    # Making threads
    for i in range(0,num_threads):
        threadList.append(ClientThread(i+1,"Thread-"+str(i+1),api_list[0] + str(random.randint(15,25))))
    
    # Starting threads
    for thread in threadList:
        thread.start()

def high_mode():
    '''
        High mode client that generates a large number 
        of requests and overloads the VM
    '''
    num_threads = 5
    num_grps = 12
    global launchingVMFlag
    
    now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    print("[{}] : CLIENT MOVING TO HIGH MODE".format(now))
    
    i = 0
    # Making threads
    while i< num_grps:
        if not launchingVMFlag:
            threads = [ClientThread(j+1,"Group-" + str(i+1)+ " Thread-"+str(j+1),api_list[random.randint(0,len(api_list)-1)]+str(random.randint(30,33))) for j in range(0,num_threads)]
            for thread in threads:
                thread.start()
            
            # This is to give the autoscaler a gap to inform the client of overload if any
            time.sleep(3)

            i += 1

if __name__ == "__main__":
	
    low_mode()
    
    # Sleep time before moving to high mode
    time.sleep(10)
    
    # Launching threads to listen to autoscaler
    launchingListenerThread = ListenerThread(100,"Launching Listener Thread", 6000)
    launchedListenerThread = ListenerThread(101,"Launched Listener Thread", 6001)
    launchingListenerThread.start()
    launchedListenerThread.start()
    
    high_mode()
    print("Exiting Main Thread")
