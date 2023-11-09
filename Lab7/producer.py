#!/usr/bin/env python
import pika
import sys
from crawler import scrap
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.exchange_declare(exchange='logs', exchange_type='fanout')
links = scrap('https://999.md/ru/list/transport/cars', 1)
for link in links:
    message = link
    channel.basic_publish(
        exchange='logs',
        routing_key='',
        body=message,
        properties=pika.BasicProperties(
            delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
        ))
    print(f" [x] Sent {message}")
connection.close()