# -*- coding: utf-8 -*-
# !/usr/bin/python


from functools import wraps
import os
import sqlite3
from hashlib import sha224


class DatabaseManager:
    def __init__(self):
        self.database_name = "fuzzHistory.db" 
        self.connect = None
        self.cursor = None
        
        if not os.path.isfile(self.database_name):
            self.create_database()
            self.create_table()
            self.set_master()
            self.set_setting()

    def set_master(self):
        sql = "insert into master (master_code, master_chat_id, api_code) values ('{}', '{}', '{}')".format(sha224("password").hexdigest(), "chat_id", "api_code")
        self.execute(sql, "set")

    def set_setting(self):
        sql = "insert into setting (file_type, seed_path, seed_file, mutate_path, crash_path, target_path, loop, test_number, mutate_mode) values ('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}')".format("aiff", "seed", "seed", "testcase", "crash", "C:\\Program Files (x86)\\GRETECH\\GOMAudio\\Goma.exe", 1000, 1, "binary")
        self.execute(sql, "set")

    def _connect_fuzz_history(func): 
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            self.connect = sqlite3.connect(self.database_name, isolation_level=None) 
            self.cursor = self.connect.cursor()
            return func(self, *args, **kwargs)
        return wrapper

    def _close_fuzz_history(self):
        self.connect.commit()        
        self.connect.close()
   
    @_connect_fuzz_history
    def create_database(self):
        print "DatabaseManager: Ready to new fuzzing project" 
        self._close_fuzz_history()
    
    @_connect_fuzz_history
    def create_table(self):
        sql_communication = """create table if not exists communication (
            id integer PRIMARY KEY,
            chat_id text NOT NULL,
            update_id text NOT NULL,
            master BOOLEAN NOT NULL,
            Timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            );"""
        
        sql_fuzz = """create table if not exists fuzz (
            id integer PRIMARY KEY,
            target text NOT NULL,
            crash_type text NOT NULL,
            report text NOT NULL,
            mutate_file text NOT NULL,
            seed_file text NOT NULL,
            Timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        );"""
        
        sql_master = """create table if not exists master (
            id integer PRIMARY KEY,
            master_code text NOT NULL,
            master_chat_id text NOT NULL,
            api_code text NOT NULL,
            Timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        );"""
        
        sql_setting = """create table if not exists setting (
            id integer PRIMARY KEY,
            file_type text NOT NULL,
            seed_path text NOT NULL,
            seed_file text NOT NULL,
            mutate_path text NOT NULL,
            crash_path text NOT NULL,
            target_path text NOT NULL,
            loop integer NOT NULL,
            test_number integer NOT NULL,
            mutate_mode text NOT NULL,
            Timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        );"""
        tables = [sql_communication, sql_fuzz, sql_master, sql_setting]
        for table in tables:
            self.cursor.execute(table)

        self._close_fuzz_history()

    def set_crash(self, crashInformation):
        sql = "insert into fuzz (target, crash_type, report, mutate_file, seed_file) values ('{}','{}','{}','{}','{}')".format(crashInformation[0], crashInformation[1], crashInformation[2], crashInformation[3], crashInformation[4])
        self.execute(sql, "set")

    def get_crash(self):
        sql = "select * from fuzz"
        return self.execute(sql, "get")

    def get_report(self, target):
        sql = "select target, crash_type, report, Timestamp from fuzz where target like '%{}%'".format(target)
        return self.execute(sql, "get")

    def get_targets(self):
        sql = "select target from fuzz"
        return self.execute(sql, "get")

    def set_request(self, conversation):
        sql = "insert into communication (chat_id, update_id, master) values ('{}','{}','{}')".format(conversation[0], conversation[1], conversation[2])
        self.execute(sql, "set")

    def get_master_chat_id(self):
        sql = "select master_chat_id from master"
        return self.execute(sql, "get")[0][0]
    
    def set_master_chat_id(self, masterChatID):
        sql = "update master set master_chat_id='{}'".format(masterChatID)
        self.execute(sql, "set")

    def get_api_code(self):
        sql = "select api_code from master"
        return self.execute(sql, "get")[0][0]

    def get_completed(self):
        sql = "select update_id from communication order by id desc limit 1"
        return self.execute(sql, "get")[0][0]
   
    def get_master_code(self):
        sql = "select master_code from master"
        return self.execute(sql, "get")[0][0]

    def set_api_code(self, apiCode):
        sql = "update master set api_code='{}'".format(apiCode)
        self.execute(sql, "set")

    def set_master_code(self, masterCode):
        sql = "update master set master_code='{}'".format(masterCode)
        self.execute(sql, "set")

    def get_file_type(self):
        sql = "select file_type from setting"
        return self.execute(sql, "get")[0][0]
    
    def get_seed_path(self):
        sql = "select seed_path from setting"
        return self.execute(sql, "get")[0][0]
    
    def get_seed_file(self):
        sql = "select seed_file from setting"
        return self.execute(sql, "get")[0][0]
    
    def get_mutate_path(self):
        sql = "select mutate_path from setting"
        return self.execute(sql, "get")[0][0]
    
    def get_crash_path(self):
        sql = "select crash_path from setting"
        return self.execute(sql, "get")[0][0]
    
    def get_target_path(self):
        sql = "select target_path from setting"
        return self.execute(sql, "get")[0][0]
    
    def get_loop(self):
        sql = "select loop from setting"
        return self.execute(sql, "get")[0][0]

    def get_test_number(self):
        sql = "select test_number from setting"
        return self.execute(sql, "get")[0][0]

    def set_test_number(self, test_number):
        sql = "update setting set test_number='{}'".format(test_number)
        self.execute(sql, "set")

    def get_mutate_mode(self):
        sql = "select mutate_mode from setting"
        return self.execute(sql, "get")[0][0]

    @_connect_fuzz_history 
    def execute(self, sql, mode):
        self.cursor.execute(sql)
        if mode == "get":
            rows = self.cursor.fetchall()
            self._close_fuzz_history()
            return rows
        elif mode == "set":
            self._close_fuzz_history()
