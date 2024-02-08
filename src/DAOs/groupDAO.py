from globals.variables import Group, GROUPS, Partner
from typing import Optional

def register(name, id, members: Optional[dict[str, Partner]], joined = False):
    group = GROUPS.get(id, Group(name, id))
    group.joined = joined
    for i in members:
        group.insert_member(members[i])
    GROUPS[id] = group
    return group

def to_json():
    groups = {}
    for i in GROUPS:
        groups[i] = GROUPS[i].to_json()
    return groups

def from_dict(data: dict):
    group = Group(name=data['name'], id=data['id'], joined=data['joined'])
    
    # Adiciona membros ao grupo
    for member_host, member_data in data.get('members', {}).items():
        member = Partner(
            host=member_data['host'],
            port=member_data['port'],
            socket=member_data['socket']
        )
        member.has_disconnected = member_data['has_disconnected']
        member.is_offline = member_data['is_offline']
        group.insert_member(member)
    return group