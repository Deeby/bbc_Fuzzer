from fuzz import FuzzManager
from communication import CommunicationManager
import threading


class Secretary:
    def __init__(self):
        self.fuzzManager = FuzzManager()
        self.communicationManager = CommunicationManager()

    def work_start(self):
        communicationManager_thread = threading.Thread(target=self.communicationManager.start)
        communicationManager_thread.setDaemon(0)
        communicationManager_thread.start()

        self.fuzzManager.start()

    def start(self):
        self.work_start()
