from doctest import Example
from pydantic import BaseModel
from pydantic import Field
from pydantic import EmailStr

# User BaseModel
class UserBase(BaseModel):
    email: EmailStr = Field(
        ...,
        example = "mail@bussines.com",
    )
    username: str = Field(
        ...,
        min_length=5,
        max_length=50,
        example = "John Doe",
    )
# User Id
class User(UserBase):
    id: int = Field(
        ...,
        example = 1
    )
# User Create password
class UserRegister(UserBase):
    password: str = Field(
        ...,
        min_length=8,
        max_length=50,
        example='my_password'
    )
