
import logging
from confluent_kafka import Consumer
from PythonConsumer import Rconsumer
logging.basicConfig(format="%(levelname)s:%(name)s:%(message)s")

class control:
    def __init__(self):
         param : dict = None
         kafkaParameter :dict =None
         c = None

        #Getting kafka parameter    
    def getKafkaParameters(self):
        kafkaParameter = self.param
        self.kafkaParameter = kafkaParameter


    def KafkaConnect(self):
        try:
            self.c =  Consumer(self.kafkaParameter)
        except Exception as e:
            print("The error is: ",e)

    def KafkaConnectClose(self):
        try:
            self.c.close()
        except Exception as e:
            print("The error is: ",e)

    # Controller of consumer
    def Controller(self,param:dict):
        self.param = param
        #print(self.param)
        self.getKafkaParameters()
        #Getting kafka Connection. Once get the connect and will use in multiple times
        self.KafkaConnect()
        Rconsumer.consume().RConsumer(self.c)
        self.KafkaConnectClose()
        #.produce().RProducer(self.fileFullPath,self.kafkaParameter)