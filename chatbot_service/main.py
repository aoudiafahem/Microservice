from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
from openai import OpenAI, OpenAIError  # تغيير الاستيراد
import os
import logging
from fastapi.middleware.cors import CORSMiddleware

# إعداد نظام التسجيل (Logging)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# تحميل المتغيرات من .env
load_dotenv()

app = FastAPI()

# إعداد CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# التحقق من وجود مفتاح OpenAI
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

if not OPENAI_API_KEY:
    logger.error("OPENAI_API_KEY not found in environment variables")
    raise RuntimeError("OpenAI API key is missing in environment variables")

# تهيئة عميل OpenAI (الجديد)
client = OpenAI(api_key=OPENAI_API_KEY)

class ChatRequest(BaseModel):
    message: str

@app.post("/chat")
async def chat_with_bot(request: ChatRequest):
    try:
        logger.info(f"Received chat request with message: {request.message[:50]}...")
        
        if not request.message.strip():
            logger.warning("Received empty message")
            raise HTTPException(status_code=400, detail="Message cannot be empty")
        
        model_params = {
            "model": "gpt-3.5-turbo",
            "messages": [{"role": "user", "content": request.message}],
            "temperature": 0.7,
            "max_tokens": 1000,
        }
        
        logger.debug(f"Sending request to OpenAI with params: {model_params}")
        
        # التغيير الرئيسي هنا (استخدام client بدلاً من openai مباشرة)
        response = client.chat.completions.create(**model_params)
        
        if not response.choices:
            logger.error("No choices returned from OpenAI API")
            raise HTTPException(status_code=500, detail="No response from AI model")
        
        reply = response.choices[0].message.content
        logger.info(f"Successfully generated response: {reply[:50]}...")
        
        return {"response": reply}
        
    except OpenAIError as e:  # التغيير هنا لاستخدام OpenAIError
        logger.error("OpenAI API error: %s", str(e))
        error_detail = str(e)
        status_code = 502  # Bad Gateway by default
        
        if "authentication" in error_detail.lower():
            status_code = 401
            error_detail = "Invalid OpenAI API key. Please check your configuration."
        elif "rate limit" in error_detail.lower():
            status_code = 429
            error_detail = "API rate limit exceeded. Please try again later."
            
        raise HTTPException(
            status_code=status_code,
            detail=error_detail
        )
    except Exception as e:
        logger.error("Unexpected error: %s", str(e), exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )

@app.get("/health")
async def health_check():
    """نقطة نهاية للتحقق من صحة الخدمة"""
    try:
        # تحقق بسيط من اتصال OpenAI (محدث للإصدار الجديد)
        client.models.list(limit=1)
        return {
            "status": "healthy",
            "openai_configured": bool(OPENAI_API_KEY),
            "details": "Service is running normally"
        }
    except Exception as e:
        logger.error("Health check failed: %s", str(e))
        raise HTTPException(
            status_code=503,
            detail=f"Service unavailable: {str(e)}"
        )