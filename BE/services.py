import time
from datetime import datetime, timedelta
from fastapi import FastAPI, Body, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Dict, Any
from pydantic import BaseModel
from sqlalchemy.orm import Session

from crew.chatbot import process_user_query
from models import ChatSession, User, ChatHistory, UserCreate, UserResponse, Token, SessionLocal
from auth import get_password_hash, authenticate_user, create_access_token, get_current_active_user, ACCESS_TOKEN_EXPIRE_MINUTES

# Import admin routes after all dependencies are defined
from admin import router

app = FastAPI(title="Locations API", description="API providing locations coordinates data")

# Include admin routes
app.include_router(router)

# Get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Add CORS middleware to allow cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for development
    allow_credentials=False,  # Must be False when allow_origins=["*"]
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"]
)

class CityRequest(BaseModel):
    input_string: str

    
@app.post("/locations")
async def get_cities(request: CityRequest = Body(...)):
    """
    Returns cities data or a string based on the processed query.
    
    Takes a long string as input. The response type can be either:
    - A list of dictionaries with city information
    - A string response
    """
    try:
        # Log or process the input_string if needed
        print(f"Received input string: {request.input_string[:100]}...")  # Print first 100 chars
        
        # Get the response
        result = process_user_query(request.input_string)
        print(f"Processed result: {result[:100]}...")  # Print first 100 chars of result
        
        # Check the type of result and return appropriate response
        if isinstance(result, str):
            return {"type": "text", "content": result}
        elif isinstance(result, (list, dict)):
            return {"type": "json", "content": result}
        else:
            return {"type": "error", "content": "Unexpected response type"}
        # return [{'rank': 1, 'score': 1.221296787261963, 'index': 11, 'title': 'Aditya Shagun Mall', 'place_id': 'ChIJL9wRPVm-wjsRcD1BYTfcW_E'}, {'rank': 2, 'score': 1.247261881828308, 'index': 6, 'title': 'Royale Heritage Mall', 'place_id': 'ChIJndd_RLvrwjsRx5LWxbkYYH8'}, {'rank': 3, 'score': 1.3079421520233154, 'index': 21, 'title': 'ISKCON NVCC Pune', 'place_id': 'ChIJSdctqfvqwjsR7tcJvlsbul4'}, {'rank': 4, 'score': 1.314194917678833, 'index': 15, 'title': 'Piazza Pizza By Little Italy SGS Mall', 'place_id': 'ChIJ0wMQ-U_AwjsRsuEOeqz4KPc'}, {'rank': 5, 'score': 1.3251968622207642, 'index': 2, 'title': 'Seasons Mall', 'place_id': 'ChIJ41PwQ_LBwjsRypeqtFw7peY'}]
            
    except Exception as e:
        return {"type": "error", "content": str(e)}


@app.get("/")
async def root():
    """
    Root endpoint that provides information about the API.
    """
    return {
        "message": "Welcome to the locations API. Use POST /locations with a JSON body containing 'input_string' to get the list of locations."
    }


@app.post("/signup")
async def signup(user: UserCreate, db: Session = Depends(get_db)):
    try:
        # Check if username exists
        db_user = db.query(User).filter(User.email == user.email).first()
        if db_user:
            return {"success": True, "message": "Username already registered"}
        
        # Check if email exists
        db_user = db.query(User).filter(User.email == user.email).first()
        if db_user:
            return {"success": True, "message": "Email already registered"}
        
        # Create new user
        hashed_password = get_password_hash(user.password)
        db_user = User(
            username=user.email,
            email=user.email,
            hashed_password=hashed_password
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return {"success": True, "message": "Registration successful"}
    except Exception as e:
        return {"success": False, "message": str(e)}

class SignInRequest(BaseModel):
    email: str
    password: str

@app.post("/signin")
async def login_for_access_token(
    credentials: SignInRequest,
    db: Session = Depends(get_db)
):
    try:
        print(f"Attempting to authenticate user: {credentials.password}")
        user = authenticate_user(db, credentials.email, credentials.password)
        if not user:
            return {
                "success": False,
                "message": "Incorrect username or password"
            }
        
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user.email}, expires_delta=access_token_expires
        )
        return {
            "success": True,
            "message": "Login successful",
            "data": {
                "access_token": access_token,
                "token_type": "bearer"
            }
        }
    except Exception as e:
        return {"success": False, "message": str(e)}

@app.get("/users/me", response_model=UserResponse)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user

# Chat session endpoints
class ChatSessionCreate(BaseModel):
    topic: str = None

@app.post("/chat/sessions")
async def create_chat_session(
    session_data: ChatSessionCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    chat_session = ChatSession(
        user_id=current_user.id,
        topic=session_data.topic
    )
    db.add(chat_session)
    db.commit()
    db.refresh(chat_session)
    return chat_session

@app.get("/chat/sessions")
async def get_chat_sessions(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    sessions = db.query(ChatSession)\
        .filter(ChatSession.user_id == current_user.id)\
        .order_by(ChatSession.last_updated.desc())\
        .all()
    return sessions

@app.get("/chat/sessions/{session_id}")
async def get_chat_session(
    session_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    session = db.query(ChatSession)\
        .filter(ChatSession.id == session_id, ChatSession.user_id == current_user.id)\
        .first()
    if not session:
        raise HTTPException(status_code=404, detail="Chat session not found")
    return session

# Chat history endpoints
class ChatMessageCreate(BaseModel):
    session_id: int
    message: str
    response: str
    response_type: str = "text"  # 'text' or 'json'

@app.post("/chat/history")
async def save_chat_history(
    chat_data: ChatMessageCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    # Verify session exists and belongs to user
    session = db.query(ChatSession)\
        .filter(ChatSession.id == chat_data.session_id, ChatSession.user_id == current_user.id)\
        .first()
    if not session:
        raise HTTPException(status_code=404, detail="Chat session not found")
    
    chat_history = ChatHistory(
        session_id=chat_data.session_id,
        user_id=current_user.id,
        message=chat_data.message,
        response=chat_data.response,
        response_type=chat_data.response_type
    )
    db.add(chat_history)
    # Update session last_updated time
    session.last_updated = datetime.utcnow()
    db.commit()
    db.refresh(chat_history)
    return {"status": "success", "message": "Chat history saved"}

@app.get("/chat/history/{session_id}")
async def get_chat_history(
    session_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    # Verify session exists and belongs to user
    session = db.query(ChatSession)\
        .filter(ChatSession.id == session_id, ChatSession.user_id == current_user.id)\
        .first()
    if not session:
        raise HTTPException(status_code=404, detail="Chat session not found")
    
    chat_history = db.query(ChatHistory)\
        .filter(
            ChatHistory.session_id == session_id,
            ChatHistory.user_id == current_user.id
        )\
        .order_by(ChatHistory.timestamp.asc())\
        .all()
    return chat_history

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)