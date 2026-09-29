import base64,json,hmac,hashlib,time
from sqlalchemy.orm import Session
import os
from app.config import settings
from app.models.db import User
def _b64(x): return base64.urlsafe_b64encode(x).rstrip(b"=").decode()
def _unb64(x): return base64.urlsafe_b64decode(x+"="*((4-len(x)%4)%4))
def generate_password_hash(password):
    salt=os.urandom(16)
    digest=hashlib.scrypt(password.encode(),salt=salt,n=2**14,r=8,p=1)
    return f"scrypt${_b64(salt)}${_b64(digest)}"
def check_password_hash(stored,password):
    _,salt,digest=stored.split("$")
    actual=hashlib.scrypt(password.encode(),salt=_unb64(salt),n=2**14,r=8,p=1)
    return hmac.compare_digest(actual,_unb64(digest))
def create_user(db,email,password):
    email=email.strip().lower()
    if db.query(User).filter(User.email==email).first(): raise ValueError("Email is already registered.")
    user=User(email=email,password_hash=generate_password_hash(password));db.add(user);db.commit();db.refresh(user);return user
def authenticate(db,email,password):
    u=db.query(User).filter(User.email==email.strip().lower()).first()
    return u if u and check_password_hash(u.password_hash,password) else None
def create_access_token(user_id):
    header=_b64(b'{"alg":"HS256","typ":"JWT"}')
    payload=_b64(json.dumps({"sub":str(user_id),"exp":int(time.time())+settings.access_token_expire_minutes*60},separators=(",",":")).encode())
    sig=_b64(hmac.new(settings.secret_key.encode(),f"{header}.{payload}".encode(),hashlib.sha256).digest())
    return f"{header}.{payload}.{sig}"
def get_user_from_token(db,token):
    try:
        header,payload,sig=token.split(".")
        expected=_b64(hmac.new(settings.secret_key.encode(),f"{header}.{payload}".encode(),hashlib.sha256).digest())
        if not hmac.compare_digest(sig,expected): return None
        data=json.loads(_unb64(payload))
        if int(data["exp"])<int(time.time()): return None
        return db.get(User,int(data["sub"]))
    except Exception:return None
