from pydantic import BaseModel

class Token(BaseModel):
    """ Represents the authentication token returned to the client """
    access_token: str
    token_type: str = "bearer"

class TokenPayload(BaseModel):
    """ Represents the payload data contained inside the token (e.g., decoded JWT) """
    sub: str | None = None