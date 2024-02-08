import json

class Message:
    def __init__(self, host: str, id: str, content: str) -> None:
        self.host = host
        self.id = str(id)
        self.content = content

    def to_json(self):
        return json.dumps(self, default=serialize, indent=2)
    
    def to_dict(self):
        return serialize(self)

    def __str__(self):
        return self.host + " diz: " + self.content
    
    def get_real_id(self):
        return self.host + self.id
    
def serialize(obj):
    if isinstance(obj, Message):
        return {"host": obj.host, "id": obj.id, "content": obj.content}
    raise TypeError("Object not serializable")