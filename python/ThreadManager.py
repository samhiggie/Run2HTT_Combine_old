#brief class for creating and running our combine fits in seperate threads and dumping the output 
#in a safe easily manageable way.
import os 
import threading

class ThreadManager():
    def __init__(self):
        self.Threads = []
    def StartNewFit(self,CombineCommand,Parameter,OutputDir):
        NewThread = threading.Thread(target=self.RunCombineCommand,args=(CombineCommand,Parameter,OutputDir))
        NewThread.start()
        self.Threads.append(NewThread)
    def RunCombineCommand(self,CombineCommand,Parameter,OutputDir):
        os.system(CombineCommand+" >& "+OutputDir+"Fit_"+Parameter+".txt")
    def WaitForAllThreadsToFinish(self):
        print("Waiting for threads...")
        for Process in self.Threads:
            Process.join()
        print("All fits finished running!")
