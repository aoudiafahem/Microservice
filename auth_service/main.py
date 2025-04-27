from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
from database import SessionLocal, engine
import models, schemas, utils
import bcrypt
from jwt_utils import create_access_token  # ✅ استيراد لإنشاء JWT

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # أصل الواجهة
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ✅ تسجيل مستخدم جديد
@app.post("/auth/register")
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt())
    new_user = models.User(
        name=user.name,
        email=user.email,
        password=hashed_password.decode('utf-8')
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "User registered successfully"}

# ✅ تسجيل دخول وإرسال OTP
@app.post("/auth/login")
def login(user: schemas.UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    if not bcrypt.checkpw(user.password.encode('utf-8'), db_user.password.encode('utf-8')):
        raise HTTPException(status_code=400, detail="Incorrect password")

    otp = utils.generate_otp()
    utils.store_otp(db, db_user.id, otp)
    utils.send_otp_email(db_user.email, otp, db_user.name)

    return {"message": "OTP sent to your email"}

# ✅ التحقق من OTP وإرجاع التوكن
@app.post("/auth/verify-otp")
def verify_otp(data: schemas.OTPVerify, db: Session = Depends(get_db)):
    is_valid, result = utils.verify_otp(db, data.email, data.otp)
    if not is_valid:
        raise HTTPException(status_code=400, detail=result)

    # إنشاء توكن JWT بعد نجاح التحقق
    token = create_access_token({"sub": result.email})

    return {
        "message": "OTP verified successfully",
        "user": {
            "name": result.name,
            "email": result.email
        },
        "token": token  # ✅ نرجع التوكن مع الرد
    }
