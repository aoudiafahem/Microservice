from fastapi import FastAPI, Request, UploadFile, File, Depends
from fastapi.middleware.cors import CORSMiddleware
import httpx
from jwt_utils import verify_jwt_token

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

AUTH_URL = "http://auth_service:8001"
PREDICT_URL = "http://prediction_service:8002"

@app.post("/auth/register")
async def register(request: Request):
    body = await request.json()
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{AUTH_URL}/auth/register", json=body)
    return response.json()

@app.post("/auth/login")
async def login(request: Request):
    body = await request.json()
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{AUTH_URL}/auth/login", json=body)
    return response.json()

# ✅ تحقق من OTP
@app.post("/auth/verify-otp")
async def verify_otp(request: Request):
    body = await request.json()
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{AUTH_URL}/auth/verify-otp", json=body)
    return response.json()

# ✅ توقع الصورة
@app.post("/predict")
async def predict(file: UploadFile = File(...), token_data: dict = Depends(verify_jwt_token)):
    async with httpx.AsyncClient() as client:
        files = {"file": (file.filename, await file.read(), file.content_type)}
        response = await client.post(f"{PREDICT_URL}/predict", files=files)
        print("🟢 RESPONSE FROM prediction_service:", response.text)
    return response.json()
