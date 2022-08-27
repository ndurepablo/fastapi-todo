from fastapi import HTTPException, status


from app.v1.model.user_model import User as UserModel
from app.v1.schema import user_schema
from app.v1.service.auth_service import get_password_hash

# create user
def create_user(user: user_schema.UserRegister):
    # search the user in the database
    get_user = UserModel.filter((UserModel.email == user.email) | (UserModel.username == user.username)).first()
    if get_user:
        msg = 'Email already exists'
        if get_user.username == user.username:
            msg = 'Username already exists'
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=msg
            )
    # if not exists, create user
    else:
        db_user = UserModel(
            username = user.username,
            email = user.email,
            password = get_password_hash(user.password)
        )
        db_user.save()
    # return user
    return user_schema.User(
        id = db_user.id,
        username = db_user.username,
        email = db_user.email
    )