import os
os.environ["DATABASE_URL"]="sqlite:///./data/test_pocketsmart.db"
os.environ["SECRET_KEY"]="test-secret"
from fastapi.testclient import TestClient
from app.main import app
def test_health():
    with TestClient(app) as client:
        r=client.get("/health"); assert r.status_code==200 and r.json()["status"]=="ok"
def test_register_login_logout():
    with TestClient(app) as client:
        client.post("/api/register",json={"email":"test@example.com","password":"secret123"})
        r=client.post("/api/login",json={"email":"test@example.com","password":"secret123"})
        assert r.status_code==200
        assert client.get("/api/session-info").status_code==200
        assert client.post("/api/logout").status_code==200
def test_home_requires_login():
    with TestClient(app) as client:
        r=client.post("/api/generate-home",json={"budget":20000,"rooms":["Bedroom"],"style":"modern","notes":""})
        assert r.status_code==401
