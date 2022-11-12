import sys
import libvirt
import time
from datetime import datetime
from multiprocessing.connection import Client

def sendMessage(message, port):
	'''
		Input: 
			message: string to be sent
			port: port to send message via
	'''
	address = ('localhost', port)
	conn = Client(address, authkey=b'secret password')
	conn.send(message)
	conn.close()


def getCpustats(dom,domainName,intervalTime):
	'''
		Input:
			dom: Domain handler for a particular domain
			domainName: Name of domain being handled by dom
			intervalTime: Interval time between which CPU time is recorded

		Output: integer representing the percentage of CPU 
		being used by the domain passed as input
	'''
	cpu_stats1 = dom.getCPUStats(False)
	time.sleep(intervalTime)
	cpu_stats2 = dom.getCPUStats(False)
	
	stats = 0
	for i in range(len(cpu_stats2)):
		stats += (cpu_stats2[i]['cpu_time'] - cpu_stats1[i]['cpu_time']) / (10000000.0 * intervalTime)
		
	now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
	print("[{}] {} CPU Usage: {}".format(now,domainName,stats))
	return stats
	
def launchVM(dom):
	'''
		Input: 
			dom: Domain handler for a particular domain
		
		Launches a VM and throws an error and halts if it is unable to.
	'''
	try:
		dom.create()
	except libvirt.libvirtError:
		print('Unable to launch vm')
		sys.exit(1)

def connectToVM(domName):
	'''
		Input:
			domName: Name of domain being handled by dom
		
		Connect to a domain, throws an error and halts if it is unable to.
	'''
	dom = conn.lookupByName(domName)
	if dom == None:
 		print('Failed to find the domain '+domName, file=sys.stderr)
 		exit(1)
	return dom

if __name__ == "__main__":

	#this is defining domain names for vms
	primary_domName = 'vm1'
	secondary_domName = 'vm2'
	threshold = 75
	spikeWaitTime = 3
	intervalTime = 1
	vmLaunchingFlag = False
	
	conn = None
	try:
		conn = libvirt.open("qemu:///system")
	except libvirt.libvirtError as e:
 		print(repr(e), file=sys.stderr)
 		exit(1)
	
	primaryDom = connectToVM(primary_domName)
	spikeCount = 0
	secondaryDom = None
	while True:
 		stats = getCpustats(primaryDom, primary_domName, intervalTime)
 		
 		if secondaryDom is not None:
 			stats2 = getCpustats(secondaryDom, secondary_domName, intervalTime)
 			if stats2 < 20 and vmLaunchingFlag:
 				sendMessage("VM Launched", 6001)
 				vmLaunchingFlag = False
 		else:
 			now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
 			print("[{}] {} CPU Usage: {}".format(now,secondary_domName,0))
 			if stats > threshold:
 				spikeCount += 1
 			else:
 				spikeCount = 0
 			if spikeCount == spikeWaitTime:
 				print("\n" + "-"*20)
 				print("LAUNCHING SECOND VM")
 				print("-"*20 + "\n")
 				secondaryDom = connectToVM(secondary_domName)
 				launchVM(secondaryDom)
 				sendMessage("VM Launching", 6000)
 				vmLaunchingFlag = True
 		print("-"*20 + "\n")
	conn.close()
	exit(0)
