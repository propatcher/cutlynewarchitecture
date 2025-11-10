from dataclasses import dataclass
from datetime import datetime
from uuid import UUID, uuid4

@dataclass
class Link:
    id : UUID
    original_url : str
    short_code : str
    user_id : UUID
    created_at : datetime
    click_count : int = 0
    
    @classmethod
    def create(cls, original_url: str, short_code: str, user_id: UUID) -> "Link":
        return cls(
            id = uuid4(),
            original_url = original_url,
            short_code = short_code,
            user_id = user_id,
            created_at = datetime.now()
        )
    
    def increment_click_count(self):
        self.click_count += 1