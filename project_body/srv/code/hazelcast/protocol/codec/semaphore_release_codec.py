from hazelcast.serialization.bits import *
from hazelcast.protocol.client_message import ClientMessage
from hazelcast.protocol.custom_codec import *
from hazelcast.util import ImmutableLazyDataList
from hazelcast.protocol.codec.semaphore_message_type import *

REQUEST_TYPE = SEMAPHORE_RELEASE
RESPONSE_TYPE = 100
RETRYABLE = False


def calculate_size(name, permits):
    """ Calculates the request payload size"""
    data_size = 0
    data_size += calculate_size_str(name)
    data_size += INT_SIZE_IN_BYTES
    return data_size


def encode_request(name, permits):
    """ Encode request into client_message"""
    client_message = ClientMessage(payload_size=calculate_size(name, permits))
    client_message.set_message_type(REQUEST_TYPE)
    client_message.set_retryable(RETRYABLE)
    client_message.append_str(name)
    client_message.append_int(permits)
    client_message.update_frame_length()
    return client_message


# Empty decode_response(client_message), this message has no parameters to decode



