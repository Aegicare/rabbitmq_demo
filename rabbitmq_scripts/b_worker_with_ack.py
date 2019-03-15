import time

import pika


def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)
    time.sleep(body.count(b'.'))
    print(" [x] Done")
    ch.basic_ack(delivery_tag=method.delivery_tag)


connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.queue_declare(queue='task_queue', durable=True)
print(' [*] Waiting for messages. To exit press CTRL+C')

channel.basic_qos(prefetch_count=3)
channel.basic_consume(callback,
                      queue='task_queue')
channel.start_consuming()

# It's a common mistake to miss the basic_ack.
# rabbitmqctl.bat list_queues name messages_ready messages_unacknowledged
