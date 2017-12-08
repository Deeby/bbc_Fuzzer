from winappdbg import Debug, HexDump, win32, CrashDump, Crash
from functools import wraps
from time import sleep
import threading
import shutil
import os
import time
import subprocess

class FuzzManager:
	def __init__(self):
                self.mutatemode = None # radamsa windows binary/docker container
		self.seedPath = "seed"
                self.seedFile = "seed"
		self.mutatePath = "testcase"
		self.crashPath = "crash"
                self.targetPath = "C:\\Program Files (x86)\\VUPlayer\\VUPlayer.exe"
                self.crashType = None
                self.workSummary = None

		self.loop = 10 # 10000
		self.testNumber = 0
                self.mutatemode = "binary"
	
                self.pid = None
                self.debug = None
                self.event = None

        def mutate(self):
                print "mutate"
                if self.mutatemode == "binary":
                    print "bin/radamsa.exe -r seed -n "+ str(self.loop) +" -o testcase/%n"
                    subprocess.call("bin/radamsa.exe -r seed -n "+ str(self.loop) +" -o testcase/%n")
                elif self.mutatemode == "docker":
                    print "docker run -d -v []:/testcase,[]:/seed --name=radamsa bongbongco88/radamsa"
                        
	def execute(self):
		print "target Execute"	
		print(self.targetPath, self.mutatePath + "/" + str(self.testNumber))
                try:
                    self.debug = Debug(self.checkCrash, bKillOnExit = True)
                    #self.debug = Debug(bKillOnExit = True)
                    self.debug.execv([self.targetPath, "./" + self.mutatePath+'/'+str(self.testNumber)])
                    self.debug.execv([self.targetPath, "./" + self.mutatePath+'/'+str(self.testNumber)])
	            self.debug.loop()
                except e:
                    print e

	def checkCrash(self, event):
		print "target Debug"
                code = event.get_event_code()
                self.event = event

                if code == win32.EXCEPTION_DEBUG_EVENT and event.is_last_chance():
                    self.dump() 
                print "No Exception Occurred"
                self.debug.stop()

        def dump(self):
            try:
                crash = Crash(self.event)
                crash.fetch_extra_data(self.event)
                crashInfo = crash.fullReport(False)

                self.crashType = crashInfo.split('\n')[2].split(':')[1]
                
                self.workSummary = crashType + '_' + str(time.time())
                
                reportDescriptor = open(crashPath + '/' + workSummary + '/' + "report.txt", 'w')
                reportDescriptor.write(crashInfo)
                reportDescriptor.close()

                print "Exception Occurred"
                event.get_process().kill()
            except:
                pass

	def checkingCount(func): 
		@wraps(func)
		def wrapper(self, *args, **kwargs):
		       	self.testNumber = self.testNumber + 1	
                        if self.testNumber > self.loop:
				print "Completed Fuzzing Test"
				exit()
			
                        print "TestCase: ", self.testNumber	
			return func(self, *args, **kwargs) 
		return wrapper

	@checkingCount
	def fuzz(self):
                self.waitingForProcess()
		fuzzThread = threading.Thread(target=self.execute)	
		fuzzThread.setDaemon(0)
		fuzzThread.start()
	
	def caseCopy(self):
            os.mkdir('./' + self.crashPath + '/' + self.workSummary)
            
            #shutil.copyfile(self.seedPath + '/' + self.seedFile, self.crashPath + '/' + self.workSummary + '/' + self.seedFile) 
            shutil.copyfile(self.mutatePath + '/' + self.testNumber, self.crashPath + '/' + self.workSummary + '/' + self.testNumber)


	def waitingForProcess(self):
		counter = 0
		while self.pid == None:
			if counter < 5:
				sleep(1)
				counter = counter + 1
				if counter >= 5:
                                    break
        
        def setMutateMode(self, mode):
                self.mutatemode = mode

	def start(self):
                mutateThread = threading.Thread(target=self.mutate)
                mutateThread.setDaemon(0)
                mutateThread.start()
                while True:
			self.fuzz()	


def main():
	fuzzManager = FuzzManager()
	fuzzManager.start()

if __name__ == "__main__":
	main()
