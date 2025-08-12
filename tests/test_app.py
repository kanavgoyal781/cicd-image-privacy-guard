import io
from fastapi.testclient import TestClient
from PIL import Image
from app.main import app
c = TestClient(app)
def test_health(): assert c.get("/health").json()["status"]=="ok"
def test_sanitize():
    b=io.BytesIO(); Image.new("RGB",(16,16),(1,2,3)).save(b,format="PNG")
    r=c.post("/sanitize",files={"file":("x.png",b.getvalue(),"image/png")})
    assert r.status_code==200
