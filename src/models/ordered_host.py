from typing import Optional

class OrderedHost:
    def __init__(self, current: str, next: Optional[str] = None):
        self.current = current
        self.next_is_offline = False
        self.next = next