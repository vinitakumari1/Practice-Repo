from pydantic import BaseModel, EmailStr, field_validator
from typing import Annotated


# Shared password validator
def validate_password_rules(value: str) -> str:
    import re
    if len(value) < 8 or len(value) > 20:
        raise ValueError("Password must be between 8 and 20 characters.")
    if not re.search(r"[a-z]", value):
        raise ValueError("Password must contain at least one lowercase letter.")
    if not re.search(r"[A-Z]", value):
        raise ValueError("Password must contain at least one uppercase letter.")
    if not re.search(r"\d", value):
        raise ValueError("Password must contain at least one digit.")
    if not re.search(r"[@$!%*?&]", value):
        raise ValueError("Password must contain at least one special character (@$!%*?&).")
    return value


class UserRegister(BaseModel):
    email: EmailStr
    full_name: str
    password: Annotated[str, str]

    @field_validator("password")
    def validate_password(cls, value):
        return validate_password_rules(value)


class UserLogin(BaseModel):
    email: EmailStr
    password: str  # No custom rules for login (just match)


