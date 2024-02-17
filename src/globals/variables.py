from models.partner import Partner
from models.message import Message
from typing import Optional
from helpers.client import get_local_ip
from helpers import file

MY_IP = get_local_ip()
FIRST_PARTNER: Optional[Partner] = Partner(MY_IP, file.env('DEFAULT_PARTNER_PORT'), None)
PARTNERS: dict[str, Partner] = {MY_IP: FIRST_PARTNER}
FIRST_PART_REFERENCE = [FIRST_PARTNER]
MESSAGES: list[Message] = []
INTERPROC_MESSAGES = None