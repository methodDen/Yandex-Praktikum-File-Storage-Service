from pydantic import BaseModel, Field


class UserBaseSchema(BaseModel):
    username: str
    password: str


class UserCreateSchema(UserBaseSchema):
    username: str = Field(..., min_length=4, max_length=50)
    password: str = Field(..., min_length=8, max_length=50)


class UserUpdateSchema(UserBaseSchema):
    pass


class UserRegisterRequestSchema(UserBaseSchema):
    pass


class UserRegisterResponseSchema(UserBaseSchema):
    pass