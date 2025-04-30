from fastapi import FastAPI, Request, UploadFile, File, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import httpx
from jwt_utils import verify_jwt_token
import logging
from typing import Dict, Any

# Configuration du système de journalisation (Logging)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# Configuration CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Définition des adresses des services
AUTH_URL = "http://auth_service:8001"
PREDICT_URL = "http://prediction_service:8002"
CHATBOT_URL = "http://chatbot_service:8003"

# Temps d'attente pour les requêtes (en secondes)
REQUEST_TIMEOUT = 30.0

async def make_service_request(
    url: str,
    method: str = "post",
    json_data: Dict[str, Any] = None,
    files: Dict[str, Any] = None
) -> Dict[str, Any]:
    """Fonction utilitaire pour effectuer des requêtes aux services internes"""
    try:
        async with httpx.AsyncClient(timeout=REQUEST_TIMEOUT) as client:
            if method.lower() == "post":
                if files:
                    response = await client.post(url, files=files)
                else:
                    response = await client.post(url, json=json_data)
            else:
                response = await client.get(url)
            
            response.raise_for_status()
            return response.json()
            
    except httpx.HTTPStatusError as e:
        logger.error(f"Service returned error: {str(e)}")
        raise HTTPException(
            status_code=e.response.status_code,
            detail=f"Service error: {e.response.text}"
        )
    except httpx.RequestError as e:
        logger.error(f"Service connection error: {str(e)}")
        raise HTTPException(
            status_code=503,
            detail="Service unavailable, please try again later"
        )
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Internal server error"
        )

@app.post("/auth/register")
async def register(request: Request):
    """Enregistrement d'un nouvel utilisateur"""
    body = await request.json()
    logger.info(f"Register request for {body.get('email')}")
    return await make_service_request(f"{AUTH_URL}/auth/register", json_data=body)

@app.post("/auth/login")
async def login(request: Request):
    """Connexion"""
    body = await request.json()
    logger.info(f"Login attempt for {body.get('email')}")
    return await make_service_request(f"{AUTH_URL}/auth/login", json_data=body)

@app.post("/auth/verify-otp")
async def verify_otp(request: Request):
    """Vérification du code OTP"""
    body = await request.json()
    logger.info(f"OTP verification attempt for {body.get('email')}")
    return await make_service_request(f"{AUTH_URL}/auth/verify-otp", json_data=body)

@app.post("/chatbot")
async def chatbot_proxy(request: Request):
    """Redirection vers le service de chat"""
    data = await request.json()
    logger.info(f"Chatbot request with message: {data.get('message', '')[:50]}...")
    return await make_service_request(f"{CHATBOT_URL}/chat", json_data=data)

@app.post("/predict")
async def predict(
    file: UploadFile = File(...),
    token_data: dict = Depends(verify_jwt_token)
):
    """Prédiction d'image"""
    logger.info(f"Prediction request from user: {token_data.get('email')}")
    try:
        files = {"file": (file.filename, await file.read(), file.content_type)}
        return await make_service_request(f"{PREDICT_URL}/predict", files=files)
    except Exception as e:
        logger.error(f"File handling error: {str(e)}")
        raise HTTPException(
            status_code=400,
            detail="Error processing uploaded file"
        )