from pydantic import (
    BaseModel,
    Field,
)


class UserBaseSchema(BaseModel):
    username: str
    password: str


class UserCreateSchema(UserBaseSchema):
    pass


class UserUpdateSchema(UserBaseSchema):
    pass


class UserRegisterRequestSchema(UserBaseSchema):
    username: str = Field(..., min_length=4, max_length=50)
    password: str = Field(..., min_length=8, max_length=50)


class UserRegisterResponseSchema(UserBaseSchema):
    pass


class AccessTokenResponse(BaseModel):
    access_token: str


class UserTokenData(BaseModel):
    username: str | None = None


class CurrentUserSchema(BaseModel):
    id: int
    username: str
