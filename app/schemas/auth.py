from pydantic import BaseModel, EmailStr, Field


class RegisterRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)
    handle: str = Field(min_length=2, max_length=30)


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"