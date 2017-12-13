from fuzz import FuzzManager
from communication import CommunicationManager
from multiprocessing import Pool


class Secretary:
    def __init__(self):
        self.fuzzManager = FuzzManager()
        self.communicationManager = CommunicationManager()

    def work_start(self):
        pool = Pool(processes=1)
        pool.map(self.communicationManager.start, '')

        self.fuzzManager.start()

    def start(self):
        self.work_start()
