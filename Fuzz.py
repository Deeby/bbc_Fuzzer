# -*- coding: utf-8 -*-
# !/usr/bin/python


from database import DatabaseManager
from communication import CommunicationManager
from winappdbg import Debug, HexDump, win32, CrashDump, Crash
from functools import wraps
from time import sleep
import threading
import shutil
import os
import time
import base64
import subprocess


class FuzzManager:
    def __init__(self):
        self.databaseManager = DatabaseManager()
        self.communicationManager = CommunicationManager()

        self.file_type = self.databaseManager.get_file_type()
        self.seed_path = self.databaseManager.get_seed_path()
        self.seed_file = self.databaseManager.get_seed_file()
        self.mutate_path = self.databaseManager.get_mutate_path()
        self.crash_path = self.databaseManager.get_crash_path()
        self.target_path = self.databaseManager.get_target_path()
        self.work_summary = None

        self.loop = self.databaseManager.get_loop()
        self.test_number = self.databaseManager.get_test_number()
        self.mutate_mode = self.databaseManager.get_mutate_mode() # windows binary or docker container

        self.pid = None
        self.debug = None
        self.event = None
        
        require_directorys = [self.seed_path, self.mutate_path, self.crash_path]
        for directory in require_directorys:
            if not os.path.exists(directory):
                os.makedirs(directory)

    def mutate(self):
        if self.mutate_mode == "binary":
            subprocess.call("bin/radamsa.exe -r seed -n {} -o testcase/%n".format(self.loop))
	elif self.mutate_mode == "docker":
	    print "docker run -d -v []:/testcase,[]:/seed --name=radamsa bongbongco88/radamsa"
				
    def execute(self):
        print "# {} Opening mutate file to target by bbcFuzzer".format(self.test_number)
        print(["{}".format(self.target_path), "{}\\{}".format(self.mutate_path, self.test_number)])
        try:
            _debug = Debug(self.check_crash, bKillOnExit = True)
            _debug.execv(["{}".format(self.target_path), "{}\\{}".format(self.mutate_path, self.test_number)])
            _debug.loop()
        except WindowsError:
            self.communicationManager.alert("Failed execute")
            print "Failed execute"
        finally:
            self.add_test_number()
            _debug.stop()

    def check_crash(self, event):
	code = event.get_event_code()
	self.event = event

	if code == win32.EXCEPTION_DEBUG_EVENT and event.is_last_chance():
	    self.dump() 
	
    def dump(self):
	crash = Crash(self.event)
	crash.fetch_extra_data(self.event)
	report = crash.fullReport(False)

	crash_type = report.split('\n')[2].split(':')[1]
		
	self.work_summary = crash_type + '_' + str(time.time())
			
	report_descriptor = open("{}/{}/report.txt".format(self.crash_path, self.work_summary), 'w')
	report_descriptor.write(report)
        report_descriptor.close()
          
        self.save_report(crash_type, report)
        self.copy_case()

        print "Exception Occurred"
        self.communicationManager.alert("Exception Occurred")
        self.communicationManager.alert(report)
        self.event.get_process().kill()

    def save_report(self, crash_type, report):
        mutate_descriptor = open("{}/{}".format(self.mutate_path, self.test_number), 'r')
        mutate_content = mutate_descriptor.read()

        seed_descriptor = open("{}/{}".format(self.seed_path, self.seed_file), 'r')
        seed_content = seed_descriptor.read()
        
        crash_information = (self.target_path, crash_type, self.file_type, report, base64.encodestring(mutate_content), base64.encodestring(seed_content)) 
        self.databaseManager.set_crash(crash_information)

    def copy_case(self):
	os.mkdir("./{}/{}".format(self.crash_path, self.work_summary))
	shutil.copyfile("{}/{}".format(self.mutate_path, self.test_number), "{}/{}/{}".format(self.crash_path, self.work_summary, self.test_number))

    def _check_count(func): 
	@wraps(func)
	def wrapper(self, *args, **kwargs):
	    if self.test_number > self.loop:
		print "Completed Fuzzing Test"
                shutil.copy('fuzzHistory.db', self.crash_path)  
		exit()
			
	    return func(self, *args, **kwargs) 
	return wrapper

    @_check_count
    def fuzz(self):
	fuzz_thread = threading.Thread(target=self.execute)	
	fuzz_thread.setDaemon(0)
	fuzz_thread.start()
        sleep(5)

    def add_test_number(self):
        self.test_number = self.test_number + 1
        if self.test_number % 100 == 0:
            self.databaseManager.set_test_number(self.test_number)
            for complete_test_file in range(self.test_number - 100, self.test_number):
                os.remove("./{}/{}".format(self.mutate_path, complete_test_file))

    def start(self):
	mutate_thread = threading.Thread(target=self.mutate)
	mutate_thread.setDaemon(0)
	mutate_thread.start()
	while True:
	    self.fuzz()


if __name__=="__main__":
    fuzzManager = FuzzManager()
    fuzzManager.start()
