
# KAFKA Setup in Docker:


Given docker compose file will create multi node instances for kafka streaming. But due to our sample project system limitation , we are going to start single docker container. 

1. doker-compose.yml - This file has been modified with single sytem to minimize the resource utilization 


Note : Need to create minimum three controler , brokers for replication etc.. But for testing only one system.

Reference details site : ( it is already available , hence I am using this site information for reference and modified based on our needs)

https://hub.docker.com/r/apache/kafka


## Execution Steps

Command :  Go to the docker-compose.yml file directory and exeucte the following command. ( if you are familier with docker, you can execute from anywhere)

docker compose up -d 


2. About kafka (Brokers , controllers , producer and Consumer groups) , Topic , Partition and offset

Kafka is distirbuted and parallel compution middle ware system. This system will stream data from one edge to another edge. This is event based distribution system  and it is working in publish , subscripe model. Separate algorithm need to write to put the data in stream and the same way need to have aother separate algorithm for reading. 

### Clusters :
 There are systems are called brokers and working togather to perform this steaming operations. One of the broker system will work as controller for leader selection and topic maintance. Brokers are core for all the operations in the KAFKA.

### Producer : 
 This is client system and this interact with kafka stream to put the data into topics. Becuase kafka stream is not peer to peer messaging system. Producer will publish the data into the stream. 

### Consumer / Consumer group :
 Conusmer client will subscribe the stream and have to pull the messages / data. If you are planning to use more than one consumer to increase the parallel exeuction , yes it doable. Consumer can read more than one toics. 

### Topic : 
 This is secure message tunnel , data will be travelled . Each topics can be accessed by all the brokers. 

### Partition : 
 Each topics can be partition for parallel exeuction , scalability ,etc. Be default each topic has one partition. 


### Offset :
 Each message will be assigned one sequence number within each parititon . This number called offset. 

### Data:
 Data should be in key value pair. 


3. Configurations

As we are setuping sample project , we need to enable message deletion option true and auto message deletion as well.  We need to delete as based on our needs.



  -e KAFKA_NODE_ID=1 \    --> Borker id 
  -e KAFKA_PROCESS_ROLES=broker,controller \ --> it is acting as broker and controller 
  -e KAFKA_LISTENERS=PLAINTEXT://:9092,CONTROLLER://:9093 \ --> Messaging and controller listener
  -e KAFKA_ADVERTISED_LISTENERS=PLAINTEXT://localhost:9092 \ --> external listener
  -e KAFKA_CONTROLLER_LISTENER_NAMES=CONTROLLER \ --> Name of the controller 
  -e KAFKA_LISTENER_SECURITY_PROTOCOL_MAP=CONTROLLER:PLAINTEXT,PLAINTEXT:PLAINTEXT \
  -e KAFKA_CONTROLLER_QUORUM_VOTERS=1@localhost:9093 \ --> Controller port
  -e KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR=1 \  --> Replication factor
  -e KAFKA_TRANSACTION_STATE_LOG_REPLICATION_FACTOR=1 \
  -e KAFKA_TRANSACTION_STATE_LOG_MIN_ISR=1 \
  -e KAFKA_GROUP_INITIAL_REBALANCE_DELAY_MS=0 \
  -e KAFKA_NUM_PARTITIONS=3 \ --> Number of partition 


  Broker config :

  log.segment.bytes:268435456 (256 MB) --> Segment file size control , by default 1 GB. Small size reduce the throughput but improve the old data delete. 

  log.retention.ms=86400000 (1 day) -->  How long Kafka retain the message

  num.io.threads=8 --> No of thread used to handle i/o operation ,more thread improve performance in high volume environment.


  Producer Config : 

  acks=1 --> Level of acknowledgement required from broker before send message.  1 - faster , all-durability
  batch.size=65536 (64 KB) --> Maximum size   of a batch of messages sent to kafka. 
  linger.ms=5 -->  Waiting period before send batch
  compression.type=gzip --> Data Compressing type.


  Consumer configuration :

  group.id=my-consumer-group  --> Consumer group
  fetch.min.bytes=1024 (1 KB) --> Fetching min messages size
  max.poll.records=500 --> maximum number of records a consumer can fetch in one poll


  Consumer Group Management:
  auto.offset.reset=latest  --> Determines what to do when there is no initial offset or when an offset is out of range. latest is commonly used for real-time processing, as it will consume only new messages.
  enable.auto.commit=false  -->  If set to false, this requires you to manage offsets manually

  Replication and Fault Tolerance:

  replication.factor=3  --> many copies of each partition are stored across brokers.
  min.insync.replicas=2 Ensures that at least this many replicas are in sync for data to be considered written successfully


  Topic Configurations:
  retention.ms=604800000 (7 days) --> The retention time for messages in a topic
  segment.bytes=1073741824 (1 GB) --> The maximum size of each log segment in a partition


  Throughput Optimization:
  connections.max.idle.ms=600000 (10 minutes) --> Maximum time a connection can stay idle before being closed
  network.thread.pool.size=6  --> The number of threads used for handling network requests.

  Monitoring and Metrics:

  metrics.sample.window.ms=10000 (10 seconds)  --> Controls how often Kafka collects metrics
  metrics.reporters=org.apache.kafka.common.metrics.JmxReporter  --> Specifies the custom reporters that should be used for exporting metrics




4. Topic creation & Testing.. 

docker exec --workdir /opt/kafka/bin/ -it broker-1 sh

./kafka-topics.sh --bootstrap-server broker-1:19092,broker-2:19092,broker-3:19092 --create --topic test


./kafka-topics.sh --bootstrap-server localhost:9092 --create --topic test
./kafka-topics.sh --bootstrap-server broker-1:19092  --list

5. Message testing 

./kafka-console-producer.sh --bootstrap-server broker-1:19092 --topic test

./kafka-console-consumer.sh --bootstrap-server broker-1:19092 --topic test --from-beginning


6. Topic deletion and down


docker rm -f broker


7. More Common frequent problems



### 1. **High Consumer Lag**
   **Problem**: Consumers fall behind in processing messages, leading to high lag in consuming messages from Kafka topics.
   - **Cause**: Consumer cannot keep up with the rate at which producers are sending messages, or consumer processing is slow.
   - **Solution**:
     - **Increase consumer parallelism**: Add more consumers to the consumer group to distribute the load.
     - **Scale consumers**: Increase the number of consumer instances to match the number of partitions in the topic.
     - **Optimize consumer processing logic**: Ensure that consumer logic is efficient and doesn’t introduce delays (e.g., database writes, complex calculations).
     - **Use `max.poll.records`**: Set this to a value that aligns with your consumer’s processing speed.
     - **Tuning `fetch.min.bytes` and `fetch.max.wait.ms`**: Adjust these settings for better consumption throughput without overwhelming the consumer.

### 2. **Out of Memory (OOM) in Consumers or Producers**
   **Problem**: Kafka producers or consumers run out of memory due to large volumes of data being processed.
   - **Cause**: Producers or consumers are trying to load too much data into memory or are not batching messages efficiently.
   - **Solution**:
     - **Tuning `batch.size` and `linger.ms` for Producers**: Properly tune these parameters to ensure that the producer doesn’t accumulate too many messages in memory before sending them.
     - **Consumer Memory Management**: Set a lower value for `max.poll.records` to limit the number of records the consumer fetches in each poll. This reduces memory consumption.
     - **Increase JVM heap size**: Adjust the Kafka consumer or producer’s heap memory settings to provide more memory resources (e.g., `-Xmx` for the JVM).
     - **Offload to disk**: Consider using local disk or an external storage system for heavy workloads, reducing the memory burden on Kafka.

### 3. **Message Duplication**
   **Problem**: Messages are processed more than once due to reprocessing, leading to data inconsistencies.
   - **Cause**: Kafka producers or consumers may retry messages in case of failures (e.g., network issues, broker failures).
   - **Solution**:
     - **Idempotent Producers**: Enable idempotence on Kafka producers by setting `acks=all` and `enable.idempotence=true`. This ensures that the producer only writes each message once.
     - **Consumer Offset Management**: Use manual offset management (`enable.auto.commit=false`) to ensure that the consumer only processes each message once. This will allow better control over when a message is considered "processed."
     - **Exactly-Once Semantics (EOS)**: Enable Kafka's Exactly-Once Semantics (EOS) feature to guarantee no duplication of messages across producers and consumers (requires Kafka 0.11 or higher).

### 4. **Broker Unavailability or Failures**
   **Problem**: Kafka brokers fail or become unavailable, causing message delivery issues or data loss.
   - **Cause**: Kafka brokers are down, network partitions, or insufficient replication.
   - **Solution**:
     - **Replication Factor**: Set `replication.factor` to a high value (e.g., 3) to ensure data availability in case of broker failure.
     - **Min In-Sync Replicas**: Set `min.insync.replicas` to ensure a certain number of replicas are always in sync before acknowledging a write.
     - **Monitoring and Alerts**: Set up monitoring (using tools like Prometheus, JMX, or Kafka Manager) to proactively identify broker failures or issues.
     - **Zookeeper Stability**: Ensure that your Zookeeper ensemble is properly configured and stable, as Kafka relies on Zookeeper for leader election and metadata management.

### 5. **Topic Partition Imbalance**
   **Problem**: Uneven distribution of messages across partitions, leading to performance bottlenecks in some consumers while others are underutilized.
   - **Cause**: Poor partition key selection or partition skew in the topic.
   - **Solution**:
     - **Proper Partitioning Strategy**: Ensure that the partitioning key used for messages distributes data evenly across all partitions. This might involve custom partitioners or shuffling data across partitions.
     - **Rebalance Consumers**: In case of partition imbalances, manually rebalance the consumers using Kafka's consumer group rebalance APIs or by adjusting the number of consumer instances.
     - **Increase Partitions**: If certain partitions are receiving too much traffic, consider increasing the number of partitions to improve parallelism and consumer load balancing.

### 6. **Broker Disk Pressure and Storage Issues**
   **Problem**: Kafka brokers run out of disk space, leading to message delivery failures or slowdowns.
   - **Cause**: High message throughput and retention settings, or insufficient disk capacity.
   - **Solution**:
     - **Disk Monitoring**: Set up disk usage monitoring for your Kafka brokers and set alerts to avoid full disk situations.
     - **Adjust Log Retention**: Reduce `log.retention.ms` or set a maximum size for log segments (`log.segment.bytes`) to avoid brokers running out of space.
     - **Add More Disks**: Scale your Kafka brokers by adding more disk space or moving to a more scalable infrastructure (e.g., cloud storage).
     - **Log Compaction**: If retention isn't strictly needed, consider enabling log compaction on topics that don't require retaining every message.

### 7. **High Latency or Slow Processing**
   **Problem**: High latency in message delivery, impacting real-time processing performance.
   - **Cause**: Slow producers, consumers, or Kafka brokers due to resource bottlenecks or incorrect configuration.
   - **Solution**:
     - **Producer Tuning**: Adjust producer configurations like `linger.ms`, `batch.size`, and `acks` for better throughput with acceptable latency.
     - **Consumer Processing Optimization**: If the consumer is processing messages slowly, review the business logic and optimize any blocking or time-consuming operations.
     - **Broker Configuration**: Ensure that Kafka brokers have sufficient resources (CPU, memory, disk) to handle the expected throughput and that they're properly tuned (e.g., `num.network.threads`, `num.io.threads`).
     - **Optimize Kafka Clients**: Ensure that Kafka client libraries are up to date and tuned for low latency.

### 8. **Network Issues and Slow Data Transfer**
   **Problem**: Slow or inconsistent network speeds between producers, brokers, and consumers, leading to high message delivery times.
   - **Cause**: Network congestion, misconfigured network settings, or slow links.
   - **Solution**:
     - **Compression**: Use compression (`compression.type=gzip` or `snappy`) to reduce the message size and thus the amount of data transferred over the network.
     - **Network Monitoring**: Use network monitoring tools to identify and address network congestion or bottlenecks between Kafka brokers, producers, and consumers.
     - **Upgrade Network Hardware**: If network hardware is outdated or not able to handle the load, consider upgrading to more capable networking equipment.
     - **Tune Network Buffer Sizes**: Adjust Kafka's network buffer settings like `socket.receive.buffer.bytes` and `socket.send.buffer.bytes` for better throughput.

### 9. **Rebalancing Issues with Consumer Groups**
   **Problem**: Consumers experience frequent rebalances, leading to message processing delays.
   - **Cause**: Changes in the consumer group membership (e.g., adding/removing consumers) or unbalanced partition assignments.
   - **Solution**:
     - **Increase Session Timeout**: Set a higher `session.timeout.ms` for the consumer group to prevent unnecessary rebalancing due to slow consumers.
     - **Avoid Frequent Changes**: If possible, avoid frequently adding/removing consumers or modifying consumer group configurations during critical times.
     - **Use Sticky Partitioner**: In cases where you need to ensure that consumers remain assigned to their original partitions, use a sticky partitioning strategy to reduce unnecessary rebalancing.

### 10. **Incorrect or Inconsistent Message Ordering**
   **Problem**: Messages processed out of order, which can be critical for certain use cases (e.g., event-driven systems, financial transactions).
   - **Cause**: Kafka guarantees message order only within a partition. Misaligned keys or multiple producers can result in out-of-order message delivery.
   - **Solution**:
     - **Partition Key Design**: Ensure that messages that need to be processed in order share the same partition key so they’re sent to the same partition.
     - **Use Single Producer for Critical Messages**: If ordering is crucial, use a single producer for all messages in the same topic.



