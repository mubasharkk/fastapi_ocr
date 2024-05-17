import jwt
from decouple import config
import uuid
from fastapi import Request, Query, HTTPException, Depends, Header, Query
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional


class JWTBearer(HTTPBearer):
    secret = config('APP_SECRET')

    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request, api_key: str = Query()) -> Optional:
        bearer: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
        if bearer and bearer.scheme == "Bearer" and self.verify_jwt(
                request.query_params['api_key'], bearer.credentials
        ):
            return HTTPAuthorizationCredentials(scheme=bearer.scheme, credentials=bearer.credentials)
        else:
            raise HTTPException(status_code=403, detail="Could not validate credentials")

    def verify_jwt(self, api_key: str, api_token: str) -> bool:
        try:
            data = jwt.decode(api_token, self.secret, algorithms=["HS256"])
            return data['api_key'] == api_key
        except:
            return False


def generate_token():
    api_key = uuid.uuid4().hex
    api_token = jwt.encode({"api_key": api_key}, config('APP_SECRET'), algorithm="HS256")
    return {'api_key': api_key, 'api_token': api_token}


# Dependency function to check for the api_key
def check_api_key(api_key: str = Query(...)) -> uuid:
    try:
        return uuid.UUID(str(api_key))
    except ValueError:
        raise HTTPException(
            status_code=403,
            detail="Could not validate credentials",
        )
