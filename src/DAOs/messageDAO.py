from globals import variables
from globals.variables import Message, MY_IP
import json
from helpers import file

MESSAGES_COUNTER = 0

def register(host, content, sender_name = "", id = None):
    global MESSAGES_COUNTER
    for msg in variables.MESSAGES:
        if int(msg.id) >= MESSAGES_COUNTER:
            if (id is not None) and id <= msg.id:
                if host > msg.host:
                    id = msg.id + 1
                else:
                    msg.id += 1
            MESSAGES_COUNTER = int(msg.id)
    if id is None:
        id = 0
    MESSAGES_COUNTER = max(MESSAGES_COUNTER + 1, id)
    old_messages = variables.MESSAGES.copy()
    new_message = Message(host, MESSAGES_COUNTER, content, sender_name)
    
    old_messages.append(new_message)
    variables.MESSAGES = sorted(old_messages, key=lambda msg: (msg.get_hash()))
    return new_message

def empty():
    return len(variables.MESSAGES) == 0

def messages_groups_are_equals(messagesGp1, messagesGp2):
    msgQty = len(messagesGp1)
    if msgQty != len(messagesGp2):
        return False
    count = 0
    while count < msgQty:
        if messagesGp1[count] != messagesGp2[count]:
            return False
        count += 1
    return True

def get_last_message():
    msgQty = len(variables.MESSAGES)
    if not msgQty:
        return None
    return variables.MESSAGES[msgQty - 1]

def to_json():
    return json.dumps(to_list_of_dicts(), indent=2)

def to_list_of_dicts():
    messages = []
    for message in variables.MESSAGES:
        messages.append(message.to_dict())
    return messages

def from_list_of_dicts(json_data) -> list[Message]:
    messages = []
    for message_data in json_data:
        host = message_data.get("host", "")
        msg_id = message_data.get("id", "")
        content = message_data.get("content", "")
        sender_name = message_data.get("sender_name", "")
        new_message = Message(host, msg_id, content, sender_name)
        messages.append(new_message)
    return messages

def merge_messages(new_messages):
    old_messages = variables.MESSAGES.copy()
    msgs_dict = {}
    for message in old_messages:
        msgs_dict[message.get_real_id()] = message
    for message in new_messages:
        if msgs_dict.get(message.get_real_id()) is None:
            old_messages.append(message)
    variables.MESSAGES = sorted(old_messages, key=lambda msg: (msg.get_hash()))