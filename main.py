"""
Valentine's Day Invitation Creator - FastAPI Backend
"""
import os
import base64
import uuid
from io import BytesIO
from pathlib import Path

from fastapi import FastAPI, UploadFile, Form, HTTPException, File, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy import create_engine, Column, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from pydantic import BaseModel
from PIL import Image
import uvicorn

# ========== DATABASE SETUP ==========
DATABASE_URL = "sqlite:///./database.db"
engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


# ========== DATABASE MODEL ==========
class Invitation(Base):
    __tablename__ = "invitations"

    id = Column(String, primary_key=True, index=True)
    recipient_name = Column(String, index=True)
    sender_name = Column(String)
    message = Column(Text)
    theme = Column(String, default="romantic")
    photo_base64 = Column(Text, nullable=True)  # data:image/jpeg;base64,...


# Create tables
Base.metadata.create_all(bind=engine)

# ========== FASTAPI APP ==========
app = FastAPI(title="💝 Valentine's Invitation Creator")

# Templates
templates = Jinja2Templates(directory="templates")


# ========== UTILITY FUNCTIONS ==========
def generate_short_id() -> str:
    """Generate a short invitation ID (first 12 chars of UUID)"""
    return str(uuid.uuid4())[:12]


def compress_image(file: UploadFile, max_size_mb: int = 2) -> str:
    """
    Compress image to JPEG and convert to base64 data URL.
    
    Args:
        file: UploadFile from form
        max_size_mb: Maximum file size in MB
    
    Returns:
        Base64 data URL (data:image/jpeg;base64,...)
    """
    # Check original file size
    file_size_mb = len(file.file.read()) / (1024 * 1024)
    file.file.seek(0)  # Reset file pointer
    
    if file_size_mb > max_size_mb:
        raise ValueError(f"Photo too large ({file_size_mb:.1f}MB). Max {max_size_mb}MB.")
    
    # Open and resize image
    img = Image.open(file.file)
    
    # Resize to max 800px width, maintain aspect ratio
    MAX_WIDTH = 800
    if img.width > MAX_WIDTH:
        ratio = MAX_WIDTH / img.width
        new_height = int(img.height * ratio)
        img = img.resize((MAX_WIDTH, new_height), Image.Resampling.LANCZOS)
    
    # Convert to RGB if needed (for PNG with transparency)
    if img.mode in ("RGBA", "LA", "P"):
        rgb_img = Image.new("RGB", img.size, (255, 255, 255))
        rgb_img.paste(img, mask=img.split()[-1] if img.mode == "RGBA" else None)
        img = rgb_img
    
    # Compress to JPEG 70% quality
    buffer = BytesIO()
    img.save(buffer, format="JPEG", quality=70, optimize=True)
    buffer.seek(0)
    
    # Convert to base64
    image_bytes = buffer.getvalue()
    base64_str = base64.b64encode(image_bytes).decode("utf-8")
    
    return f"data:image/jpeg;base64,{base64_str}"


def get_db():
    """Dependency: Get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ========== ROUTES ==========

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    """Serve the invitation creation form"""
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/create")
async def create_invitation(
    name: str = Form(...),
    sender: str = Form(default="Your Secret Admirer"),
    message: str = Form(...),
    theme: str = Form(default="romantic"),
    photo: UploadFile = File(None),
):
    """
    Create a new invitation.
    
    - name: recipient name (required)
    - sender: sender name (optional)
    - message: invitation message (required)
    - theme: one of romantic/playful/elegant/minimalist
    - photo: optional image file
    
    Returns: Redirect to /view/{invitation_id}
    """
    db = SessionLocal()
    
    try:
        # Generate ID
        inv_id = generate_short_id()
        
        # Process photo if uploaded
        photo_base64 = None
        if photo and photo.filename:
            try:
                photo_base64 = compress_image(photo, max_size_mb=5)
            except ValueError as e:
                db.close()
                raise HTTPException(status_code=400, detail=str(e))
        
        # Create invitation record
        invitation = Invitation(
            id=inv_id,
            recipient_name=name.strip(),
            sender_name=sender.strip() or "Your Secret Admirer",
            message=message.strip(),
            theme=theme or "romantic",
            photo_base64=photo_base64,
        )
        
        db.add(invitation)
        db.commit()
        db.close()
        
        # Redirect to viewer
        return RedirectResponse(url=f"/view/{inv_id}", status_code=303)
    
    except Exception as e:
        db.close()
        raise HTTPException(status_code=500, detail=f"Error creating invitation: {str(e)}")


@app.get("/view/{inv_id}", response_class=HTMLResponse)
async def view_invitation(inv_id: str, request: Request):
    """Display the invitation"""
    db = SessionLocal()
    
    try:
        # Fetch invitation from database
        invitation = db.query(Invitation).filter(Invitation.id == inv_id).first()
        
        if not invitation:
            db.close()
            raise HTTPException(status_code=404, detail="Invitation not found")
        
        # Render viewer template with invitation data
        return templates.TemplateResponse(
            "viewer.html",
            {
                "request": request,
                "invitation_id": inv_id,
                "name": invitation.recipient_name,
                "sender": invitation.sender_name,
                "message": invitation.message,
                "theme": invitation.theme,
                "photo": invitation.photo_base64,
            },
        )
    
    finally:
        db.close()


@app.get("/health")
async def health():
    """Health check for deployment"""
    return {"status": "ok", "service": "valentines-invitation"}


# ========== ERROR HANDLERS ==========

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """Custom error page handler"""
    if exc.status_code == 404:
        return templates.TemplateResponse(
            "error.html",
            {
                "request": request,
                "status_code": 404,
                "message": "Invitation not found. 💔",
            },
            status_code=404,
        )
    
    return HTMLResponse(
        f"<h1>Error {exc.status_code}</h1><p>{exc.detail}</p>",
        status_code=exc.status_code,
    )


# ========== STARTUP ==========

if __name__ == "__main__":
    # Get port from environment (for Railway.app deployment)
    port = int(os.getenv("PORT", 8000))
    
    # Run server
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=port,
        reload=os.getenv("ENV", "production") != "production",
    )
