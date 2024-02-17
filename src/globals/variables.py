from models.partner import Partner
from models.ordered_host import OrderedHost
from models.group import Group
from models.message import Message
from typing import Optional
from helpers.client import get_local_ip
from helpers import file, client

GROUPS: dict[str, Group] = {}
MY_IP = get_local_ip()
FIRST_PARTNER: Optional[Partner] = Partner(MY_IP, file.env('DEFAULT_PARTNER_PORT'), None)
PARTNERS: dict[str, Partner] = {MY_IP: FIRST_PARTNER}
FIRST_PART_REFERENCE = [FIRST_PARTNER]
MESSAGES: list[Message] = []
INTERPROC_MESSAGES = None

__private_key = None

def get_private_key():
    global __private_key
    if __private_key is None:
        __private_key = client.serialize_key(file.read_backup_file("private_key.zap"), True)
    return __private_key