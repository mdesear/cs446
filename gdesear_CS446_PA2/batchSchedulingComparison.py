"""
Misha Desear
CS 446 PA2

About batchSchedulingComparison:
A program that allows the user to input the name of a text file containing processes and associated information
(PID, burst time, arrival time, and priority) and a desired scheduling algorithm. The program then returns the order
in which processes were executed using their PIDs, as well as average turnaround and wait times.

FCFS: 
Most appropriate for batch systems and situations where all processes are short and do not need to execute in a 
specific order. Easy to implement and minimal overhead, however processes may wait for long amounts of time before 
execution depending on burst time of processes that arrived first. This makes FCFS less efficient than other methods.
Convoy effect is another issue that can arise as a result of FCFS, wherein one slow process slows the entire set of
processes, and subsequently the entire operating system. 

Shortest Job First:
Most appropriate for batch systems and situations where all processes are available at the same time and their 
run times are known. Waiting time for each process is relatively minimal, however, there is the possibility of 
a long process never being executed as shorter processes are continuously executed first (starvation). SJF 
implementation is more complex compared to FCFS due to the need to record elapsed/remaining time. This also 
results in more overhead compared to FCFS.

Priority:
Most appropriate for real time operating systems and situations where processes need to be executed in a specific 
order. Also relatively easy to implement, as it is similar to FCFS (this is how ties are broken) except it takes 
process priority into account. Starvation is also an issue that can arise with this scheduling algorithm in the 
form of higher priority processes being continuously executed and lower priority processes never being executed. 
"""

import sys, glob, os

class Process:

	def __init__(self, pid, arrivalTime, burstTime, priority):
		self.pid = pid
		self.arrivalTime = arrivalTime
		self.burstTime = burstTime
		self.priority = priority
		
	def getPid(self):
		return self.pid
		
	def getArrival(self):
		return self.arrivalTime
		
	def getBurst(self):
		return self.burstTime
		
	def getPriority(self):
		return self.priority

def main():
	batchfileName = ''
	sortType = ''
	
	if len(sys.argv) != 3:
		print ('Usage: batchSchedulingComparison.py <batchfileName> <sortType>')
	else:
		try:
			processes = []
			completeTimes = []
			pids = []
			arrivals = []
			bursts = []
			priorities = []
			
			batchfileName = sys.argv[1] 
			sortType = sys.argv[2]
				
			ifile = open(batchfileName, 'r').readlines()
			for line in ifile:
				row = line.split(',')
				pid, arrivalTime, burstTime, priority = [i.strip() for i in row]
				process = Process(pid, arrivalTime, burstTime, priority)
				processes = processes + [ process ]
				
			pids = [process.pid for process in processes]
			arrivals = [process.arrivalTime for process in processes]
			bursts = [process.burstTime for process in processes]
			priorities = [process.priority for process in processes]
			
			if sortType == 'FCFS':
				completeTimes, FCFSpids = FirstComeFirstServedSort(processes)
				avgTurnaround, taTimes = AverageTurnaround(completeTimes, arrivals)
				avgWait = AverageWait(taTimes, bursts)
				print ('\nPID ORDER OF EXECUTION\n')
				for i in range(0, len(FCFSpids)):
					print (FCFSpids[i] + '\n')
				print ('Average Process Turnaround Time: ' + '%.2f' % avgTurnaround + '\n')
				print ('Average Process Wait Time: ' + '%.2f' % avgWait + '\n') 
				
			elif sortType == 'ShortestFirst':
				completeTimes, SJFpids = ShortestJobFirst(processes)
				avgTurnaround, taTimes = AverageTurnaround(completeTimes, arrivals)
				avgWait = AverageWait(taTimes, bursts)
				print ('\nPID ORDER OF EXECUTION\n')
				for i in range(0, len(SJFpids)):
					print (SJFpids[i] + '\n')
				print ('Average Process Turnaround Time: ' + '%.2f' % avgTurnaround + '\n')
				print ('Average Process Wait Time: ' + '%.2f' % avgWait + '\n')
				
			elif sortType == 'Priority':
				completeTimes, priorityPids = PrioritySort(processes)
				avgTurnaround, taTimes = AverageTurnaround(completeTimes, arrivals)
				avgWait = AverageWait(taTimes, bursts)
				print ('\nPID ORDER OF EXECUTION\n')
				for i in range(0, len(priorityPids)):
					print(priorityPids[i] + '\n')
				print ('Average Processes Turnaround Time: ' + '%.2f' % avgTurnaround + '\n')
				print ('Average Processes Wait Time: ' + '%.2f' % avgWait + '\n')
			else:
				print ('Invalid process scheduling algorithm entered. Valid options are FCFS, ShortestFirst, or Priority.')
				sys.exit()
			
		except IOError: 
			print ('Could not open file using provided filename.')
			sys.exit()
			

def AverageTurnaround(processCompletionTimes, processArrivalTimes):
	
	averageTurnaround = 0.0
	numProcesses = 0
	turnaroundTimes = []
	
	completionTimes = list(processCompletionTimes)
	arrivalTimes = list(processArrivalTimes)
	
	for i in range(len(processCompletionTimes)):
		turnaroundTimes.append(int(completionTimes[i]) - int(arrivalTimes[i]))
		numProcesses += 1
		
	turnaroundSum = sum(turnaroundTimes)
	averageTurnaround = float(turnaroundSum / numProcesses)
		
	return averageTurnaround, turnaroundTimes

def AverageWait(processTurnaroundTimes, processBurstTime):
	
	averageWait = 0.0
	numProcesses = 0
	waitTimes = []
	
	turnaroundTimes = list(processTurnaroundTimes)
	burstTimes = list(processBurstTime)
	
	for i in range(len(turnaroundTimes)):
		waitTimes.append(int(turnaroundTimes[i]) - int(burstTimes[i]))
		numProcesses += 1

	waitSum = sum(waitTimes)
	averageWait = float(waitSum / numProcesses)
	return averageWait

def FirstComeFirstServedSort(batchFileData):
	
	startTime = []
	endTime = []
	sTime = 0
	
	sortedProcesses = sorted(batchFileData, key=lambda x: (int(x.arrivalTime), x.pid))
	
	sortedPids = [o.pid for o in sortedProcesses]
	completeTimes = [o.burstTime for o in sortedProcesses]
	arrivalTimes = [o.arrivalTime for o in sortedProcesses]
	
	for i in range(len(sortedProcesses)):
		if (sTime < int(arrivalTimes[i])):
			sTime = int(arrivalTimes[i])
		startTime.append(sTime)
		sTime = sTime + int(completeTimes[i])
		eTime = sTime
		endTime.append(eTime)
		completeTimes[i] = eTime
			
	return completeTimes, sortedPids

def ShortestJobFirst(batchFileData):
	
	completeTimes = []
	
	complete = 0
	t = 0
	minimum = 999999999
	shortest = 0
	n = len(batchFileData)
	check = False
		
	sortedProcesses = sorted(batchFileData, key=lambda x: (x.pid, int(x.arrivalTime)))
	
	remainingTime = [o.burstTime for o in sortedProcesses]
	sortedPids = [o.pid for o in sortedProcesses]
	arrivalTimes = [o.arrivalTime for o in sortedProcesses]
	
	pids = []
	
	for i in range (0, n):
		remainingTime[i] = int(remainingTime[i])
		arrivalTimes[i] = int(arrivalTimes[i])
		
	while (complete != n):
		for j in range (n):
			if ((arrivalTimes[j] <= t) and (remainingTime[j] < minimum) and remainingTime[j] > 0):
				 minimum = remainingTime[j]
				 shortest = j
				 check = True
				 pids.append(sortedPids[j])
		if (check == False):
			t += 1
			continue
				
		remainingTime[shortest] -= 1
		minimum = remainingTime[shortest]
		if (minimum == 0):
			minimum = 999999999
			
		if (remainingTime[shortest] == 0):
			complete += 1
			check = False
				
			fint = t + 1
			completeTimes.append(fint)
				
		t += 1
		
	return completeTimes, pids
	
def PrioritySort(batchFileData):

	startTime = []
	endTime = []
	sTime = 0
	
	sortedProcesses = sorted(batchFileData, key=lambda x: (int(x.arrivalTime), int(x.priority), x.pid))
	
	sortedPids = [o.pid for o in sortedProcesses]
	completeTimes = [o.burstTime for o in sortedProcesses]
	arrivalTimes = [o.arrivalTime for o in sortedProcesses]
	
	for i in range(len(sortedProcesses)):
		if (sTime < int(arrivalTimes[i])):
			sTime = int(arrivalTimes[i])
		startTime.append(sTime)
		sTime = sTime + int(completeTimes[i])
		eTime = sTime
		endTime.append(eTime)
		completeTimes[i] = eTime
	
	return completeTimes, sortedPids

if __name__ == "__main__":
	main()

