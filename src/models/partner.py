from typing import Optional
import json
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend

class Partner:
    def __init__(self, host: str, port: int, socket = None, public_key: str = None):
        self.host = host
        self.port = port
        self.socket = socket
        self.has_disconnected = False
        self.next_partner: Optional[Partner] = None
        self.is_offline = False
        self.public_key = public_key

    def to_json(self):
        return json.dumps(self, default=serialize, indent=2)
    
    def to_dict(self):
        return serialize(self)
    
def serialize(obj: Partner):
    if isinstance(obj, Partner):
        return {'host': obj.host, 'port': obj.port, 
                'socket': None,
                # 'socket': obj.socket,
                'has_disconnected': obj.has_disconnected, 'next_partner': obj.next_partner.to_dict() if obj.next_partner is not None else None,
                'is_offline': obj.is_offline, 'public_key': obj.public_key}
    raise TypeError("Object not serializable")