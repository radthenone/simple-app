from datetime import datetime
from typing import Optional

import pydantic
from pydantic import EmailStr


class User(pydantic.BaseModel):
    username: str
    password: str
    email: EmailStr
    is_active: bool = False
    is_admin: bool = False
    created_at: str = datetime.now().isoformat()
    updated_at: Optional[str] = None
