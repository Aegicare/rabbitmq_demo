#!/usr/bin/env python
import datetime
import time
import pika

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()
channel.queue_declare(queue='aegis_queue', durable=True)


def vep(sample_no):
    time.sleep(30)
    if sample_no.endswith('err'):
        result = 'err'
    else:
        result = 'suc'
    return '{}-{}'.format(result, datetime.datetime.now())


def on_request(ch, method, props, body):
    """
    :param ch: channel: BlockingChannel
    :param method: method: spec.Basic.Deliver
    :param props: properties: spec.BasicProperties
    :param body: body: str or unicode
    :return:
    """
    sample_no = str(body)

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
