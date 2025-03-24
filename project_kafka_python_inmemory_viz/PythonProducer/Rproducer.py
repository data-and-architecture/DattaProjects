import pyarrow.parquet as pq
import time
import pandas as pd
from confluent_kafka import Producer
import logging
logging.basicConfig(format="%(levelname)s:%(name)s:%(message)s")

class produce:
    def __init__(self):
        self.p = None
        self.row = None
    
    def KafkaConnect(self,param):
        try:
            self.p =  Producer(param)
        except Exception as e:
            print("The error is: ",e)

    # Converting parquet to json . As don't have direct method in pyarrow . Just using pandas for conversion
    def ConvertPqtoJSON(self, row ):
        self.row = None
        df_parquet : pd.DataFrame = row.to_pandas()
        for index , row in df_parquet.iterrows():
            self.row = row.to_json()

    
    def delivery_report(self,err, msg):
        """Called once for each message produced to indicate delivery result."""
        if err is not None:
            print(f"Message delivery failed: {err}")
        else:
            print(f"Message delivered to {msg.topic()} [{msg.partition()}] at offset {msg.offset()}")


    def ProduceToKafka(self,topic, key):
         #print(self.row)
         self.p.produce(topic, key=key, value=self.row, callback=self.delivery_report)
         self.p.flush()


    # Driver methods
    def RProducer(self,filepath , kafkaConfig):
        
        #Getting kafka Connection. Once get the connect and will use in multiple times
        self.KafkaConnect(kafkaConfig)

        # Reading file
        parquet_file = pq.ParquetFile(filepath)
        key_counter = 1 
        for row in parquet_file.iter_batches(batch_size=1):
            self.ConvertPqtoJSON(row)
            self.ProduceToKafka('test',str(key_counter))
            time.sleep(5)
            # Break control just for testing . 
            # After testing , remove this block of code.
            if key_counter >= 1 :
                print('Coming out')
                break
            else:
                key_counter += 1