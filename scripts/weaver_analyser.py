#!/usr/bin/env python
import pika
import json

connection = pika.BlockingConnection(
    pika.ConnectionParameters(
        host='192.168.56.50',
        port=5672,
        virtual_host='aegis_vhost',
        credentials=pika.PlainCredentials('aegis', 'aegicare123'),
    )
)
channel = connection.channel()
channel.queue_declare(queue='aegis_queue', durable=True)


def fib_recursion(n):
    """ 故意让时间很长很长"""
    if n <= 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fib_recursion(n - 1) + fib_recursion(n - 2)


def vep(n):
    result_list = []
    for i in range(n):
        result = fib_recursion(i)
        result_list.append(result)
    return result_list


def on_request(ch, method, props, body):
    """
    :param ch: channel: BlockingChannel
    :param method: method: spec.Basic.Deliver
    :param props: properties: spec.BasicProperties
    :param body: body: str or unicode
    :return:
    """
    data = json.loads(body.decode("utf-8"))
    sample_no = data[0][0]
    sample_no = 3

    print(" [.] Input Sample %s" % sample_no)
    response = vep(sample_no)
    print(" [.] Output %s" % response)

    ch.basic_publish(exchange='',
                     routing_key=props.reply_to,
                     properties=pika.BasicProperties(
                         correlation_id=props.correlation_id,
                         delivery_mode=2,  # make message persistent
                     ),
                     body=str(response))
    ch.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_qos(prefetch_count=5)
channel.basic_consume(on_request, queue='aegis_queue')

print(" [x] Awaiting RPC requests")
channel.start_consuming()

# How should the client react if there are no servers running?
# Should a client have some kind of timeout for the RPC?
# If the server malfunctions and raises an exception, should it be forwarded to the client?
# Protecting against invalid incoming messages (eg checking bounds) before processing.
