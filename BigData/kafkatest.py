python kafkatest.py p g k


# -*- coding: utf-8 -*-
import sys
import time
import json
from kafka import KafkaProducer
from kafka import KafkaConsumer
from kafka.errors import KafkaError
KAFAKA_HOST = "192.168.0.156"
KAFAKA_PORT = 9092
KAFAKA_TOPIC = "topic-20"
class Kafka_producer():
    def __init__(self, kafkahost,kafkaport, kafkatopic, key):
        self.kafkaHost = kafkahost
        self.kafkaPort = kafkaport
        self.kafkatopic = kafkatopic
        self.key = key
        print("producer:h,p,t,k",kafkahost,kafkaport,kafkatopic,key)
        bootstrap_servers = '{kafka_host}:{kafka_port}'.format(
                kafka_host=self.kafkaHost,
                kafka_port=self.kafkaPort
                )
        print("boot svr:",bootstrap_servers)
        self.producer = KafkaProducer(bootstrap_servers = bootstrap_servers
                )
    def sendjsondata(self, params):
        try:
            parmas_message = json.dumps(params,ensure_ascii=False)
            producer = self.producer
            print(parmas_message)
            v = parmas_message.encode('utf-8')
            k = key.encode('utf-8')
            print("send msg:(k,v)",k,v)
            for i in range(20):
                producer.send(self.kafkatopic, key=k, value= v, partition= i)
            producer.flush()
        except KafkaError as e:
            print (e)
class Kafka_consumer():
    def __init__(self, kafkahost, kafkaport, kafkatopic, groupid):
        self.kafkaHost = kafkahost
        self.kafkaPort = kafkaport
        self.kafkatopic = kafkatopic
        self.groupid = groupid
        self.key = key
        self.consumer = KafkaConsumer(self.kafkatopic, group_id = self.groupid,
                bootstrap_servers = '{kafka_host}:{kafka_port}'.format(
                    kafka_host=self.kafkaHost,
                    kafka_port=self.kafkaPort )
                )
    def consume_data(self):
        try:
            for message in self.consumer:
                yield message
        except KeyboardInterrupt as e:
            print (e)
def main(xtype, group, key):
    if xtype == "p":
        producer = Kafka_producer(KAFAKA_HOST, KAFAKA_PORT, KAFAKA_TOPIC, key)
        print ("===========> producer:", producer)
        for _id in range(1000000):
            params = '{"message" : "%s"}' % str(_id)
            params=[{"mesg0" :_id},{"mesg1" :_id}]
            producer.sendjsondata(params)
    if xtype == 'c':
        consumer = Kafka_consumer(KAFAKA_HOST, KAFAKA_PORT, KAFAKA_TOPIC, group)
        print ("===========> consumer:", consumer)
        message = consumer.consume_data()
        for msg in message:
            print ('msg---------------->k,v', msg.key,msg.value)
            print ('offset---------------->', msg.offset)
if __name__ == '__main__':
    xtype = sys.argv[1]
    group = sys.argv[2]
    key = sys.argv[3]
