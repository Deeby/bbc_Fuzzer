# -*- coding: utf-8 -*-
# !/usr/bin/python


from database import DatabaseManager
import telegram
from functools import wraps
from hashlib import sha224


class CommunicationManager:
    def __init__(self):
        self.databaseManager = DatabaseManager()
        self.chat_id = int(self.databaseManager.get_master_chat_id())
        self.text = None
        self.api_code = self.databaseManager.get_api_code()
        self.manager = telegram.Bot(self.api_code)
        self.tasks = None
        self.task_code = None
        try:
            self.completed = self.databaseManager.get_completed()
        except:
            self.completed = None
        self.check_master = False
    
    def set_master_chat_id(self):
        self.databaseManager.set_master_chat_id(self.chat_id)

    def set_complete(self):
        self.completed = self.task.update_id
        conversation = (self.chat_id, self.completed, self.check_master)
        self.databaseManager.set_request(conversation)
   
    def update_task(self):
        self.tasks = self.manager.get_updates(offset=self.completed, timeout=10)

    def send_message_(self):
        self.manager.send_message(self.chat_id, self.text)

    def get_report(self):
        return self.databaseManager.get_crash() 
    
    def is_master(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            if self.task.message.text[:7] =="/master":
                try:
                    master_code = self.task.message.text.split(':')[1]
                except IndexError:
                    master_code = "NotMaster because don't know usage."
                
                if sha224(master_code).hexdigest() == self.databaseManager.get_master_code():
                    self.check_master = True
                    self.chat_id = self.task.message.chat_id
                    self.set_master_chat_id()
                    self.task.message.text = "/master"
                else:
                    self.task.message.text = "/notmaster"
                    self.check_master = False

            elif self.task.message.chat_id == int(self.databaseManager.get_master_chat_id()) :
                self.check_master = True
            else:   
                self.task.message.text = "/notmaster"
                self.check_master = False
            return func(self, *args, **kwargs)
        return wrapper

    @is_master
    def classify(self):
        if self.task.message.text == "/start":
            self.text = "Welcome"
            self.task_code = None
        elif self.task.message.text == "/report":
            try:
                target = self.task.message.text.split(':')[1]
                self.text = self.databaseManager.get_report(target)
            except IndexError:
                self.text = "usage: /report:[target]\n\n If you want to target list, send me command \"/targets\"" 
            
            self.task_code = None
        elif self.task.message.text == "/targets":
            self.text = self.databaseManager.get_targets()
            self.task_code = None
        elif self.task.message.text == "/changeseed":
            self.text = "Changing Seed file"
            self.task_code = None
        elif self.task.message.text == "/changetarget":
            self.text = "Changing Target Program"
            self.task_code = None
        elif self.task.message.text == "/help":
            self.text = "Command List\n  /targets\n  report:[target]"
            self.task_code = None
        elif self.task.message.text == "/master":
            self.text = "Hello, master. You check in at conference room."
            self.task_code = None
        elif self.task.message.text == "/notmaster":
            self.task_code = None
            self.text = "Why do not you hire your secretary?"
        else:
            self.text = "I like talk but I'm busy. Sorry ..."
            self.task_code = None
        
    def action(self):
        if self.task_code == None:
            self.send_message_()

    def working(self):
        while True:
            self.update_task()
            for self.task in self.tasks:
                if self.completed == self.task.update_id:
                    continue
                self.classify()
                self.action() 
                self.set_complete()

    def start(self):
        self.working()
