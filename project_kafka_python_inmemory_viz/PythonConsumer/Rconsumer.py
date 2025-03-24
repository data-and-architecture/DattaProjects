
from confluent_kafka import Consumer
import logging


import redis
from redis.commands.json.path import Path
import redis.commands.search.aggregation as aggregations
import redis.commands.search.reducers as reducers
from redis.commands.search.field import TextField , NumericField ,TagField
from redis.commands.search.indexDefinition import IndexDefinition, IndexType
from redis.commands.search.query import NumericFilter , Query

logging.basicConfig(format="%(levelname)s:%(name)s:%(message)s")

class redisCleint:
    def __init__(self):
        pass

    def dataPush(self, connection, msg_list:dict):
        for key in msg_list.keys():
            redis_key = 'trips:'+key
            connection.json().set(redis_key,Path.root_path(),"trip :"+ msg_list[key])

    def redisHandler(self,msg_list : dict):
        connection = redis.Redis(host='localhost',port=6379 , decode_responses=True)
        self.dataPush( connection,msg_list)


class consume:
    def __init__(self):
        pass

    
    def delivery_report(self,err, msg):
        """Called once for each message produced to indicate delivery result."""
        if err is not None:
            print(f"Message delivery failed: {err}")
        else:
            print(f"Message delivered to {msg.topic()} [{msg.partition()}] at offset {msg.offset()}")

    # Every 10 message , it will push the data into redis.
    # we can setup , when receive the message from consmer and that to push into redis. But now , we are waiting 
    # 10 message. 
    def consumerFromKafka(self,topic, c : Consumer):
        c.subscribe(topic)
        message_count = 1
        msg_list = {}
        while True:
            msg = c.poll(1.0)
            if msg is None:
                continue
            if msg.error():
                print('Consumer error :{}'.format(msg.error()))
                continue


            msg_list[msg.key().decode('utf-8')] = msg.value().decode('utf-8')
            if message_count >= 1 :
                redisCleint().redisHandler(msg_list)
                msg_list = {}
            else :
                message_count += 1

    # Driver methods
    def RConsumer(self, c:Consumer):
        self.consumerFromKafka(['test'],c)
        #connection = redis.Redis(host='localhost',port=6379 , decode_responses=True)
        

        