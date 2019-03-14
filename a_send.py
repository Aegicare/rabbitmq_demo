#!/usr/bin/env python
import pika

# if use IP address, you'll get 403 ACCESS_REFUSED
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.queue_declare(queue='hello')

channel.basic_publish(exchange='',
                      routing_key='hello',
                      body='Hello World!')
print(" [x] Sent 'Hello World!'")

connection.close()

# run `rabbitmqctl list_queues` to see what queues RabbitMQ has and how many messages are in them
# Timeout: 60.0 seconds ...
# Listing queues for vhost / ...
# name    messages
# hello   1
