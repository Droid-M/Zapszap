from DAOs import messageDAO, partnerDAO
from globals.variables import MY_IP, PRIVATE_KEY
from services import partner_service, data_service
from helpers import file, key
import json

def intercept_messages(data: dict):
    # Rgistra as mensagens recebidas
    file.log("message.log", "intercept_messages")
    file.log("message.log", "Merge msgs" if data.get("merge_messages") else "New msg")
    me = partnerDAO.get_me()
    if data.get("merge_messages"):
        messages = json.loads(key.decrypt_message(data.get("messages_list"), PRIVATE_KEY, me.public_key))
        messages = messageDAO.from_list_of_dicts(messages)
        file.log("message.log", "current messages:")
        file.log("message.log", messageDAO.to_json())
        messageDAO.merge_messages(messages)
        file.log("message.log", "merge messages:")
        file.log("message.log", messageDAO.to_json())
    else:
        new_msg = data.get("new_message")
        new_msg = key.decrypt_message(new_msg, PRIVATE_KEY, me.public_key)
        messageDAO.register(data.get("from"), new_msg, data.get("sender"))

    # Registra que o usuário recebeu e tratou a mensagem:
    receivers_list: list = data.get("receivers_list", [])    

    if MY_IP not in receivers_list:
        receivers_list.append(MY_IP)
    data["receivers_list"] = receivers_list

    data_service.backup_data()

    # Envia a mensagem para o próximo colega na lista:
    next = partnerDAO.get_me().next_partner
    if next is None:
        next = partnerDAO.get_first()
    messages = key.encrypt_message(json.dumps(messageDAO.to_list_of_dicts()), next.public_key)
    data["messages_list"] = messages
    partner_service.forward_message_to_active_member(next, data)
