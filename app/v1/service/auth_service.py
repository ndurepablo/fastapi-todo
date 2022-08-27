from datetime import datetime, timedelta
from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from jose import JWTError, jwt
from passlib.context import CryptContext

from app.v1.model.user_model import User as UserModel
from app.v1.schema.token_schema import TokenData
from app.v1.utils.settings import Settings

settings = Settings()

# declare token settings
SECRET_KEY = settings.secret_key
ALGORITHM = 'HS256'
ACCESS_TOKEN_TIME_EXPIRE_MINUTES = settings.token_expire

# init hash password generator
pwd_context = CryptContext(schemes=["bcrypt"], deprecated='auto')
# setting up url for token validation
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/login")

# verify from hash password
def verify_password(plain_password, password):
    return pwd_context.verify(plain_password, password)

# encrypting password
def get_password_hash(password):
    return pwd_context.hash(password)

# filter user by email or usrname
def get_user(username: str):
    return UserModel.filter(
        (UserModel.email == username) | 
        # Necesitabamos el FIRST para que no tire ATTRIBUTERRROR
        (UserModel.username == username)).first()

# auth user
def authenticate_user(username: str, password: str):
    user = get_user(username)
    if not user:
        return False
    # ACA
    if not verify_password(password, user.password):
        return False
    return user

    
# token creator  
def create_access_token(data: dict, expire_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expire_delta:
        expire = datetime.utcnow() + expire_delta
    else:
        expire = datetime.utcnow + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encode_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encode_jwt

# user token generator
def generate_token(username, password):
    user = authenticate_user(username, password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="incorrect username/email or password",
            headers={"WWW-Authenticate': 'Bearer"}
        )
    else:
        acess_token_expires = timedelta(minutes=ACCESS_TOKEN_TIME_EXPIRE_MINUTES)
        return create_access_token(
            data={'sub': user.username},
            expire_delta=acess_token_expires
        )
    
# After user authentication, get, decode and return current user
async def get_current_user(token: str = Depends(oauth2_scheme)):
    credential_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate': 'Bearer"}
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get('sub')
        if username is None:
            raise credential_exception
        else:
            token_data = TokenData(username=username)
    except JWTError:
        raise credential_exception
    
    user = get_user(username=token_data.username)
    if user is None:
        raise credential_exception
    else:
        return user
        