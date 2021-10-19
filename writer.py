import logging
import os
import string
import sys
import syslog
import time
from collections import deque
import pandas as pd

import aof
import data_process
import reader
import threading

import recall

stop_flag = False

mutex = threading.Lock()


class formWriter:
    def __init__(self, config_name: string):
        self.writeConfig = dict()
        self.config_name = config_name
        self.persis_threads = []
        self.backup_buffer = deque()
        self.preprocess = None

    def start(self):
        preprocess, ok = recall.get_preprocess_recall()
        if ok:
            self.preprocess = preprocess
        self.load_config(self.config_name)
        for t in self.persis_threads:
            t.start()

    def load_config(self, config_name):
        config = reader.json_read(config_name)
        if config is None:
            logging.error("config file is not exist in this dictionary, please check")
            sys.exit(-1)
        for form_name, form_config in config.items():
            f = form(form_name, form_config)
            self.writeConfig[form_name] = f
            t = threading.Thread(target=f.persist, daemon=True)
            self.persis_threads.append(t)

    def __del__(self):
        self.close()

    def close(self):
        global stop_flag
        stop_flag = True
        for t in self.persis_threads:
            t.join()
        logging.info("close completed")

    def write_data(self, data: dict):
        if self.preprocess is not None:
            data = self.preprocess(data)
        for form in self.writeConfig.values():
            if not form.write(data):
                return False
        aof.write_aof(data)
        return True


class form:
    def __init__(self, name, config: dict):
        self.name = name
        for key, value in config.items():
            if value is None or value == "":
                logging.error("config content can not be '""', check form: {}: {}".format(name, key))
                sys.exit(-1)
        self.file_path = config["filePath"]
        self.file_name = config["fileName"]
        self.file_type = config["fileType"]
        self.fields = config["fields"]
        self.entity = {v: "" for k, v in self.fields.items()}
        self.recall_enable = False
        self.buffer = deque()
        if "recall" in config.keys():
            if recall.is_registered(config["recall"]):
                self.recall = recall.get_recall(config["recall"])
                self.recall_enable = True

    def contain(self, in_field):
        return self.fields.__contains__(in_field)

    def write(self, data):
        entry = dict.copy(self.entity)
        is_blank_row = True
        for in_field, field in self.fields.items():
            if data.__contains__(in_field):
                entry[field] = [data[in_field]]
                is_blank_row = False
        if not stop_flag and not is_blank_row:
            if self.recall_enable:
                entry = self.recall(entry)
            self.buffer.append(entry)
            return True
        elif is_blank_row:
            return True
        return False

    def persis_to_excel(self, entry):
        df = pd.DataFrame(entry)
        mutex.acquire()
        if not os.path.exists(self.file_path):
            os.makedirs(self.file_path)
        mutex.release()
        path = self.file_path + self.file_name + ".xlsx"
        if not os.path.exists(path):
            open(path, 'w')
            writer = pd.ExcelWriter(path, mode='a')
            df.to_excel(writer, sheet_name="Sheet1", index=False)
        writer = pd.ExcelWriter('123.xlsx', mode='a')
        df.to_excel(writer, sheet_name='sheet1')
        writer.save()

    def persis_to_csv(self, entry):
        df = pd.DataFrame(entry)
        mutex.acquire()
        if not os.path.exists(self.file_path):
            os.makedirs(self.file_path)
        mutex.release()
        path = self.file_path + self.file_name + ".csv"
        if not os.path.exists(path):
            # open(path, 'w')
            df.to_csv(self.file_path + self.file_name + ".csv", index=False, mode='w')
        else:
            df.to_csv(self.file_path + self.file_name + ".csv", index=False, mode='a', header=False)

    def persist(self):
        while True:
            if len(self.buffer) > 0:
                entry = self.buffer.popleft()
                if self.file_type == "csv":
                    self.persis_to_csv(entry)
                elif self.file_type == "xlsx":
                    self.persis_to_excel(entry)
            elif stop_flag:
                break
            else:
                time.sleep(0.1)


if __name__ == '__main__':
    data_process.init()
    fm = formWriter("config.json")
    fm.start()
    data = {"country": "CH", "name": "shen"}
    data2 = {"country": "CH"}
    for i in range(10):
        fm.write_data(data)
        fm.write_data(data2)
    time.sleep(10)
