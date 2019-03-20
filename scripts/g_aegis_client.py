#!/usr/bin/env python
import pika
import uuid


class AegisRpcClient(object):
    def __init__(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        self.channel = self.connection.channel()

        result = self.channel.queue_declare(exclusive=True)
        self.callback_queue = result.method.queue

        self.channel.basic_consume(self.on_response, no_ack=True, queue=self.callback_queue)

    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = body

    def call(self, data):
        self.response = None
        self.corr_id = str(uuid.uuid4())

        self.channel.basic_publish(exchange='',
                                   routing_key='aegis_queue',
                                   properties=pika.BasicProperties(
                                       reply_to=self.callback_queue,
                                       correlation_id=self.corr_id,
                                       delivery_mode=2,  # make message persistent
                                   ),
                                   body=str(data))
        while self.response is None:
            self.connection.process_data_events()
        return self.response


def handle_weaver_result(response):
    # result success or fail
    print(" [.] Got result %r" % response)
    # handle result


print(" [x] Requesting Sample vcf analysis result")
aegis_rpc = AegisRpcClient()
# sample_no = 'AS3000-err'
sample_no = 'AS1000-suc'
response = aegis_rpc.call(sample_no)
handle_weaver_result(response)
