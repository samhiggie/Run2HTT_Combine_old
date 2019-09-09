#brief class for creating and running our combine fits in seperate threads and dumping the output 
#in a safe easily manageable way.
import os 
import threading
import Queue

class ThreadManager():
    def __init__(self,NumThreads):
        self.NumThreads = NumThreads
        self.Threads = []
        self.CommandQueue = Queue.Queue()
        self.ParameterQueue = Queue.Queue()
        self.OutputDirQueue = Queue.Queue()
        self.queueLock = threading.Lock()    

    def RunThread(self):
        while not self.CommandQueue.empty():
            self.queueLock.acquire()
            CombineCommand = self.CommandQueue.get()
            OutputDir = self.OutputDirQueue.get()
            Parameter = self.ParameterQueue.get()
            self.queueLock.release()
            print("Starting fit for "+Parameter+"...")
            FinishStatus = os.system(CombineCommand+" >& "+OutputDir+"Fit_"+Parameter+".txt")
            print("Finished fit for: "+Parameter+" With status: "+str(FinishStatus))

    def WaitForAllThreadsToFinish(self):
        print("\nWaiting for threads...")
        for Process in self.Threads:
            Process.join()
        print("All fits finished running!")

    def AddNewFit(self,CombineCommand,Parameter,OutputDir):
        self.queueLock.acquire()
        self.CommandQueue.put(CombineCommand)
        self.ParameterQueue.put(Parameter)
        self.OutputDirQueue.put(OutputDir)
        self.queueLock.release()
        
    def BeginFits(self):
        if self.NumThreads > self.CommandQueue.qsize():
            self.NumThreads = self.CommandQueue.qsize()
        for i in range(self.NumThreads):
            NewThread = threading.Thread(target=self.RunThread)
            NewThread.start()
            self.Threads.append(NewThread)
