from globals.variables import Partner, OrderedHost
from typing import Optional
import json

class Group:
    def __init__(self, name: str, id: str, joined = False) -> None:
        """
        parameters:
            - id (str): group identifier (must be generated via timestamp with milliseconds)
            - name (str): group name
            - members (dict): partners/members list
            - members_order (list): indicates the order in which members should receive messages
        """
        self.name = name
        self.id = id
        self.members: dict[str, Partner] = {}
        self.joined = joined
        # self.members_order: list[OrderedHost] = []

    def insert_member(self, new_member: Partner, secure_insertion = True):
        if not secure_insertion:
            self.members[new_member.host] = new_member
        else:
            member = self.members.get(new_member.host)
            if member is None:
                member = new_member
                member.socket = None
                member.has_disconnected = False
            self.members[member.host] = member

    def remove_member(self, member_host) -> Optional[Partner]:
        return self.members.pop(member_host)

    def to_json(self):
        return json.dumps(self, default=serialize, indent=2)
    
    def to_dict(self):
        return serialize(self)
    
def serialize(obj):
    if isinstance(obj, Group):
        members = {}
        for i in obj.members:
            members[i] = obj.members[i].to_dict()
        return {'name': obj.name, 'id': obj.id, 'joined': obj.joined, 'members': members}
    raise TypeError("Object not serializable")