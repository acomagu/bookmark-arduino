from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient

host = "aggyfr1bsx83e.iot.us-east-1.amazonaws.com"
certificatePath = "./key/e9bfb45fb9-certificate.pem.crt"
privateKeyPath = "./key/e9bfb45fb9-private.pem.key"
rootCAPath = "./key/rootCA.pem"

mqtt = AWSIoTMQTTClient("rasp-mailbox")
mqtt.configureEndpoint(host, 8883)
mqtt.configureCredentials(rootCAPath, privateKeyPath, certificatePath)
mqtt.configureAutoReconnectBackoffTime(1, 32, 20)

mqtt.connect()
