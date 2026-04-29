from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
import shutil
import os
import uuid
from deps import get_current_admin

router = APIRouter()

UPLOAD_DIR = "uploads"

@router.post("/")
async def upload_file(file: UploadFile = File(...), admin = Depends(get_current_admin)):
    if not os.path.exists(UPLOAD_DIR):
        os.makedirs(UPLOAD_DIR)
    
    file_extension = os.path.splitext(file.filename)[1]
    unique_filename = f"{uuid.uuid4()}{file_extension}"
    file_path = os.path.join(UPLOAD_DIR, unique_filename)
    
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    # Return the URL to access the file
    # In a real app, you might want to get the base URL from settings
    return {"url": f"/uploads/{unique_filename}"}
