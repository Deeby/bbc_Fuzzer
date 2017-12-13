from winappdbg import System
from fuzz import FuzzManager
from communication import CommunicationManager
from database import DatabaseManager
import threading


class Secretary:
    def __init__(self):
        self.fuzzManager = FuzzManager()
        self.communicationManager = CommunicationManager()
        self.databaseManager = DatabaseManager()

        self.setting()

    def setting(self):
        self.databaseManager.set_system_bit(System.bits)

    def working(self):
        communicationManager_thread = threading.Thread(target=self.communicationManager.start)
        communicationManager_thread.setDaemon(0)
        communicationManager_thread.start()

        self.fuzzManager.start()

    def start(self):
        self.working()
