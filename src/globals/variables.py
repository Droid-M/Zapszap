from models.partner import Partner
from models.message import Message
from typing import Optional
from helpers import client
from helpers import file

MY_IP = client.get_local_ip()
FIRST_PARTNER: Optional[Partner] = Partner(MY_IP, file.env('DEFAULT_PARTNER_PORT'), None)
PARTNERS = {MY_IP: FIRST_PARTNER}
FIRST_PART_REFERENCE = [FIRST_PARTNER]
MESSAGES = []
INTERPROC_MESSAGES = None