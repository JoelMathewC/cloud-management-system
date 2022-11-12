# Cloud Management System
This project is done as a part of the S7 B.Tech Cloud Computing course from NITC by Abin Gigo Joseph(B190880CS), Joel Mathew Cherian (B190664CS), Joseph Mani Jacob Mani (B190529CS) and Karthik Sridhar (B190467CS).

The project focuses on building a cloud management system in python that autoscales to spawn a new VM when the current VM is overloaded. This project considers the case of scale up from one server to two. The folder structure of the project is as follows

```
.
├── README.md
├── client
│   └── client.py
├── cms
│   └── autoscaler.py
├── output-log
│   ├── README.md
│   ├── autoscaler-log.txt
│   ├── client-log.txt
│   └── plots
│       ├── log-plot.png
│       └── plot-logs.py
└── server
    ├── backend
    │   ├── README.md
    │   └── main.py
    └── start-script
        ├── README.md
        ├── server-startup.service
        └── server-startup.sh
```
## Setup
This project used Lubuntu as the operating system on the host and child VMs. The steps involved in the setup are as follows
1. Using virt-manager to setup VMs (Ensured that KVM was used for faster virtualization). The VMs used in out setup has domain name 'vm1' and 'vm2'.
2. The child VMs created were then assigned a static IP of 192.168.122.150 and 192.168.122.151
3. Additionally we looked into libvirt documentation to monitor and control VMs via the libvirt API.

## Server
The backend is required to run a CPU intensive task. We decided to make a backend that calculated the nth fibonacci number for an input n. The algorithm used has an exponential time complexity ensuring that the task is sufficiently intensive for even small values of n.

We used the lightweight web-framework, fastapi to create the backend. We also set the backend to launch on startup so that the backend is running as soon as a new VM is spawned.

**Logging**: No logging done on the server side

## Client
The client is a multi-threaded application that makes multiple requests to the given backend. The client has two modes
1. Low mode: A small number of requests are made to the backend such that the backend is not overloaded
2. High mode: A high amount of cpu-intensive requests are made to the backend which overloads it

The client also talks to the autoscaler via sockets to get information on if a new VM has been launched. The client randomly chooses from a list of available API endpoints to make backend calls to. When a new VM is spawned its endpoint is added to the list of available API endpoints. 

## Autoscaler
The Autoscaler keeps track of the CPU statistics of vm1. When the CPU stats cross the threshold of 75 it triggers the launching of vm2. When vm2 has finished launching the autoscaler informs the client program of the same via sockets. The launching of VMs and retrieval of CPU statistics is done entirely using the libvirt API.
