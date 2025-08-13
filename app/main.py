import io, os
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import StreamingResponse
from PIL import Image, UnidentifiedImageError
app = FastAPI(title="Privacy Guard")
ALLOWED = {"image/jpeg","image/png"}
MAX_BYTES = 5*1024*1024
APP_VERSION = os.getenv("APP_VERSION", "dev")
@app.get("/health")
def health(): return {"status":"ok","version":APP_VERSION}
@app.post("/sanitize")
async def sanitize(file: UploadFile = File(...)):
    if file.content_type not in ALLOWED: raise HTTPException(415,"Only JPEG/PNG allowed")
    data = await file.read()
    if len(data) > MAX_BYTES: raise HTTPException(413,"File too large")
    try: img = Image.open(io.BytesIO(data))
    except UnidentifiedImageError: raise HTTPException(400,"Invalid image")
    had_exif = bool(getattr(img, "getexif", lambda: {})())
    buf = io.BytesIO()
    if file.content_type=="image/jpeg":
        img.convert("RGB").save(buf, format="JPEG", quality=90); mime="image/jpeg"
    else:
        img.save(buf, format="PNG", optimize=True); mime="image/png"
    return StreamingResponse(io.BytesIO(buf.getvalue()), media_type=mime,
        headers={"X-Exif-Removed": "true" if had_exif else "false", "X-App-Version": APP_VERSION})
