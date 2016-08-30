# coding: utf-8
import FaBoProximity_VCNL4010
import time
import sys
import json
import awsiot

vcnl4010 = FaBoProximity_VCNL4010.VCNL4010()

def wait_start_reading():
    while True:
        prox = vcnl4010.readProx()
        print(prox)
        if prox < 5000:
            return
        time.sleep(10)

def wait_stop_reading():
    while True:
        prox = vcnl4010.readProx()
        print(prox)
        if prox > 7000:
            return
        time.sleep(10)

try:
    while True:
        timestamp = time.time()
        wait_start_reading()
        awsiot.mqtt.publish("bookmark", json.dumps({
            "timestamp": timestamp,
            "event": "start reading"
        }), 1)
        print("start")
        wait_stop_reading()
        awsiot.mqtt.publish("bookmark", json.dumps({
            "timestamp": timestamp,
            "event": "stop reading"
        }), 1)
        print("stop")
except KeyboardInterrupt:
    sys.exit()
