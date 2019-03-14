#!/usr/bin/env python
import pika
import uuid


class FibonacciRpcClient(object):
    # We establish a connection, channel and declare an exclusive 'callback' queue for replies
    def __init__(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))

        self.channel = self.connection.channel()

        result = self.channel.queue_declare(exclusive=True)
        self.callback_queue = result.method.queue

        self.channel.basic_consume(self.on_response, no_ack=True, queue=self.callback_queue)

    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = body

    def call(self, n):
        self.response = None
        # callback function will use this value to catch the appropriate response
        self.corr_id = str(uuid.uuid4())

        # Message properties
        # delivery_mode: Marks a message as persistent (with a value of 2) or transient (any other value).
        # content_type: Used to describe the mime-type of the encoding. For example for the often used JSON encoding
        #     it is a good practice to set this property to: application/json.
        # reply_to: Commonly used to name a callback queue.
        # correlation_id: Useful to correlate RPC responses with requests.
        self.channel.basic_publish(exchange='',
                                   routing_key='rpc_queue',
                                   properties=pika.BasicProperties(
                                       reply_to=self.callback_queue,
                                       correlation_id=self.corr_id,
                                   ),
                                   body=str(n))
        while self.response is None:
            # At this point we can sit back and wait until the proper response arrives.
            self.connection.process_data_events()
        # And finally we return the response back to the user
        return int(self.response or 0)


fibonacci_rpc = FibonacciRpcClient()

print(" [x] Requesting fib(30)")
response = fibonacci_rpc.call(30)
print(" [.] Got %r" % response)
