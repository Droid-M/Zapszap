import json

class Message:
    def __init__(self, host: str, id: str, content: str, sender_name: str) -> None:
        self.host = host
        self.id = str(id)
        self.content = content
        self.sender_name = sender_name

    def to_json(self):
        return json.dumps(self, default=serialize, indent=2)
    
    def to_dict(self):
        return serialize(self)

    def __str__(self):
        return self.sender_name + " (" + self.host + ") diz: " + self.content
    
    def get_real_id(self):
        return self.id + self.sender_name + self.host
    
    def get_hash(self):
        return str(self.id).rjust(8, '0') + self.sender_name + self.host
    
def serialize(obj):
    if isinstance(obj, Message):
        return {"host": obj.host, "id": obj.id, "content": obj.content, "name": obj.sender_name}
    raise TypeError("Object not serializable")