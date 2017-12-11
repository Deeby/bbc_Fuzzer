from fuzz import FuzzManager
from communication import CommunicationManager
from threading


class Secretary:
    def __init__(self):
        self.fuzzManaser = FuzzManager()
        self.communicationManager = CommunicationManager()
        self.team =[self.fuzzManager, self.communicationManager]

    def work_start(self):
        for member in self.team:
            working = threading.Thread(target=member.start)
            working.setDaemon(0)
            working.start()

    def start(self):
        self.work_start()
