from typing import Annotated

import uvicorn
from fastapi import Depends, FastAPI
from fastapi.security import OAuth2PasswordBearer
import jwt


app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

data = {
    "password": "wdawd",
    "name": "name",
    "surname": "surname"
}

encoded_jwt = jwt.encode(data, "secret", algorithm="HS256")

print(encoded_jwt)

encoded_jwt = jwt.decode(encoded_jwt, "secret", algorithms=["HS256"])

print(encoded_jwt)

