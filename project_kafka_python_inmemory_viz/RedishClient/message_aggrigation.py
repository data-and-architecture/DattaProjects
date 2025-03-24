

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

    def dataRead(self, connection):
        schema = (
            NumericField("$.trip.VendorID",as_name="vendor")
        )
       # connection.ft().create_index(schema
       #                              ,definition=IndexDefinition(prefix=["Trips:"],
        #                                                               index_type=IndexType.JSON))
        
        #req = aggregations.AggregateRequest("*").group_by([],reducers.count().alias("total"))
        req = Query("*")
        rows = connection.ft().search(req)
        #rows = connection.ft().aggregate(req).rows
        print(rows)
        #connection.json().set('',Path.root_path(),msg_list)

    def redisClientHandler(self):
        connection = redis.Redis(host='localhost',port=6379 , decode_responses=True)
        self.dataRead(connection)

def main():
    redisCleint().redisClientHandler()

if __name__ =="__main__":
    main()