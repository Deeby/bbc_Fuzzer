# -*- coding: utf-8 -*-
# !/usr/bin/python

import telegram

class CommunicationManager:
    def __init__(self):
        self.chat_id = None
        self.text = None
        self.manager = None 
        self.apiCode = None
        self.tasks = None
        self.taskCode = None
        self.completed = None
    
    def getManager(self):
        self.manager = telegram.Bot(self.apiCode) 
    
    def getApiCode(self):
        self.apiCode = ""
    
    def setMaster(self):
        self.chat_id = ""

    def setComplete(self):
        self.completed = self.task.update_id
   
    def updateTask(self):
        self.tasks = self.manager.get_updates(offset=self.completed, timeout=10)

    def sendMsg(self):
        self.manager.send_message(self.chat_id, self.text)

    #def sendFile(self):

    def classify(self):
        if self.task.message.text == "/start":
            self.text = "Welcome"
            self.taskCode = None
        elif self.task.message.text == "/getdump":
            self.text = "Sending dump"
            self.taskCode = None
        elif self.task.message.text == "/getstate":
            self.text = "Sending state"
            self.taskCode = None
        elif self.task.message.text == "/changeseed":
            self.text = "Changing Seed file"
            self.taskCode = None
        elif self.task.message.text == "/changetarget":
            self.text = "Changing Target Program"
            self.taskCode = None
        elif self.task.message.text == "/help":
            self.text = "Command List"
            self.taskCode = None
        else:
            self.text = "I like talk but I'm busy. Sorry ..."
            self.taskCode = None
        
    def action(self):
        if self.taskCode == None:
            self.sendMsg()

    def working(self):
        self.getApiCode()
        self.getManager()
        self.setMaster()
        
        while True:
            self.updateTask()
            for self.task in self.tasks:
                if self.completed == self.task.update_id:
                    continue
                self.classify()
                self.action() 
                self.setComplete()

    def start(self):
        self.working()


if __name__=="__main__":
    communicationManager = CommunicationManager()
    communicationManager.start()
