# coding: utf-8
import FaBoProximity_VCNL4010
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import time
import sys

vcnl4010 = FaBoProximity_VCNL4010.VCNL4010()

host = "aggyfr1bsx83e.iot.us-east-1.amazonaws.com"
certificatePath = "./key/e9bfb45fb9-certificate.pem.crt"
privateKeyPath = "./key/e9bfb45fb9-private.pem.key"
rootCAPath = "./key/rootCA.pem"

mqtt = AWSIoTMQTTClient("rasp-mailbox")
mqtt.configureEndpoint(host, 8883)
mqtt.configureCredentials(rootCAPath, privateKeyPath, certificatePath)
mqtt.configureAutoReconnectBackoffTime(1, 32, 20)

mqtt.connect()

def count(n, i):
    time.sleep(1)
    if n is 0:
        i += 1
        print("ALERT")
        mqtt.publish("alert", i, 1)
        return
    prox = vcnl4010.readProx()
    print("Prox = ", prox)
    if prox > 7000:
        count(n-1, i)

try:
    while True:
        count(10, 0)


except KeyboardInterrupt:
    sys.exit()
